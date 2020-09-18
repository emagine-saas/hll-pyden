import sys
import subprocess
from splunk import Intersplunk
from utils import load_pyden_config, get_proxies, pyden_env, createWorkingLog
import os
if sys.version > '3':
    from importlib import reload

confFile=False
if sys.argv[-1].startswith("conf="):
    confFile= sys.argv[-1].replace("conf=", "")

def pipExec(py_exec, log, sysargs, asCSV):
    if sysargs[-1] == "reloaded":
        reload(os)
        reload(sys)
        return

    if "conf=" in sysargs[-1] :
        sysargs[-1]="reloaded"
    else:
        sysargs.append("reloaded")

    proxies=()
    if asCSV:
        proxies = get_proxies(None)

    forkEnv=pyden_env(confFile, py_exec, "" )
    if proxies:
        forkEnv['HTTP_PROXY'] = proxies['http']
        forkEnv['HTTPS_PROXY'] = proxies['https']
    os.execve(py_exec, ['python'] + sysargs, forkEnv)

def pydenPip(log, asCSV, sysargs, verbose) ->int:
    pm_config, config = load_pyden_config()

    pyden_location = pm_config.get('appsettings', 'location')
    env = False
    pip_arg_index = 1
    if config.has_option('default-pys', 'environment'):
        env = config.get('default-pys', 'environment')
    for key, val in enumerate(sysargs):
        if 'environment' in val:
            env = val.split('=')[1]
            pip_arg_index = key
            break

    if not env:
        log.warning("pip, invoked with empty env, CRASH!")
        if asCSV:
            Intersplunk.generateErrorResults("Unknown/empty env, FAIL" )
        return 2
    py_exec = os.path.join(os.environ['SPLUNK_HOME'], config.get(env, 'executable'))
    verbose and log.debug("pip using "+py_exec+"/python interpreter")

    pipExec(py_exec, log, sysargs, asCSV)
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    pip = subprocess.call([py_exec, '-m', 'pip'] + sysargs[pip_arg_index:-1])
    if pip != 0:
        log.error("Pip exit status was non-zero "+str(pip))
        if asCSV:
            Intersplunk.generateErrorResults("[the real] Pip failed returned error "+str(pip) )
        return 3
    verbose and log.debug("pyden pip completed ")
    return 0


if __name__ == "__main__":
# with an object to mantain state, I can skip alot of these args on the sideEffect functions.
    log = createWorkingLog()
    sys.exit(pydenPip(log, True, sys.argv, False ))


