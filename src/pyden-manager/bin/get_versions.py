
from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re
import sys
from utils import get_proxies, createWorkingLog, readConfig

def getVersions(log, asCSV, verbose):
    settings = dict()
    proxies=()
    if asCSV:
        proxies = get_proxies(None)
        download_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                                 sessionKey=session_key)[1]
    else:
        download_url = readConfig('download', 'url')
        
    r = requests.get(download_url, proxies=proxies)
    version_pattern = r"""<a href\=\"\d(?:\.\d{1,2}){1,2}\/\"\>(?P<version>\d(?:\.\d{1,2}){1,2})"""
    all_versions = re.findall(version_pattern, r.text)
    verbose and log.debug(all_versions)
    compatible_versions = [version for version in all_versions if (version.startswith('2') and version > '2.7') or (
                version.startswith('3') and version > '3.5')]

    verbose and log.debug(compatible_versions)
    # sometime there are only pre release or release candidates so we need to check each compatible version for release
# https://www.mail-archive.com/python-list@python.org/msg447129.html
    for version in compatible_versions:
        url = download_url.rstrip() +'/'+ str( version)+"/"
        verbose and log.debug(url)
        r = requests.get(url, headers={'Cache-Control': 'no-cache'}, proxies=proxies)
        source_pattern = r"""<a href=\"(?P<link>.*)\">Python-{}.tgz""".format( version.replace('.', '\\.'))
        verbose and log.debug(source_pattern)
        verbose and log.debug(r.text)
        match = re.findall(source_pattern, r.text)
        verbose and log.debug(match)
        if not match:
            verbose and log.debug(version)
            compatible_versions.remove(version)
    verbose and log.debug(compatible_versions)
    results = [{'version': version} for version in compatible_versions]
    if asCSV:
        Intersplunk.outputResults(results)
    else:
        return results


if __name__ == "__main__":
    logger = createWorkingLog()
    getVersions(logger, True, False)


