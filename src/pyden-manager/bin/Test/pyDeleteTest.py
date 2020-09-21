
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
from utils import createWorkingLog, load_pyden_config
if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yourself to support other non-server OS \n")
    sys.exit(1)

class pyDeleteTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append('/opt/splunk/etc/apps/pyden-manager/bin/')
        sys.path.append('/opt/splunk/etc/apps' +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( '/opt/splunk/lib/python3.7/site-packages')
        sys.path.append( '/opt/splunk/lib/python3.7/site-packages/splunk/')
        sys.stdin.close()

    def test1(self):    
        fakeArgs=[ "scriptname", "2.7.20" ]
        log=createWorkingLog()
        pm_config, config = load_pyden_config()
        values=setup(log, fakeArgs, pm_config, config )
        self.assertTrue(values['exit']!=0, "Expected fail outcome "+values['exit'] )

        fakeArgs=[ "scriptname", "3.5.1" ] 
        self.assertTrue(values['exit']==0, "Expected fail outcome "+values['exit'] )

    def test2(self):    
        import create_dist 
        log=createWorkingLog()
        fakeArgs=['scriptname', 'version=3.5.1']
        ret=createDist(log, fakeArgs, False )
        self.assertTrue(ret==0, "Failed to install; to be able to delete "+ret )
        
        pm_config, config = load_pyden_config()
        values=setup(log, fakeArgs, pm_config, config )
        self.assertTrue(values['exit']==0, "Expected fail outcome "+values['exit'] )
        
        ret=pyDelete(log, values, config)
        self.assertTrue(ret==0, "Expected fail outcome "+ret )
    

if( __name__=='__main__'):
    unittest.main()    

