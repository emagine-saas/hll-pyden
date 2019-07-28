import os
import subprocess
import sys
if sys.version < '3':
    from ConfigParser import ConfigParser
    from StringIO import StringIO
else:
    from configparser import ConfigParser
    from io import StringIO


def load_pyden_config():
    pm_config = ConfigParser()
    splunk_bin = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')
    proc = subprocess.Popen([splunk_bin, 'btool', 'pyden', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_out, proc_err = proc.communicate()
    buf = StringIO(proc_out.decode())
    pm_config.readfp(buf)

    pyden_location = pm_config.get('appsettings', 'location')
    local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([local_conf])
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
    import splunk.entity as entity
    myapp = 'pyden-manager'
    user = ""
    password = ""
    try:
        entities = entity.getEntities(['admin', 'passwords'], namespace=myapp, owner='nobody', sessionKey=session_key)
    except Exception as e:
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
