from utils import load_pyden_config, getConf
import sys
import os
from splunk import Intersplunk
import re
from utils import createWorkingLog

def getVEnvs(log, asCSV, verbose ):
    pm_config, config = load_pyden_config()
    conf=getConf()
    pyden_location= os.path.dirname(os.path.realpath(__file__))
    sections = conf.sections()
    verbose and log.debug(sections)
    if "default-pys" in sections:
        sections.remove("default-pys")
    regex = re.compile(r"""\d\.\d{1,2}\.\d{1,2}""")
    venvs = [env for env in sections if not regex.match(env)]
    results = [{"environment": env} for env in venvs]
    verbose and log.debug("There are "+str(len(results))+" sections")
    try:    
        for result in results:
            result['version'] = conf.get(result['environment'], 'version')
            result["is_default"] = 1 if result['environment'] == conf.get("default-pys", "environment") else 0
    except BaseException as e:
        pass

    if asCSV:
        Intersplunk.outputResults(results)
    else:
        return results


if __name__ == "__main__":
    logger = createWorkingLog()
    if '--no-block' in sys.argv:
        tt=getVEnvs(logger, False, True )
        print("version,is_default")
        for i in tt:
            print(str(i['version'])+","+str(i['is_default']))

    else:
        getVEnvs(logger, True, False )

