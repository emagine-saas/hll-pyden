from splunk.rest import simpleRequest
import os
from ConfigParser import ConfigParser


def load_pyden_config(session_key):
    pyden_location = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/app/location",
                                   sessionKey=session_key)[1]
    default_conf = os.path.abspath(os.path.join(pyden_location, 'default', 'pyden.conf'))
    local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([default_conf, local_conf])
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
