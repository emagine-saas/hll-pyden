import os
import subprocess
import sys
import logging
# Log verboseness names are fairly obvious 
DESIRED_LOG_LEVEL=logging.DEBUG
from splunk_logger import setup_logging
if sys.version < '3':
    from ConfigParser import ConfigParser,NoOptionError, NoSectionError
    from StringIO import StringIO
else:
    from configparser import ConfigParser,NoOptionError, NoSectionError
    from io import StringIO

# this log object is turned off somewhere
# also this set of logging is less useful as it doesnt report current state, just that the script got that far
util_logger = setup_logging()


def load_pyden_config():
    util_logger.debug("Loading Pyden config")
    pm_config = ConfigParser()
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    util_logger.debug("Reading config from btool")
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_out, proc_err = proc.communicate()
    buf = StringIO(proc_out.decode())
    pm_config.readfp(buf)
    util_logger.debug("Grabbing config attributes like location")
    pyden_location = pm_config.get('appsettings', 'location')
    local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([local_conf])
    util_logger.debug("Returning writable config object")
    return pm_config, config


def write_pyden_config(pyden_location, config, stanza, attribute, value):
    local_conf = os.path.join(pyden_location, 'local', 'pyden.conf')
    local_dir = os.path.dirname(local_conf)
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    if not config.has_section(stanza):
        config.add_section(stanza)
    config.set(stanza, attribute, value)
    with open(local_conf, 'w') as f:
        config.write(f)


def get_proxies(session_key):
    if(type(session_key) == type(None)):
        settings=dict()
        Intersplunk.readResults(settings=settings)
        session_key = settings['sessionKey']

    import splunk.entity as entity
    util_logger.debug("Getting proxy settings")
    myapp = 'pyden-manager'
    user = ""
    password = ""
    util_logger.debug("Getting proxy password")
    try:
        entities = entity.getEntities(['admin', 'passwords'], namespace=myapp, owner='nobody', sessionKey=session_key)
    except Exception as e:
        util_logger.error("Could not obtain proxy credentials")
        raise Exception("Could not get %s credentials from splunk. Error: %s" % (myapp, str(e)))

    for i, c in entities.items():
        user, password = c['username'], c['clear_password']

    auth = "%s:%s@" % (user, password) if user else ""
    proxy = load_pyden_config()[0].get('appsettings', 'proxy')

    proxies = {
        "http": "http://%s%s/" % (auth, proxy),
        "https": "https://%s%s/" % (auth, proxy)
    } if proxy else {}
    return proxies

def pyden_env(confFile, py_exec, pyden):
    forkEnv={}
    if confFile and os.path.isfile( confFile):
        cc = ConfigParser()
        cc.optionxform=str
        cc.read(confFile)
        if 'pyden_env' in cc.sections():
            forkEnv=dict(cc.items('pyden_env'))
    base = os.path.dirname(py_exec)
    forkEnv['PATH'] = base + os.pathsep + os.environ["PATH"]
    forkEnv['PYDEN_CONFIG']=pyden
    if not 'SPLUNK_HOME' in forkEnv:
        forkEnv['SPLUNK_HOME']='/opt/splunk'
    return forkEnv

# this function should be called
# def readLocalConfigWithoutANetworkStack(section, item):
def readConfig(section, item):
    config=os.path.dirname(os.path.dirname( os.path.realpath(__file__))) + os.sep+ "local"+os.sep+ "pyden.conf"
    c = ConfigParser()
    c.read( config)
    ret=False
    try:
        ret = c.get( section, item )
    except NoOptionError:
        pass
    except NoSectionError:
        config=os.path.dirname(os.path.dirname( os.path.realpath(__file__))) + os.sep+ "default"+os.sep+ "pyden.conf"
        c2 = ConfigParser()
        c2.read( config)
        try:
            ret = c2.get( section, item )
        except NoOptionError:
            pass
        except NoSectionError:
            pass

    return ret

def createWorkingLog():
    LOGFILE = os.sep.join([ os.environ['SPLUNK_HOME'], 'var', 'log', 'splunk', 'hll-setup.log'])
# https://stackoverflow.com/questions/533048/how-to-log-source-file-name-and-line-number-in-python
# had to add the process id item, due to all the fork/ exec in pyden
    FORMAT = "%(asctime)-15s [%(process)d]  %(funcName)s # %(lineno)s %(message)s "
    l = logging.getLogger("pyden-man")
    l.setLevel( DESIRED_LOG_LEVEL )
    ch = logging.FileHandler(LOGFILE )
    formatter = logging.Formatter(FORMAT )
    ch.setFormatter(formatter)
    l.addHandler(ch)
    return l
   
