from utils import load_pyden_config
from splunk import Intersplunk
import re
import subprocess
from splunk_logger import setup_logging


if __name__ == "__main__":
    logger = setup_logging()
    pyden_location, config = load_pyden_config()
    sections = config.sections()
    logger.debug(sections)
    if "default-pys" in sections:
        sections.remove("default-pys")
    regex = re.compile(r"""\d\.\d{1,2}\.\d{1,2}""")
    venvs = [env for env in sections if not regex.match(env)]
    results = [{"environment": env} for env in venvs]
    for result in results:
        executable = config.get(result['environment'], 'executable')
        p = subprocess.Popen([executable, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()
        version = (output + err).strip()
        result['version'] = version
        result["is_default"] = 1 if result['environment'] == config.get("default-pys", "environment") else 0

    Intersplunk.outputResults(results)
