
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yours self to support other non-server OS \n")
    sys.exit(1)

class getVersionTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append(os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden-manager"+os.sep+"bin"+os.sep )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps" +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages"+os.sep+"splunk"+os.sep )
        sys.stdin.close()

    def test1(self) :
        from utils import createWorkingLog
        from get_versions import getVersions

        # getVersions(log, asCSV, verbose)
        log = createWorkingLog()
        ret = getVersions(log, False, True)
        self.assertTrue( type(ret) == type([]), "Have an array of results"  )
        for i in ret:
            self.assertTrue( type(i) == type({}), "Have a dict for each version "+str(i)  )
            self.assertTrue( 'version' in i, "Have a version in dict "+str(i) )
            self.assertTrue( i['version'] > '2', "this is not py1" )
            self.assertTrue( i['version'] < '4', "this is not py4 as doesn't exist" )


if( __name__=='__main__'):
    unittest.main()    

