# Installation
This document describes how ArgosD should be installed, and walks you through the process.
Every command is prefixed with the name of the user it should be run as.

## Create a user
`root$ useradd argosd --system`  
Create an "argosd" user and group on your system.

## Create repository destination and grant ownership
`root$ mkdir /opt/argosd/`  
`root$ chown argosd:argosd /opt/argosd/`  
Most of the following commands should be run as this user, so you might want to switch to this user.  
`root$ sudo -Hsu argosd`

## Clone the repository
`argosd$ git clone https://github.com/danielkoster/argosd.git /opt/argosd/`  
Clone this repository in /opt/argosd/.

## Create and activate a virtual environment
`argosd$ virtualenv /opt/argosd/.virtualenv -p python3`  
`argosd$ source /opt/argosd/.virtualenv/bin/activate`  
Create and activate a python3 virtual environment. In here we can install all the required dependencies.

## Copy and fill settings file
`argosd$ cp /opt/argosd/argosd/settings_local_template.py /opt/argosd/argosd/settings_local.py`  
Copy the settings template and fill it with required data.

## Install dependencies
`argosd$ pip install -r /opt/argosd/requirements.txt`  
This installs all the required dependencies into the virtual environment.

## Install ArgosD
`root$ python3 /opt/argosd/setup.py install`  
This will create /var/log/argosd/. All the logfiles will be stored in this directory.
This also creates a systemd service called "argosd". You can interact with it through `systemctl`.

## Auto-start ArgosD
`root$ systemctl enable argosd`  
This will tell systemd we want to auto-start this daemon when our system is booted.
Whenever you reboot your system, ArgosD will automatically start running again.
