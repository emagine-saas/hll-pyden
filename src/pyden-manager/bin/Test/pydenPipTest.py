
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
import subprocess
import configparser

if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yours self to support other non-server OS \n")
    sys.exit(1)

class pydenPipTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append(os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden-manager"+os.sep+"bin"+os.sep )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps" +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages")
        sys.path.append( os.sep+"opt"+os.sep+"splunk"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages"+os.sep+"splunk"+os.sep )
        sys.stdin.close()

    def tearDown(self):
        # pip3 uninstall requests
        cmd= os.sep+"opt"+os.sep+"splunk"+os.sep+"etc"+os.sep+"apps"+os.sep+"pyden"+os.sep+"local"+os.sep+"lib"+os.sep+"venv"+os.sep+"timesuite"+os.sep+"bin"+os.sep+"pip3"
#        proc = subprocess.Popen([cmd, 'uninstall', 'requests' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = subprocess.check_output([cmd, 'uninstall', '--yes',  'requests' ], stderr=subprocess.STDOUT, timeout=10 )

#        proc_out, proc_err = proc.communicate()
##        print("XXX", proc_out.decode(),  proc_err.decode() )
        print("XXX", output.decode() )

    def test1(self): 
        from utils import createWorkingLog
        from pyden_pip import pydenPip

        # def pydenPip(log, asCSV, sysargs, verbose) ->int:
        log = createWorkingLog()
        fakeArgs=['bin/pyden_pip.py', 'install', 'reqererwer']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret >0, "Shouldn't be able to install made up package "+str(ret) )

        fakeArgs=['bin/pyden_pip.py', 'install', 'requests']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret ==0, "Should be able to install actual package "+str(ret) )

    def test2(self): 
        from utils import createWorkingLog
        from pyden_pip import pydenPip

        log = createWorkingLog()

        try:
             fakeArgs=['bin/pyden_pip.py', 'environment=TEST11111', 'install', 'requests']
             ret=pydenPip(log, False, fakeArgs, True)
             self.assertTrue( ret >0, "Shouldn't be able to install made up venv "+str(ret) )
        except configparser.NoSectionError as e:
            self.assertTrue( True, "Shouldn't be able to install made up venv "+str(e) )

        fakeArgs=['bin/pyden_pip.py', 'environment=timesuite', 'install', 'requests']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret ==0, "Should be be to install to real one "+str(ret) )

        fakeArgs=['bin/pyden_pip.py', 'environment=timesuite', 'install', '--upgrade', 'pip']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret ==0, "Compound statement from manual that is probably used by all "+str(ret) )


if( __name__=='__main__'):
    unittest.main()

