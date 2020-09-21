
# vim: ts=4 expandtab nospell
# if you don't think that this uses python naming "properly"; this isn't my only language 
import os
import sys
import unittest
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
        from utils import get_proxies
        proxies = get_proxies(None)
# in this case this is expected to be {}, as nothing was supplied over the ENV
        self.assertTrue( proxies != False and proxies != None)

    def test2(self):
        from utils import get_proxies
        proxies = get_proxies(None)
        from get_packages import get_simple_index, get_package_description, getPackages
        ret=get_simple_index(proxies) 
              
        self.assertTrue( type(ret) == type(list())) 
        for ix in ret:
            self.assertTrue( type(ix) == type(dict())) 
            self.assertTrue( 'package' in ix )
            if not ix['package'][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ] :
                self.assertTrue( len(ix['package'])>=1, "Package name seems good "+ix['package']  )
            else:
                print("Whine, bad package name: "+ix['package'])          

    def test3(self):
        from utils import get_proxies
        proxies = get_proxies(None)
        from get_packages import get_simple_index, get_package_description, getPackages
        ret= get_package_description("numpy", proxies) 
              
        self.assertTrue( type(ret) == type(list()) )
        for ix in ret:
            self.assertTrue( type(ix) == type(dict())) 
            self.assertTrue( 'description' in ix, "there is a description at all" )
            self.assertTrue( len(ix['description'])>3, "the description has content"  )

    def test4(self):
        from utils import get_proxies
        proxies = get_proxies(None)
        from get_packages import get_simple_index, get_package_description, getPackages
        ret= getPackages(["", "numpy"], False) 
              
        self.assertTrue( type(ret) == type(list()) )
        for ix in ret:
            self.assertTrue( type(ix) == type(dict())) 
            self.assertTrue( 'description' in ix, "there is a description at all" )
            self.assertTrue( len(ix['description'])>3, "the description has content"  )

    def test5(self):
        from utils import get_proxies
        proxies = get_proxies(None)
        from get_packages import get_simple_index, get_package_description, getPackages
        ret= getPackages(["", "pypi_simple_index"], False) 
              
        self.assertTrue( type(ret) == type(list()) )
        for ix in ret:
            self.assertTrue( type(ix) == type(dict())) 
            self.assertTrue( 'package' in ix )
            if not ix['package'][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ] :
                self.assertTrue( len(ix['package'])>=1, "package name has content  "+ix['package'] )
            else:
                print("Whine, bad package name: "+ix['package']) 


if( __name__=='__main__'):
    unittest.main()    

