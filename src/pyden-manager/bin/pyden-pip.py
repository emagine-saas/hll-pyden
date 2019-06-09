import sys
import subprocess
from splunk_logger import setup_logging
from utils import load_pyden_config
import os
if sys.version > '3':
    from importlib import reload


def activate():
    if sys.argv[-1] == "reloaded":
        reload(os)
        reload(sys)
        return

    sys.argv.append("reloaded")
    bin_dir = os.path.dirname(py_exec)
    path = bin_dir + os.pathsep + os.environ["PATH"]
    os.execve(py_exec, ['python'] + sys.argv, {"PATH": path, "SPLUNK_HOME": os.environ['SPLUNK_HOME']})


if __name__ == "__main__":
    logger = setup_logging()
    pyden_location, config = load_pyden_config()
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
    activate()
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    pip = subprocess.call([py_exec, '-m', 'pip'] + sys.argv[pip_arg_index:-1])
