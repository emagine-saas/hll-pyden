import sys
import subprocess
from splunk_logger import setup_logging
from utils import load_pyden_config, get_proxies, pyden_env
import os
if sys.version > '3':
    from importlib import reload

confFile=False
if sys.argv[-1].startswith("conf="):
    confFile= sys.argv[-1].replace("conf=", "")

def activate(py_exec):
    if sys.argv[-1] == "reloaded":
        reload(os)
        reload(sys)
        return

    sys.argv.append("reloaded")
    from splunk import Intersplunk
    settings = dict()
    Intersplunk.readResults(settings=settings)
    session_key = settings['sessionKey']

    proxies = get_proxies(session_key)
    forkEnv=pyden_env(confFile, py_exec, "" )
    if proxies:
        forkEnv['HTTP_PROXY'] = proxies['http']
        forkEnv['HTTPS_PROXY'] = proxies['https']
    os.execve(py_exec, ['python'] + sys.argv, forkEnv)


if __name__ == "__main__":
    logger = setup_logging()
    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    env = False
    pip_arg_index = 1
    if config.has_option('default-pys', 'environment'):
        env = config.get('default-pys', 'environment')
    for arg in sys.argv:
        if 'environment' in arg:
            env = arg.split('=')[1]
            pip_arg_index = 2
            break
    if not env:
        sys.exit(1)
    py_exec = os.path.join(os.environ['SPLUNK_HOME'], config.get(env, 'executable'))
    activate(py_exec)
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    pip = subprocess.call([py_exec, '-m', 'pip'] + sys.argv[pip_arg_index:-1])
