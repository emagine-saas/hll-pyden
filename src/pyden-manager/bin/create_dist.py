import sys
import os
import tarfile
import json
import subprocess
from splunk.rest import simpleRequest
from splunk import Intersplunk
import requests
import re
import shutil
from utils import load_pyden_config, write_pyden_config, get_proxies, createWorkingLog


def download_python(version, build_path):
    base_url = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/download/url",
                             sessionKey=session_key)[1]
    try:
        if sys.version_info[0] >2:
            base_url=str(base_url, 'utf-8')
        else:
            base_url=unicode(base_url )

        dpr = requests.get(base_url + "{0}/".format(str(version)), proxies=proxies)
    except Exception as ex:
        Intersplunk.generateErrorResults("Exception thrown getting python: ({0}, {1})".format(type(ex), ex))
        sys.exit(3)
    else:
        if dpr.status_code in range(200, 300):
            if sys.version_info[0] >2:
                tt=str(dpr.content, 'utf-8')
            else:
                tt=unicode(dpr.content )

            tt=re.findall("href=\"(.*?)\"", tt)
				# statements split up so I could check types
            python_link=False
            for python_link in tt:
                if python_link.endswith('tgz'):
                    break
#            python_link = [link for link in re.findall("href=\"(.*?)\"", dpr.content) if link.endswith('tgz')][0]
            dpr = requests.get(base_url + "{0}/{1}".format(version, python_link), proxies=proxies)
        else:
            if sys.version_info[0] >2:
                Intersplunk.generateErrorResults(
                "Failed to reach www.python.org. Request returned - Status code: {0}, Response: {1}".format(
                   str(dpr.content, 'utf-8'), str(dpr.content, 'utf-8')))
            else:
                Intersplunk.generateErrorResults(
                "Failed to reach www.python.org. Request returned - Status code: {0}, Response: {1}".format(
                   unicode(dpr.content ), unicode(dpr.content )))
           sys.exit(4)

    if dpr.status_code in range(200, 300):
        # save
        build_file = os.path.join(build_path, "Python-{0}.tgz".format(str(version)))
        with open(build_file, "wb") as download:
            download.write(dpr.content)
    else:
        Intersplunk.generateErrorResults(
            "Failed to download python. Request returned - Status code: {0}, Response: {1}".format(str(dpr.status_code),
                                              str(dpr.text)))
        sys.exit(5)
    return build_file


def build_dist(version, download, log):
    pm_config, config = load_pyden_config()
    pyden_location = pm_config.get('appsettings', 'location')
    if version in config.sections():
        log.warning("Requested to install version of python already present "+version)
        Intersplunk.generateErrorResults("Version already exists.")
        sys.exit(6)
    build_path = os.path.join(os.getcwd(), 'build')
    if not os.path.isdir(build_path):
        os.mkdir(build_path)
    if download is True:
        log.debug("Downloading Python")
        build_file = download_python(version, build_path)
    else:
        log.debug("Using existing source archive"+download)
        build_file = os.path.join(build_path, download)

    # unpack
    if os.path.isdir(build_file[:-4]):
        shutil.rmtree(build_file[:-4], ignore_errors=True)
    os.chdir(build_path)
    list_before_extraction = os.listdir(os.getcwd())
    log.debug("Extracting archive "+build_file)
    with tarfile.open(build_file, "r:gz") as tarball:
        tarball.extractall()
    list_after_extraction = os.listdir(os.getcwd())
    extracted_members = [member for member in list_after_extraction if member not in list_before_extraction]
    if len(extracted_members) == 1:
        extracted_member = extracted_members[0]
    else:
        log.error("Source archive is malformed (multiple project roots?)")
        Intersplunk.generateErrorResults("Aborting: Python source archive contained more than one project root. ")
        sys.exit(7)

    # configure and build
    pyden_prefix = os.path.join(pyden_location, 'local', 'lib', 'dist', version)
    if not os.path.isdir(pyden_prefix):
        os.makedirs(pyden_prefix)
    os.chdir(os.path.join(os.getcwd(), extracted_member))
    optimize_conf = simpleRequest("/servicesNS/nobody/pyden-manager/properties/pyden/appsettings/optimize",
                                  sessionKey=session_key)[1]
    optimize = '--enable-optimizations' if optimize_conf in ['true', 'True', '1', 1] else ''
    # remove environment variables. needed to use host libraries instead of splunk's built-in.
    del os.environ['LD_LIBRARY_PATH']
    del os.environ['OPENSSL_CONF']
    if 'PYTHONPATH' in os.environ:
        del os.environ['PYTHONPATH']
    log.debug("Configuring source "+os.path.join(os.curdir, 'configure'))
    configure = subprocess.Popen([os.path.join(os.curdir, 'configure'),
                                  optimize,
                                  '--with-ensurepip=install',
                                  '--prefix={0}'.format(pyden_prefix)],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True, env=os.environ)
    result, error = configure.communicate()
    for message in result.split('\n'):
        if message:
            log.info("Configure results:" +message)
    for message in error.split('\n'):
        if message:
            log.error("Configure results:" +message)
    if configure.returncode != 0:
        log.error("Configure returned exit code "+str(configure.returncode))
        Intersplunk.generateErrorResults("Configure returned "+str(make.returncode )+", aborting.")

        sys.exit(8)
    log.debug("Making new python")
    make = subprocess.Popen(['make', '-j', '8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                            env=os.environ)
    result, error = make.communicate()
    for message in result.split('\n'):
        if message:
            log.info("Make command said:  "+message)
    for message in error.split('\n'):
        if message:
            log.error("Make command said:  "+message)
    if make.returncode != 0:
        log.error("Make returned exit code "+str(make.returncode))
        Intersplunk.generateErrorResults("Make returned "+str(make.returncode )+", aborting.")
        sys.exit(9)
    log.debug("Running make install ")
    install = subprocess.Popen(['make', 'altinstall'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True, env=os.environ)
    result, error = install.communicate()
    for message in result.split('\n'):
        if message:
            log.info("Make said: "+message)
    for message in error.split('\n'):
        if message:
            log.error("Make said: "+message)
    if install.returncode != 0:
        log.error("Install returned exit code "+str(install.returncode))
        Intersplunk.generateErrorResults("Install step returned "+str(install.returncode )+", aborting.")
        sys.exit(10)
    log.debug("Determining binary of " + str(pyden_prefix))
    bin_dir = os.path.join(pyden_prefix, 'bin')
    os.chdir(bin_dir)
    largest_size = 0
    py_exec = ""
    bins = os.listdir(bin_dir)
    for binary in bins:
        bin_size = os.path.getsize(binary)
        if bin_size > largest_size:
            py_exec = os.path.join(bin_dir, binary)
            largest_size = bin_size
    log.debug("Found python binary (will deploy pip next): "+str( py_exec))

    # Running get-pip and others
    if proxies:
        os.environ['HTTP_PROXY'] = proxies['http']
        os.environ['HTTPS_PROXY'] = proxies['https']
    pip = subprocess.Popen([py_exec, '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=os.environ)
    result, error = pip.communicate()
    for message in result.split('\n'):
        if message:
            log.info("install pip said "+message)
    for message in error.split('\n'):
        if message:
            log.error("install pip said "+message)
    if pip.returncode != 0:
        log.error("pip install returned exit code "+str(pip.returncode))
        Intersplunk.generateErrorResults("pip Install step returned "+str(pip.returncode )+", aborting.")
        sys.exit(11)
 
    pip = subprocess.Popen([py_exec, '-m', 'pip', 'install', 'virtualenv'], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True, env=os.environ)
    result, error = pip.communicate()
    for message in result.split('\n'):
        if message:
            log.info("install venv said: "+message)
    for message in error.split('\n'):
        if message:
            log.error("install venv said: "+message)
    if pip.returncode != 0:
        log.error("pip install returned exit code "+str(pip.returncode))
        Intersplunk.generateErrorResults("pip Install step returned "+str(pip.returncode )+", aborting.")
        sys.exit(12)
 
    log.info("Finished building Python {}. Distribution available at {}.".format(version, pyden_prefix))

    write_pyden_config(pyden_location, config, version, "executable", py_exec.lstrip(os.environ['SPLUNK_HOME']))
    if not config.has_section("default-pys") or not config.has_option("default-pys", "distribution"):
        write_pyden_config(pyden_location, config, 'default-pys', 'distribution', version)
    return


if __name__ == "__main__":
    log = createWorkingLog()
    download_arg = True
    settings = dict()
    if "--cli" in sys.argv:
        session_key = sys.stdin.read()
    else:
        Intersplunk.readResults(settings=settings)
        session_key = settings['sessionKey']
    proxies = get_proxies(session_key)
    latest_python_search = r"""
    | getversions 
    | rex field=version "(?<v_M>\d+)\.(?<v_m>\d+)\.(?<v_mm>\d+)" 
    | eval v_M=tonumber(v_M), v_m=tonumber(v_m), v_mm=tonumber(v_mm) 
    | sort -v_M, -v_m, -v_mm 
    | table version 
    | head 1
    """
    try:
        r = simpleRequest("/servicesNS/nobody/pyden-manager/search/jobs",
                          postargs={'search': latest_python_search, 'exec_mode': 'oneshot', 'output_mode': 'json'},
                          sessionKey=session_key)
        dist_version = json.loads(r[1])['results'][0]['version']
        log.debug("Found current python version "+dist_version)
    except Exception as e:
        log.error("Failed to find latest version of Python: " +str( e))
        Intersplunk.generateErrorResults("Failed to find latest version of Python: " +str( e))
        sys.exit(2)


    for arg in sys.argv:
        if "version" in arg:
            dist_version = str(arg.split("=")[1])
        if "download" in arg:
            download_arg = str(arg.split("=")[1])
    log.info("Creating Python distribution version" +str( dist_version))
    build_dist(dist_version, download_arg, log)
