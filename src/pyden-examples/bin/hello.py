from activate import activate_venv_or_die
activate_venv_or_die('py2')
import sys
import socket
import os
import time


# Empty introspection routine
def do_scheme(): 
    pass


# Empty validation routine. This routine is optional.
def validate_arguments(): 
    pass


# Routine to index data
def run_script():
    index_time = "[" + time.strftime("%m/%d/%Y %H:%M:%S %p %Z", time.localtime()) + "]"
    try:
        import splunklib
    except ImportError:
        found_sdk = "false"
    else:
        found_sdk = "true"
    print("{} host:{} executable:{} version:{} cwd:{} foundSDK: {}".format(index_time, socket.gethostname(), sys.executable, sys.version, os.getcwd(), found_sdk))


# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            validate_arguments()
        else:
            pass
    else:
        run_script()
    sys.exit(0)
