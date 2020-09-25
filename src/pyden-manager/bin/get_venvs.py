from utils import load_pyden_config
from splunk import Intersplunk
import re
from utils import createWorkingLog

def getVEnvs(log, asCSV, verbose ):
    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    sections = config.sections()
    verbose and log.debug(sections)
    if "default-pys" in sections:
        sections.remove("default-pys")
    regex = re.compile(r"""\d\.\d{1,2}\.\d{1,2}""")
    venvs = [env for env in sections if not regex.match(env)]
    results = [{"environment": env} for env in venvs]
    verbose and log.debug("There are "+str(len(results))+" sections")
    for result in results:
        result['version'] = config.get(result['environment'], 'version')
        result["is_default"] = 1 if result['environment'] == config.get("default-pys", "environment") else 0
    if asCSV:
        Intersplunk.outputResults(results)
    else:
        return results


if __name__ == "__main__":
    logger = createWorkingLog()
    getVEnvs(logger, True, True )

