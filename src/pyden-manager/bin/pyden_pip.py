import sys
import subprocess
from utils import load_pyden_config, get_proxies, pyden_env, createWorkingLog
import os
if sys.version > '3':
    from importlib import reload
if sys.version < '3':
    from HTMLParser import HTMLParser
    sys.path.append( os.environ['SPLUNK_HOME']+os.sep+ 'lib' +os.sep+'python2.7'+os.sep+'site-packages' + os.sep+'splunk'+os.sep)
else:
    from html.parser import HTMLParser
    sys.path.append( os.environ['SPLUNK_HOME']+os.sep+ 'lib' +os.sep+'python3.7'+os.sep+'site-packages' + os.sep+'splunk'+os.sep)
import Intersplunk

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

    pyden_location = config.get('appsettings', 'location')
    env = False
    pip_arg_index = 1
    conf_arg_index=-1
    if config.has_option('default-pys', 'environment'):
        env = config.get('default-pys', 'environment')
    for key, val in enumerate(sysargs):
        if 'environment' in val:
            env = val.split('=')[1]
            pip_arg_index = key +1 # needs to be after this item
        if 'conf' in val:
            conf_arg_index = key 

    if not env:
        log.warning("pip, invoked with empty env, CRASH!")
        if asCSV:
            Intersplunk.generateErrorResults("Unknown/empty env, FAIL" )
        return 2
    py_exec = os.path.join(os.environ['SPLUNK_HOME'], config.get(env, 'executable'))
    verbose and log.debug("pip using "+py_exec+"/python interpreter")
    out=None
#    pipExec(py_exec, log, sysargs, asCSV)
# This output is inherited from the original code base; its not great for unit tests
#    sys.stdout.write("messages\n")
#    sys.stdout.flush()
    try:
        proxies = get_proxies(None)
        cnmd=None
        if proxies:
            cmd=[py_exec, '-m', 'pip', '--proxy', proxies['https'] ] + sysargs[pip_arg_index:conf_arg_index ]
        else:
            cmd=[py_exec, '-m', 'pip' ] + sysargs[pip_arg_index:conf_arg_index ]
        if conf_arg_index < 0:
            conf_arg_index=len(sysargs)
        verbose and log.debug("pyden pip started "+str(cmd ) )
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=10 )
        verbose and log.debug("pyden pip completed ")
        log.error("PIP output "+ out.decode())
        if asCSV:
            Intersplunk.outputResults([ "[the real pip]: library "+str(sysargs[pip_arg_index:conf_arg_index ])+ " is installed " ])
        return 0
#

    except BaseException as e:
        log.error("[the real] Pip failed returned error "+str(e) )
        if type(out) != type(None): 
            log.error("[the real] Pip failed returned error "+str(out) )
        if asCSV:
            Intersplunk.generateErrorResults("[the real] Pip failed returned error "+str(out) )
        return 3


if __name__ == "__main__":
    sys.stdin.close()
# with an object to maintain state, I can skip alot of these args on the sideEffect functions.
    log = createWorkingLog()
    sys.exit(pydenPip(log, True, sys.argv, False ))


