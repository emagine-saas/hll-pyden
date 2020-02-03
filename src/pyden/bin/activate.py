import os
import subprocess
import sys
if sys.version < '3':
    from ConfigParser import ConfigParser
    from StringIO import StringIO
else:
    from configparser import ConfigParser
    from importlib import reload
    from io import StringIO

# The pyden-env will need to define:
#    * PYTHONPATH to be able to exec splunk responses; needs to hold the dir for local pyden installed libraries and splunk site-packages, with correct version of python
#          os.path.dirname(os.path.dirname(__file__))+ os.sep+ str(os.sep).join(["local", "lib", "venv","timesuite", "lib", "python3.7", "site-packages"])+os.pathsep +
## Python version is locked here, as we have just installed it, ourselves.  Likewise the venv as installed by us, now.
#          os.environ['SPLUNK_HOME']+os.sep+"lib"+os.sep+"python3.7"+os.sep+ "site-packages" +os.sep
#    * SPLUNK_HOME to do normal stuff
#

pyden_config = ConfigParser()
if 'PYDEN_CONFIG' in os.environ:
    pout = os.environ["PYDEN_CONFIG"]
else:
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
# https://www.python.org/dev/peps/pep-0278/
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True )
    pout, proc_err = proc.communicate()
buf = StringIO(pout)
pyden_config.readfp(buf)


class ActivationError(Exception):
    pass


def activate_venv(env, confFile):
    if env in pyden_config.sections():
        py_exec = os.path.join(os.environ.get("SPLUNK_HOME", ""), pyden_config.get(env, "executable"))
    else:
        raise ActivationError

    if "pyden" in sys.executable:
        reload(os)
        reload(sys)
        return
    forkEnv=pyden_env(confFile, py_exec, proc_out ) 
    os.execve(py_exec, ['python'] + sys.argv, forkEnv)

def activate_venv_or_die(env=False, confFile=False):
    if not env:
        env = pyden_config.get('default-pys', 'environment')
    try:
        activate_venv(env, confFile)
    except ActivationError:
        sys.exit(1)

def pyden_env(confFile, py_exec, pyden):
    forkEnv={}
    if confFile and os.path.isfile( confFile):
        cc = ConfigParser()
        cc.optionxform=str
        cc.read(confFile)
        if 'pyden_env' in cc.sections():
            forkEnv=dict(cc.items('pyden_env'))
    forkEnv['PATH'] = os.path.dirname(py_exec) + os.pathsep + os.environ["PATH"]
    forkEnv['PYDEN_CONFIG']=pyden
    return forkEnv

