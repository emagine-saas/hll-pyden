import sys
import subprocess
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
    base = os.path.dirname(os.path.dirname(py_exec))
    path = base + "/bin" + os.pathsep + os.environ["PATH"]
    os.execve(py_exec, ['python'] + sys.argv, {"PATH": path})


if __name__ == "__main__":
    pyden_location, config = load_pyden_config()
    env = False
    pip_arg_index = 1
    if config.has_option('default', 'environment'):
        env = config.get('default', 'environment')
    for arg in sys.argv:
        if 'environment' in arg:
            env = arg.split('=')[1]
            pip_arg_index = 2
            break
    if not env:
        sys.exit(1)
    py_exec = config.get(env, 'executable')
    activate()
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    subprocess.call([py_exec, '-m', 'pip'] + sys.argv[pip_arg_index:-1])
