import sys
from splunk import Intersplunk
from utils import createWorkingLog, load_pyden_config, write_pyden_config


def setDefaultPhy(dist, env, asCSV ) ->int:
    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    if dist:
        if dist in config.sections():
            write_pyden_config(pyden_location, config, "default-pys", "distribution", dist)
        else:
            if asCSV:
                Intersplunk.generateErrorResults("The Python version %s is not installed yet." % dist)
            return 2
    if env:
        if env in config.sections():
            write_pyden_config(pyden_location, config, "default-pys", "environment", env)
        else:
            if asCSV:
                Intersplunk.generateErrorResults("The virtual environment %s does not exist." % env)
            return 3
    if asCSV:
        Intersplunk.outputResults([{"message": "Successfully changed defaults"}])
    return 0


if __name__ == "__main__":
    logger = createWorkingLog()
    distribution = False
    environment = False
    for arg in sys.argv:
        if "distribution" in arg:
            distribution = arg.split("=")[1]
        if "environment" in arg:
            environment = arg.split("=")[1]
    if not (distribution or environment):
        Intersplunk.generateErrorResults(
            "The changedefaultpys command requires at least one argument of distribution or environment")
        logger.error("The changedefaultpys command requires at least one argument of distribution or environment")
        sys.exit(1)
    else:
        sys.exit( setDefaultPhy(distribution, environment, True) )


