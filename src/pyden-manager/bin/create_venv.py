import sys
import os
import subprocess
from splunk_logger import setup_logging
from utils import load_pyden_config, write_pyden_config
if sys.version < '3':
    pass
else:
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
    args = dict()
    for arg in sys.argv[1:]:
        try:
            if "reloaded" in arg:
                continue
            k, v = arg.split('=')
            args[k] = v
        except ValueError:
            logger.error("Incorrect argument provided")
            sys.exit(1)
    pyden_location, config = load_pyden_config()
    if 'name' not in args:
        logger.error("No name for the new environment was provided.")
        sys.exit(1)
    # get executable
    version = args.get('version')
    if not version:
        if config.has_option("default-pys", "distribution"):
            version = config.get("default-pys", "distribution")
    name = args['name']
    if version in config.sections():
        py_exec = os.path.join(os.environ['SPLUNK_HOME'], config.get(version, 'executable'))
        activate()
    else:
        logger.error("Python version not found in pyden.conf.")
        sys.exit(1)
    if not config.has_option("default-pys", "environment"):
        write_pyden_config(pyden_location, config, 'default-pys', 'environment', name)

    venv_dir = os.path.join(pyden_location, 'local', 'lib', 'venv')
    if not os.path.isdir(venv_dir):
        os.makedirs(venv_dir)
    os.chdir(venv_dir)
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    subprocess.call([py_exec, '-m', "virtualenv", name])
    venv_exec = os.path.join(venv_dir, name, 'bin', 'python')
    write_pyden_config(pyden_location, config, name, "executable", venv_exec.lstrip(os.environ['SPLUNK_HOME']))
    write_pyden_config(pyden_location, config, name, 'version', version)
