from activate import activate_venv_or_die
activate_venv_or_die('py3')
import sys, os, socket


def log(msg):
    with open(os.path.join("/opt/splunk", "var", "log", "splunk", "test_modalert.log"), "a") as f:
        f.write("Script run on {} using {} with {} at {}\n".format(socket.gethostname(), sys.executable, sys.version, os.getcwd()))


log("got arguments %s" % sys.argv)
log("got payload: %s" % sys.stdin.read())
