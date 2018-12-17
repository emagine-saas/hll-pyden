import sys
import os
import subprocess
from splunk import Intersplunk
from utils import load_pyden_config, write_pyden_config


if __name__ == "__main__":
    args = dict()
    for arg in sys.argv[1:]:
        try:
            k, v = arg.split('=')
            args[k] = v
        except ValueError:
            Intersplunk.generateErrorResults("Incorrect argument provided")
            sys.exit(1)
    settings = dict()
    Intersplunk.readResults(settings=settings)
    session_key = settings['sessionKey']
    if 'version' not in args or 'name' not in args:
        Intersplunk.generateErrorResults("Must supplied both a version and a name for the new environment.")
        sys.exit(1)
    # get executable
    version = args['version']
    name = args['name']
    pyden_location, config = load_pyden_config(session_key)
    if version in config.sections():
        py_exec = config.get(version, 'executable')
    else:
        py_exec = False
    if not py_exec:
        Intersplunk.generateErrorResults("Python version not found in pyden.conf.")
        sys.exit(1)
    if "default" not in config.sections():
        write_pyden_config(pyden_location, 'default', name, attribute='environment')

    if version < '3':
        module = "virtualenv"
    else:
        module = 'venv'

    venv_dir = os.path.join(pyden_location, 'local', 'lib', 'venv')
    if not os.path.isdir(venv_dir):
        os.makedirs(venv_dir)
    os.chdir(venv_dir)
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    subprocess.call([py_exec, '-m', module, name])
    venv_exec = os.path.join(venv_dir, name, 'bin', 'python')
    write_pyden_config(pyden_location, name, venv_exec)
