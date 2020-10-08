import sys
import os
import subprocess
from utils import load_pyden_config, write_pyden_config, pyden_env, createWorkingLog, getBtoolConfig
if sys.version_info[0] >= 3:
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
def pydenFork(py_exec, log, sysargs ):
    if sysargs[-1] == "reloaded":
        reload(os)
        reload(sys)
        return
    pydenFile= getBtoolConfig()

    sysargs.append("reloaded")
    log.debug("Applying external override "+str(confFile)+" on config file")
     
    forkEnv=pyden_env(confFile, py_exec, pydenFile )
    os.execve(py_exec, ['python'] + sys.argv, forkEnv)

def getBtoolConfig():
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_out, proc_err = proc.communicate()
    return proc_out.decode()

def setup(log, sysargs):
    args={}
    for arg in sysargs[1:]:
        try:
            if "reloaded" in arg:
                continue
            k, v = arg.split('=')
            args[k] = v
        except ValueError:
            log.error("Incorrect argument format provided: "+str(sysargs))
            return [2, "Incorrect argument format provided.",  "", "", "" ]

    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    if 'name' not in args:
        log.error("No name param for the new environment was provided.")
        return [3, "No name param for the new environment was provided.", "", "", ""]

    # get executable
    version = args.get('version')
    if not version:
        if config.has_option("default-pys", "distribution"):
            version = config.get("default-pys", "distribution")
    name = args['name']
    log.debug("Understood request as create venv for "+str(name)+" "+str(version)+".")
    if version in config.sections():
        py_exec = os.path.join(os.environ['SPLUNK_HOME'], config.get(version, 'executable'))
        return [0, py_exec, pyden_location, name, version]
    else:
        log.error("Unknown Python version "+str(version)+" (looking at pyden.conf).")
        return [4, "Unknown Python version (looking at pyden.conf).", "", "", ""]

def createVenv(log, binary, where, name, version ):
    pm_config, config = load_pyden_config()
    if not config.has_option("default-pys", "environment"):
        write_pyden_config(where, config, 'default-pys', 'environment', name)

    venv_dir = os.path.join(where, 'local', 'lib', 'venv')
    if not os.path.isdir(venv_dir):
        os.makedirs(venv_dir)
    os.chdir(venv_dir)

    venv = subprocess.Popen([binary, '-m', "virtualenv", name], stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE, universal_newlines=True)
    result, error = venv.communicate()
    for message in result.split('\n'):
        if message:
            log.info("[stdout] Sub process said: "+ message)
    for message in error.split('\n'):
        if message:
            log.error("[stderr] Sub process said: "+message)
    if venv.returncode != 0:
        log.error( "Sub process return value "+venv.returncode+" isn't valid (did something crash?).")
        if sys.version_info[0] > 2:
            from splunk import Intersplunk
            Intersplunk.generateErrorResults( "Sub process return value "+venv.returncode+" isn't valid (did something crash?)." )
        return 5
    venv_exec = os.path.join(venv_dir, name, 'bin', 'python')
    write_pyden_config(where, config, name, "executable", venv_exec.lstrip(os.environ['SPLUNK_HOME']))
    write_pyden_config(where, config, name, 'version', version)
    log.info("Successfully created venv ")
    if sys.version_info[0] > 2:
        from splunk import Intersplunk
        Intersplunk.addErrorMessage({}, "Everything is OK")
        Intersplunk.outputResults( [ ])
    return 0

if __name__ == "__main__":
    log = createWorkingLog()
    ret, binary, predictableLocation, venvname, venvversion=setup(log, sys.argv)
    if ret != 0 and sys.version_info[0] > 2:
        from splunk import Intersplunk
        Intersplunk.generateErrorResults(binary )
        sys.exit(ret)

    elif ret == 0:
#        pydenFork(binary, log, sys.argv)
        ret=createVenv(log, binary, predictableLocation, venvname, venvversion )
        sys.exit(ret)
    else: # somehow using py2
        sys.exit(ret)
      
    
