import sys
import subprocess
from splunk import Intersplunk
from splunk_logger import setup_logging
from utils import load_pyden_config


if __name__ == "__main__":
    logger = setup_logging()
    logger.debug(sys.argv)
    settings = dict()
    Intersplunk.readResults(settings=settings)
    session_key = settings['sessionKey']
    pyden_location, config = load_pyden_config(session_key)
    env = False
    pip_arg_index = 1
    if config.has_option('default', 'environment'):
        env = config.get('default', 'environment')
    for arg in sys.argv:
        if 'environment' in arg:
            env = arg.split('=')[1]
            pip_arg_index = 2
    if not env:
        Intersplunk.generateErrorResults("Missing required argument.")

    py_exec = config.get(env, 'executable')
    sys.stdout.write("messages\n")
    sys.stdout.flush()
    subprocess.call([py_exec, '-m', 'pip'] + sys.argv[pip_arg_index:])
