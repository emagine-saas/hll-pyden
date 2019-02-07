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
    pyden_location, config = load_pyden_config()
    if 'name' not in args:
        Intersplunk.generateErrorResults("No name for the new environment was provided.")
        sys.exit(1)
    # get executable
    version = args.get('version')
    if not version:
        if config.has_option("default-pys", "distribution"):
            version = config.get("default-pys", "distribution")
    name = args['name']
    if version in config.sections():
        py_exec = config.get(version, 'executable')
    else:
        py_exec = False
    if not py_exec:
        Intersplunk.generateErrorResults("Python version not found in pyden.conf.")
        sys.exit(1)
    if not config.has_section("default-pys") or not config.has_option("default-pys", "environment"):
        write_pyden_config(pyden_location, config, 'default-pys', name, attribute='environment')

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
    write_pyden_config(pyden_location, config, name, venv_exec)
