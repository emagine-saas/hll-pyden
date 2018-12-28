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


def write_pyden_config(pyden_location, config, stanza, value, attribute="executable"):
    local_conf = os.path.join(pyden_location, 'local', 'pyden.conf')
    local_dir = os.path.dirname(local_conf)
    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    if not config.has_section(stanza):
        config.add_section(stanza)
    config.set(stanza, attribute, value)
    with open(local_conf, 'wb') as f:
        config.write(f)
