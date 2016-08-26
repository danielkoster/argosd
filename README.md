# ArgosD
Daemon for Argos, a Python project to keep track of series on IPTorrents.

## Requirements
- Account on IPTorrents
- Python 3.2+
- System using systemd

## Installation
- Create an "argosd" user and group on your system, run all following steps as this user
- Clone this repository in /opt/argosd/
- Create and activate a virtualenv in /opt/argosd/.virtualenv/
- Copy argosd/settings_local_template.py to argosd/settings_local.py and fill it with required data
- Run `pip install -r requirements.txt`
- Run `python setup.py install` (as root)

This adds a systemd service named "argosd" to your system
and creates /var/log/argosd/ where logfiles are stored.
You can start it manually with `systemctl start argosd`.

## Running unit tests
To run unit tests first install testing dependencies with `pip install -r requirements-test.txt`.
After this, run `nosetests` to start testing.
