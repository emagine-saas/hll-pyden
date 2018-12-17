# Overview 
The goal of this application is to provide full python functionality to Splunk. Currently the python distribution built 
in to Splunk runs on a version 2.7.x depending on the Splunk version. Additionally, there are significant core modules
that are excluded in this distribution. This add will allow developers to create python virtual environments and pick
the python version and modules to install to the environment. This includes core distributions of the interpreter in
multiple 2.7.x and 3.x versions, as well as the use of pip for the installation of additional modules within a virtual 
environment.
