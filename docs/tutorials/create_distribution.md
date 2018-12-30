# Creating a CPython distribution with PyDen
## Requirements
PyDen creates CPython distributions by downloading the source code from [www.python.org](https://www.python.org) and compiling it. Therefore the host that the PyDen app is installed to must have the libraries needed for Python compilation. 

## Dashboard installation
The easiest way to make a Python version available for use with creating virtual environments is to use the `Python Versions` dashboard in PyDen Manager. After navigating to the dashboard the user is presented with a Splunk table visualization with a set of rows which contain a version number and an icon. The icon presented indicates whether the version has been installed or not. 

The green icon ![icon-plus-circle](../media/version_not_installed.png) indicates the version has not been installed to the PyDen app. The red icon ![icon-minus-circle](../media/version_installed.png) indicates the version has been installed. By clicking the icon, you can either install or delete the version depending on its status.