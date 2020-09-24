
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
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
        from utils import createWorkingLog, load_pyden_config
        from pyden_delete import  setup, pyDelete

        fakeArgs=[ "bin/pyden_delete.py", "2.7.20" ]
        log=createWorkingLog()
        pm_config, config = load_pyden_config()
        values=setup(log, fakeArgs, pm_config, config )
        self.assertTrue(values['exit']!=0, "Expected fail outcome "+str(values['exit']) )

        fakeArgs=[ "bin/pyden_delete.py", "3.5.1" ] 
        self.assertTrue(values['exit']!=0, "Expected fail outcome "+str(values['exit']) )

    def test2(self):    
        from utils import createWorkingLog, load_pyden_config
        from pyden_delete import  setup, pyDelete
        from create_dist import createDist
        log=createWorkingLog()
        fakeArgs=['bin/pyden_delete.py', 'version=3.5.1', '--no-block']
        ret=createDist(log, fakeArgs, False )
        self.assertTrue(ret==0, "Failed to install; to be able to delete "+str(ret) )
        
        fakeArgs=["scriptname", "3.5.1"] 
        pm_config, config = load_pyden_config()
        values=setup(log, fakeArgs, pm_config, config )
        self.assertTrue(values['exit']==0, "Expected fail outcome "+str(values['exit'] ))
        
        ret=pyDelete(log, values, config)
        self.assertTrue(ret==0, "Expected fail outcome "+str(ret ))
    

if( __name__=='__main__'):
    unittest.main()    

