
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
import shutil
if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yourself to support other non-server OS \n")
    sys.exit(1)

def whine(op, fn, excInfo):
    """
If onerror is provided, it must be a callable that accepts three parameters: 
   function, path, and excinfo. 
     The first parameter, function, is the function which raised the exception; it will be os.path.islink(), os.listdir(), os.remove() or os.rmdir(). 
     The second parameter, path, will be the path name passed to function. 
     The third parameter, excinfo, will be the exception information return by sys.exc_info(). 

Exceptions raised by onerror will not be caught.
"""
    print("FS Delete cmd failed on "+str(fn)+" saying "+str(excInfo))



class pyDeleteTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden-manager"+os.sep+"bin"+os.sep )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps" +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages"+os.sep+"splunk"+os.sep )
        sys.stdin.close()

    def tearDown(self):
        if os.path.isdir( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.1"):
            shutil.rmtree(  ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.1", False, whine )
            

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

