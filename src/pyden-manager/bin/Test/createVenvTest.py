
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
import shutil
if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yours self to support other non-server OS \n")
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


class createDistTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden-manager"+os.sep+"bin"+os.sep )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps" +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages"+os.sep+"splunk"+os.sep )
        sys.stdin.close()

    def tearDown(self):
#        ret=createDist(log, ["scriptname", "version=3.5.4", "--no-block"], True)
#        cmd='"+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"venv"+os.sep+"timesuite"+os.sep+"bin"+os.sep+"pip3'
        if os.path.isdir( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.4"):
            shutil.rmtree( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.4", False, whine )
        print("pls tidyup config file "+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"pyden.conf")

    def test1(self) :
        from utils import createWorkingLog
        from create_venv import pydenFork, getBtoolConfig, setup, createVenv

        ret=getBtoolConfig()
 # im surprised that func execs without crashing....       
        self.assertTrue(type(ret)==type(" "), "Have a string; not a byte array")
        self.assertTrue(len(ret) >10, "Have a string with data "+ret)

    def test2(self) :
        from utils import createWorkingLog
        from create_venv import pydenFork, getBtoolConfig, setup, createVenv
        from create_dist import createDist 
        log=createWorkingLog()

        stat, msg, where, whom, whence =setup(log, ["scriptname", "version=3.5.4", "name=pyjamas" ]) 
        self.assertTrue( type(stat) == type(1), "Stat is an int "+str(stat))
        self.assertTrue( stat == 4, "Stat is a good int "+str(stat))

        self.assertTrue( type(msg) == type(" "), "Msg is an string "+str(stat)+" "+str(msg))
        self.assertTrue( len(msg) >3, "msg has data "+str(stat)+" "+str(msg))
                
    def test3(self) :
        from utils import createWorkingLog
        from create_venv import pydenFork, getBtoolConfig, setup, createVenv
        from create_dist import createDist 
        log=createWorkingLog()

        ret=createDist(log, ["scriptname", "version=3.5.4", "--no-block"], True)
        self.assertTrue( ret==0, "createDist worked "+str(ret))

        stat, msg, where, whom, whence =setup(log, ["scriptname", "version=3.5.4", "name=pyjamas" ]) 
        self.assertTrue( type(stat) == type(1), "Stat is an int "+str(stat))
        self.assertTrue( stat == 0, "Stat is a good int "+str(stat))

        self.assertTrue( type(msg) == type(" "), "Msg is an string "+str(stat)+" "+str(msg))
        self.assertTrue( len(msg) >3, "msg has data "+str(stat)+" "+str(msg))

        ret=createVenv(log, msg, where, whom, whence)
        self.assertTrue( type(ret) == type(1), "Key is an int "+str(ret))
        self.assertTrue( ret == 0, "Key is an int "+str(ret))
 
if( __name__=='__main__'):
    unittest.main()    

