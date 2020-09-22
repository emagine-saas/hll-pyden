
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
from util import createWorkingLog
from get_venvs import getVEnvs

if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yours self to support other non-server OS \n")
    sys.exit(1)

class getPackagesTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append('/opt/splunk/etc/apps/pyden-manager/bin/')
        sys.path.append('/opt/splunk/etc/apps' +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( '/opt/splunk/lib/python3.7/site-packages')
        sys.path.append( '/opt/splunk/lib/python3.7/site-packages/splunk/')
        sys.stdin.close()

    def test1(self):
        # assumes a standard inatall has already happened
        log=createWorkingLog()
        ret=getVEnvs(log, False, True)
        self.assertTrue(type(ret) == type([]), "should have an array of results" )
        self.assertTrue(len(ret) == 1, "likely to only have one vEnv" )
        self.assertTrue('environment' in ret[0] , "slot[0] should have a name" )
        self.assertTrue('is_default' in ret[0] , "slot[0] should have a default flag" )
        self.assertTrue('version' in ret[0] , "slot[0] should have version tag" )
    
if( __name__=='__main__'):
    unittest.main()    
    
