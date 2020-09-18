import csv
import sys
import os
from ConfigParser import ConfigParser

def VersionStatus( sysargs, readSide, writeSide) ->int:
    versionfield = sysargs[1]
    statusfield = sysargs[2]
    is_defaultfield = sysargs[3]

    r = csv.DictReader( readSide )
    header = r.fieldnames

    w = csv.DictWriter( writeSide, fieldnames=header)
    w.writeheader()

    default_conf = os.path.abspath(os.path.join(os.pardir, 'default', 'pyden.conf'))
    local_conf = os.path.abspath(os.path.join(os.pardir, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([default_conf, local_conf])
    pyden_location = config.get('appsettings', 'location')
    pyden_config = ConfigParser()
    pyden_local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    pyden_config.read([pyden_local_conf])
    if pyden_config.has_option("default-pys", "distribution"):
        default_version = pyden_config.get("default-pys", "distribution")
    else:
        default_version = None

    for result in r:
        if versionfield not in result.keys():
            # no version provided
            return 1
        version = result[versionfield]
        result[statusfield] = 1 if version in pyden_config.sections() else 0
        result[is_defaultfield] = 1 if version == default_version else 0
        w.writerow(result)
    return 0

if __name__ == "__main__":
    sys.exit( VersionStatus( sys.argv, sys.stdin, sys.stdout) )

