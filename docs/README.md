# Overview 
The goal of this application is to provide full Python functionality to Splunk. Currently, the Python distribution built in to Splunk runs on a version 2.7.x depending on the Splunk version. Additionally, there are significant core modules that are excluded in this distribution. This suite of apps will allow developers to create Python virtual environments and pick the Python version and modules installed to the environment. This includes core distributions of the interpreter in multiple 2.7.x and 3.5+ versions, as well as the use of pip for the installation of additional modules within a virtual environment.

# Architecture
PyDen is broken into two separate Splunk apps called: PyDen and PyDen Manager. The PyDen Manager app contains all the functionality needed for a user to download, compile, and build Python distributions and virtual environments, as well as the ability to use pip to install packages to those environments. The actual CPython builds and environments are placed in the PyDen app. The location of the PyDen app can vary depending on the Splunk architecture. 

For a single search head environment the PyDen app can be placed along side the PyDen Manager in the Splunk apps directory. 

In a deployment with multiple search heads, PyDen can be placed onto the deployment server repository location. 

In a deployment utilizing search head clustering, it can be placed into the deployer's shcluster/apps directory. 

In all of these scenarios, PyDen Mnagaer must be installed to the same host as PyDen. The `pyden.conf` configuration file inside of the PyDen Manager app contains a stanza called `app` which has a `location` attribute which should specific the absolute path of the PyDen app. 

# Compatibility
The PyDen suite of apps has been tested for compatibility with Splunk 7.2. Use with other version of Splunk are considered experimental and should be tested thoroughly. 

# Requirements
The app builds CPython from source and therefore the success of the build is highly dependent on the operating system libraries available. The host OS must have a compiler and the packages needed in order to build Python from source. Please refer to the documentation for your OS for needed packages. Two options are included in the ./configure command during the Python build process: `--enable-optimizations` (if configured) and `--with-ensurepip=install`.

# Installation and Configuration
Installation of the PyDen Manager follows the same process as any other Splunk app. Please refer to Splunk's [documentation](https://docs.splunk.com/Documentation/Splunk/7.2.3/Admin/Deployappsandadd-ons) on the subject. The PyDen app installation process will vary depending on the Splunk deployment architecture. Please see the [Architecture](#Architecture) section for details on where to install PyDen. If PyDen is installed to any location other than the Splunk apps directory, the installation process will consist of extracting the app from the gzipped tarball and placing it in the specified directory on the host.

Both PyDen and PyDen Manager need to be installed on the same host. After both apps are installed, the PyDen Manager needs to be configured through the `pyden.conf` file. This file contains two stanzas: `download` and `app`. The `download` stanza has a single attribute called `url` which is used to specify the location from where Python is downloaded. It is not recommended to change this location except in the need to app proxy information. If a location other than [www.python.org](https://www.python.org) there will be significant gaps in the functionality of the dashboards. The `app` stanza contains two attributes `optimize` and `location`. The `location` attribute is the absolute path of the location of the PyDen app and the `optimize` attribute is a boolean which indicates whether or not Python will be built using the `--enable-optimizations` parameter. Enabling optimizations will provide significant speed improvements but takes significantly longer to build. 

# Custom Commands
There are three primary custom commands that make up the core functionality of PyDen: `createdist`, `createvenv`, and `pip`. There are additional suplemental commands that primarily aid in working with the dashboards.

## Createdist
The `createdist` command is how PyDen downloads and builds a CPython distribution. This command contains two keyword arguments `version` and `download`. The `version` argument is simply the version number of the Python installation to be built. The `download` argument is optional and only used if not doing an automatic download from [www.python.org](https://www.python.org). Instead of being downloaded, the Python source package can be placed inside the PyDen Manager's bin/build directory. When done this way, the `download` argument should provide the name of the package to be used. Package must be a file of `.tgz` format.

Examples:

*Download and install version 3.7.2 from www.python.org*
```
| createdist version=3.7.2
```

*Install 3.7.2 version of Python from source package called mypython.tgz*
```
| createdict version=3.7.2 download=mypython.tgz
```

## Createvenv
The `createvenv` command creates a Python virtual environment. 