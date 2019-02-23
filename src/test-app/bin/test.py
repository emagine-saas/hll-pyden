import activate_default
import sys

sys.stdout.write("messages\n")
sys.stdout.flush()

try:
    # there's no particular reason to use this module, any selection works for testing
    # module should fail to import right after creation of virtual environment, but should succeed after running
    # | pip install requests from the Pyden Manager app (and deploying PyDen to search head)
    import requests
except:
    sys.stdout.write("Failed to import module\n")
else:
    sys.stdout.write("Module imported from: %s" % requests.__file__)
