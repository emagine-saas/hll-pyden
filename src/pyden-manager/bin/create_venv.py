import sys
import os
import subprocess
from splunk import Intersplunk
from utils import load_pyden_config, write_pyden_config, pyden_env, createWorkingLog
if sys.version >= '3':
    from importlib import reload

confFile=False
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
    pydenFile= getBtoolConfig()

    sys.argv.append("reloaded")
    log.debug("Applying external override "+str(confFile)+" on config file")
     
    forkEnv=pyden_env(confFile, py_exec, pydenFile )
    if not 'SPLUNK_HOME' in forkEnv:
        forkEnv['SPLUNK_HOME']='/opt/splunk'
    os.execve(py_exec, ['python'] + sys.argv, forkEnv)

def getBtoolConfig():
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_out, proc_err = proc.communicate()
    return proc_out.decode()

if __name__ == "__main__":
    log = createWorkingLog()
    args = dict()
    for arg in sys.argv[1:]:
        try:
            if "reloaded" in arg:
                continue
            k, v = arg.split('=')
            args[k] = v
        except ValueError:
            log.error("Incorrect argument format provided: "+str(sys.argv))
            Intersplunk.generateErrorResults("Incorrect argument format provided." )
            sys.exit(2)

    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    if 'name' not in args:
        log.error("No name param for the new environment was provided.")
        Intersplunk.generateErrorResults("No name param for the new environment was provided." )
        sys.exit(3)

    # get executable
    version = args.get('version')
    if not version:
        if config.has_option("default-pys", "distribution"):
            version = config.get("default-pys", "distribution")
    name = args['name']
    log.debug("Understood request as create venv for "+str(name)+" "+str(version)+".")
    if version in config.sections():
        py_exec = os.path.join(os.environ['SPLUNK_HOME'], config.get(version, 'executable'))
        activate(py_exec)
    else:
        log.error("Unknown Python version "+str(version)+" (looking at pyden.conf).")
        Intersplunk.generateErrorResults( "Unknown Python version (looking at pyden.conf)." )
        sys.exit(4)

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
            log.info("Sub process said: "+ message)
    for message in error.split('\n'):
        if message:
            log.error("Sub process said: "+message)
    if venv.returncode != 0:
        log.error( "Sub process return value "+venv.returncode+" isn't valid (did something crash?).")
        Intersplunk.generateErrorResults( "Sub process return value "+venv.returncode+" isn't valid (did something crash?)." )
        sys.exit(5)
    venv_exec = os.path.join(venv_dir, name, 'bin', 'python')
    write_pyden_config(pyden_location, config, name, "executable", venv_exec.lstrip(os.environ['SPLUNK_HOME']))
    write_pyden_config(pyden_location, config, name, 'version', version)
    log.info("Successfully created venv ")
    Intersplunk.addErrorMessage({}, "Everything is OK")
    Intersplunk.outputResults( [ ])

