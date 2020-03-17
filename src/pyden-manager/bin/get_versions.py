from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re
import sys
from splunk_logger import setup_logging
from utils import get_proxies, createWorkingLog

if __name__ == "__main__":
    logger = createWorkingLog()
    #logger.debug( "XXXX")
    settings = dict()
    Intersplunk.readResults(settings=settings)
    #logger.debug( "XXXX")
    session_key = settings['sessionKey']
    proxies = get_proxies(session_key)
    #logger.debug( "XXXX "+str(sys.version_info))

    download_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                                 sessionKey=session_key)[1]
    r = requests.get(download_url, proxies=proxies)
    #logger.debug( "XXXX")
    version_pattern = r"""<a href\=\"\d(?:\.\d{1,2}){1,2}\/\"\>(?P<version>\d(?:\.\d{1,2}){1,2})"""
    all_versions = re.findall(version_pattern, r.text)
    #logger.debug( "XXXX ")
    logger.debug(all_versions)
    compatible_versions = [version for version in all_versions if (version.startswith('2') and version > '2.7') or (
                version.startswith('3') and version > '3.5')]
    #logger.debug( "XXXX")

    # logger.debug(compatible_versions)
    # sometime there are only pre release or release candidates so we need to check each compatible version for release
    for version in compatible_versions:
        # logger.debug( "XXXX")
        url = str(download_url, 'utf-8').rstrip() +'/'+ str( version)+"/"
        logger.debug(url)
        r = requests.get(url, headers={'Cache-Control': 'no-cache'}, proxies=proxies)
        source_pattern = r"""<a href=\"(?P<link>.*)\">Python-{}.tgz""".format( version.replace('.', '\\.'))
        # logger.debug(source_pattern)
        # logger.debug(r.text)
        match = re.findall(source_pattern, r.text)
        #logger.debug( "XXXX")
        # logger.debug(match)
        if not match:
            # logger.debug(version)
            compatible_versions.remove(version)
    # logger.debug(compatible_versions)
    results = [{'version': version} for version in compatible_versions]
    #logger.debug( "XXXX")
    Intersplunk.outputResults(results)
