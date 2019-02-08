import os
import sys
if sys.version < '3':
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser
    from importlib import reload


pyden_config = ConfigParser()
pyden_default = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, 'pyden', 'default', 'pyden.conf'))
pyden_local = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir, 'pyden', 'local', 'pyden.conf'))
pyden_config.read([pyden_default, pyden_local])


class ActivationError(Exception):
    pass


def activate_venv(environment):
    if environment in pyden_config.sections():
        py_exec = pyden_config.get(environment, 'executable')
    else:
        raise ActivationError

    # if sys.argv[-1] == "reloaded":
    if "pyden" in sys.executable:
        reload(os)
        reload(sys)
        return

    # sys.argv.append("reloaded")
    base = os.path.dirname(os.path.dirname(pyden_config.get(environment, "executable")))
    path = base + "/bin" + os.pathsep + os.environ["PATH"]
    os.execve(py_exec, ['python'] + sys.argv, {"PATH": path})


def activate_venv_or_die(env=False):
    if not env:
        env = pyden_config.get('default-pys', 'environment')
    try:
        activate_venv(env)
    except ActivationError:
        sys.exit(1)
