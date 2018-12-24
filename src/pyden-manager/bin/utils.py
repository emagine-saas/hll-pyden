import os
import sys
if sys.version < '3':
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


def load_pyden_config():
    pm_config = ConfigParser()
    pm_default = os.path.abspath(os.path.join(os.pardir, 'default', 'pyden.conf'))
    pm_local = os.path.abspath(os.path.join(os.pardir, 'local', 'pyden.conf'))
    pm_config.read([pm_default, pm_local])
    pyden_location = pm_config.get('app', 'location')
    local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([local_conf])
    return pyden_location, config


def write_pyden_config(pyden_location, stanza, value, attribute="executable"):
    local_conf = os.path.join(pyden_location, 'local', 'pyden.conf')
    local_dir = os.path.dirname(local_conf)
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    write_mode = 'a+' if os.path.isfile(local_conf) else 'w+'
    with open(local_conf, write_mode) as f:
        content = f.read()
        if len(content) > 0:
            f.write("\n")
        content = """[%s]\n%s = %s\n""" % (stanza, attribute, value)
        f.write(content)
