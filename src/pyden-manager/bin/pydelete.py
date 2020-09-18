import sys
import os
from utils import load_pyden_config, createWorkingLog
import shutil

def whine(op, fn, excInfo):
    """
If onerror is provided, it must be a callable that accepts three parameters: 
   function, path, and excinfo. 
     The first parameter, function, is the function which raised the exception; it will be os.path.islink(), os.listdir(), os.remove() or os.rmdir(). 
     The second parameter, path, will be the path name passed to function. 
     The third parameter, excinfo, will be the exception information return by sys.exc_info(). 

Exceptions raised by onerror will not be caught.
"""
    log.error("FS Delete cmd failed on "+str(fn)+" saying "+str(excInfo))

def setup( log, sysargs, pm_config, config ) ->dict:
    pyden_location = pm_config.get('appsettings', 'location')
    local_conf = os.path.join(pyden_location, 'local', 'pyden.conf')

    local_dir = os.path.dirname(local_conf)
    name = sysargs[1]
    if name not in config.sections():
        log.error("delete FAIL: First param '"+name+"' doesn't seem to be installed here (conf).")
        return {'exit':2, 'dir':local_dir, 'dist':None, 'venv':None}
    pytype = False
    dist_dir = os.path.join(local_dir, 'lib', 'dist')
    venv_dir = os.path.join(local_dir, 'lib', 'venv')
    if name in os.listdir(dist_dir):
        pytype = "dist"
    if name in os.listdir(venv_dir):
        pytype = "venv"
    if not pytype:
        log.error("delete FAIL: First param '"+name+"' doesn't seem to be installed here (FS).")
        return { 'exit':3, 'dir':local_dir, 'dist':None, 'venv':None}
    return { 'exit':0, 'dir':local_dir, 'dist':dist_dir, 'venv':venv_dir, 'remove':name}


def pyDelete(log, values, config) ->int:
    config.remove_section( values['remove'])

    if not os.path.isdir(local_dir):
        os.mkdir(local_dir)
    shutil.rmtree(os.path.join(local_dir, 'lib', pytype, values['remove']), False, whine )

    if pytype == 'dist':
        pytype='distribution'
    else:
        pytype='environment'
    config.remove_option('default-pys', pytype)

    with open(local_conf, 'w+') as configfile:
        config.write(configfile)

    log.error("[unless this message is after errors] Successfully deleted "+ values['remove'])
    return 0


if __name__ == "__main__":
    log=createWorkingLog()
# I need to simplify the config object thing
# maybe an object?
    pm_config, config = load_pyden_config()
    values=setup(log, sys.argv, pm_config, config )
    if values.get('exit')==0:
        sys.exit(pyDelete(log, values, config))
    else:
        sys.exit( values['exit'])


