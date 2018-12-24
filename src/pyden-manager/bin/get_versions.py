from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re

if __name__ == "__main__":
    # logger = setup_logging()
    settings = dict()
    Intersplunk.readResults(settings=settings)
    session_key = settings['sessionKey']
    download_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                                 sessionKey=session_key)[1]
    r = requests.get(download_url)
    version_pattern = r"""<a href\=\"\d(?:\.\d{1,2}){1,2}\/\"\>(?P<version>\d(?:\.\d{1,2}){1,2})"""
    all_versions = re.findall(version_pattern, r.text)
    compatible_versions = [version for version in all_versions if (version.startswith('2') and version > '2.7') or (
                version.startswith('3') and version > '3.5')]
    # sometime there are only pre release or release candidates so we need to check each compatible version for release
    for version in compatible_versions:
        url = download_url.rstrip() + "/%s/" % version
        r = requests.get(url)
        source_pattern = r"""<a href=\"(?P<link>.*)\">Python-%s.tgz""" % version.replace('.', '\\.')
        match = re.findall(source_pattern, r.text)
        if not match:
            compatible_versions.remove(version)
    results = [{'version': version} for version in compatible_versions]
    Intersplunk.outputResults(results)
