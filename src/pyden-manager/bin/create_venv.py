import sys
import os
import subprocess
from splunk_logger import setup_logging
from utils import load_pyden_config, write_pyden_config
if sys.version < '3':
    pass
else:
    from importlib import reload

if sys.argv[-1].startswith("conf="):
    confFile= sys.argv[-1].replace("conf=", "")
	

# The pyden-env will need to define:
#    * PYTHONPATH to be able to exec splunk responses; needs to hold the dir for local pyden installed libraries and splunk site-packages, with correct version of python
#          os.path.dirname(os.path.dirname(__file__))+ os.sep+ str(os.sep).join(["local", "lib", "venv","timesuite", "lib", "python3.7", "site-packages"])+os.pathsep +
## Python version is locked here, as we have just installed it, ourselves.  Likewise the venv as installed by us, now.
#          os.environ['SPLUNK_HOME']+os.sep+"lib"+os.sep+"python3.7"+os.sep+ "site-packages" +os.sep
#    * SPLUNK_HOME to do normal stuff
#
def activate(py_exec):
    if sys.argv[-1] == "reloaded":
        reload(os)
        reload(sys)
        return

    sys.argv.append("reloaded")
    bin_dir = os.path.dirname(py_exec)

    if confFile and os.path.isfile( confFile):
        cc = ConfigParser()
        cc.read(confFile) 
        if 'pyden_env' in cc:
            forkEnv=cc['pyden_env']
    else:
        forkEnv={}
    base = os.path.dirname(py_exec)
    forkEnv['PATH'] = base + os.pathsep + os.environ["PATH"]
    forkEnv['PYDEN_CONFIG']=proc_out

    path = bin_dir + os.pathsep + os.environ["PATH"]
    os.execve(py_exec, ['python'] + sys.argv, forkEnv)


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
    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
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
        activate(py_exec)
    else:
        logger.error("Python version not found in pyden.conf.")
        sys.exit(1)
    if not config.has_option("default-pys", "environment"):
        write_pyden_config(pyden_location, config, 'default-pys', 'environment', name)

    venv_dir = os.path.join(pyden_location, 'local', 'lib', 'venv')
    if not os.path.isdir(venv_dir):
        os.makedirs(venv_dir)
    os.chdir(venv_dir)
    venv = subprocess.Popen([py_exec, '-m', "virtualenv", name], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            universal_newlines=True)
    result, error = venv.communicate()
    for message in result.split('\n'):
        if message:
            logger.info(message)
    for message in error.split('\n'):
        if message:
            logger.error(message)
    if venv.returncode != 0:
        sys.exit(1)
    venv_exec = os.path.join(venv_dir, name, 'bin', 'python')
    write_pyden_config(pyden_location, config, name, "executable", venv_exec.lstrip(os.environ['SPLUNK_HOME']))
    write_pyden_config(pyden_location, config, name, 'version', version)

