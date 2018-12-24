import csv
import sys
import os
from ConfigParser import ConfigParser


def main():
    versionfield = sys.argv[1]
    statusfield = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=header)
    w.writeheader()

    default_conf = os.path.abspath(os.path.join(os.pardir, 'default', 'pyden.conf'))
    local_conf = os.path.abspath(os.path.join(os.pardir, 'local', 'pyden.conf'))
    config = ConfigParser()
    config.read([default_conf, local_conf])
    pyden_location = config.get('app', 'location')
    pyden_config = ConfigParser()
    pyden_local_conf = os.path.abspath(os.path.join(pyden_location, 'local', 'pyden.conf'))
    pyden_config.read([pyden_local_conf])

    for result in r:
        if versionfield not in result.keys():
            # no version provided
            sys.exit(1)
        version = result[versionfield]
        result[statusfield] = 1 if version in pyden_config.sections() else 0
        w.writerow(result)


if __name__ == "__main__":
    main()
