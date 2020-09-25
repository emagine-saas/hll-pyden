
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yours self to support other non-server OS \n")
    sys.exit(1)

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
        if os.path.isdir( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"venv"+os.sep+"pyjamas"):
            shutil.rmtree( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"venv"+os.sep+"pyjamas", False, whine )
        if os.path.isdir( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.2"):
            shutil.rmtree( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.2", False, whine )
        if os.path.isdir( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.3"):
            shutil.rmtree( ""+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"dist"+os.sep+"3.5.3", False, whine )
        print("pls tidyup config file "+os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"pyden.conf")

    def test1(self) :
        from utils import createWorkingLog
        from create_dist import download_python, build_dist, createDist

        ret=download_python('3.5.1', os.path.join(os.getcwd(), 'build'), {}, False, None) 
        self.assertTrue(type(ret) == type(" "), "Downloading python returned a posive outcome")
        self.assertTrue(len(ret) >4, "Downloading python returned a posive outcome "+str(len(ret)))
        
        ret=download_python('3.5.1', os.path.join(os.getcwd(), 'build'), {}, False, None) 
        self.assertTrue(type(ret) == type(" "), "Try to duplicate download "+ret)
        self.assertTrue(len(ret) >4, "dup Download python returned a posive outcome "+str(len(ret)))

    def test2(self) :
        from utils import createWorkingLog
        from create_dist import download_python, build_dist, createDist

        log =  createWorkingLog()
        ret=build_dist('3.5.2', True, log, {}, False, None)
        self.assertTrue(type(ret) == type(1), "Build dist didn't error "+str(ret))
        self.assertTrue( ret == 0, "Build dist didn't error "+str(ret))
        
    def test3(self) :
        from utils import createWorkingLog
        from create_dist import download_python, build_dist, createDist

        log =  createWorkingLog()
        ret=createDist(log, ["scriptname", "version=3.5.3", "--no-block"], True)
        self.assertTrue(type(ret) == type(1), "Build dist didn't error "+str(ret))
        self.assertTrue( ret == 0, "Build dist didn't error "+str(ret))
        

if( __name__=='__main__'):
    unittest.main()    

