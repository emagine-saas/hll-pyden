import sys
import requests
from splunk import Intersplunk
from utils import get_proxies
if sys.version < '3':
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser



class PyPIHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.packages = []
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_body:
            package = data.replace(' ', '').replace('\n', '')
            if package:
                self.packages.append(package)


def get_simple_index( proxies) ->list :
    parser = PyPIHTMLParser()

    r = requests.get("https://pypi.org/simple/", proxies=proxies)
    parser.feed(r.text)
    return [{'package': package} for package in parser.packages]

def get_package_description(package, proxies) ->list:
    r = requests.get("https://pypi.org/pypi/%s/json" % package, proxies=proxies)

    return [{"description": r.json()['info']['description']}]

def getPackages(sysargs, asCSV ):
    settings = dict()
    proxies = get_proxies(None)
    if sysargs[1] == "pypi_simple_index":
        results = get_simple_index( proxies)
    else:
        results = get_package_description(sysargs[1], proxies)

    if asCSV:
        Intersplunk.outputResults(results)
    else:
        return results

if __name__ == "__main__":
    getPackages(sys.argv, True)



