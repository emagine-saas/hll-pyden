
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest

if os.name != "posix":
    # see below paths...
    sys.stderr.write("Test is setup for a server OS, such as Redhat Linux; reconfig it yours self to support other non-server OS \n")
    sys.exit(1)

class pydenPipTest(unittest.TestCase) :
    def setUp(self):
        sys.path.append('/opt/splunk/etc/apps/pyden-manager/bin/')
        sys.path.append('/opt/splunk/etc/apps' +os.sep+"pyden"+os.sep+"local"+os.sep+ "lib"+os.sep+"venv"+os.sep+ "timesuite"+os.sep+"lib"+os.sep+"python3.7"+os.sep+"site-packages" )
        sys.path.append( '/opt/splunk/lib/python3.7/site-packages')
        sys.path.append( '/opt/splunk/lib/python3.7/site-packages/splunk/')
        sys.stdin.close()

    def test1(self): 
        from utils import createWorkingLog
        from pyden_pip import pydenPip

        # def pydenPip(log, asCSV, sysargs, verbose) ->int:
        log = createWorkingLog()
        fakeArgs=['bin/pyden_pip.py', 'install', 'reqererwer']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret >0, "Shouldn't be able to install made up package "+ret )

        fakeArgs=['bin/pyden_pip.py', 'install', 'requests']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret ==0, "Should be able to install acul package "+ret )

    def test2(self): 
        from utils import createWorkingLog
        from pyden_pip import pydenPip

        fakeArgs=['bin/pyden_pip.py', 'environment=TEST11111', 'install', 'requests']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret >0, "Shouldn't be able to install made up venv "+ret )

        fakeArgs=['bin/pyden_pip.py', 'environment=timesuite', 'install', 'requests']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret ==0, "Should be abe to install to real one "+ret )

        fakeArgs=['bin/pyden_pip.py', 'environment=timesuite', 'install', '--upgrade' 'pip']
        ret=pydenPip(log, False, fakeArgs, True)
        self.assertTrue( ret ==0, "Compound statement from manual that is probably used by all "+ret )


if( __name__=='__main__'):
    unittest.main()

