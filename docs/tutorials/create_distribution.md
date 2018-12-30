# Creating a CPython distribution with PyDen
## Requirements
PyDen creates CPython distributions by downloading the source code from [www.python.org](https://www.python.org) and compiling it. Therefore the host that the PyDen app is installed to must have the libraries needed for Python compilation. 

## Dashboard installation
The easiest way to make a Python version available for use with creating virtual environments is to use the `Python Versions` dashboard in PyDen Manager. After navigating to the dashboard the user is presented with a Splunk table visualization with a set of rows which contain a version number and an icon. The icon presented indicates whether the version has been installed or not. 

The green icon ![icon-plus-circle](../media/icon-plus-circle.png) indicates the version has not been installed to the PyDen app. The red icon ![icon-minus-circle](../media/icon-minus-circle.png) indicates the version has been installed. By clicking either icon, you can either install or delete the version depending on its status.

Once clicked the icon will turn to a spinning ![icon-rotate](../media/icon-rotate.png) icon. When finished the rotating icon converts back to either the plus or minus.

## Createdist command
While the dashboard installation should be sufficient for most use cases, there may be instances where the `createdist` command needs to be executed manually. The primary case for to is when the installation fails and the output of the command needs to be reviewed. In such a case, please review the README [Custom Commands](../README.md#custom-commands) sections.
