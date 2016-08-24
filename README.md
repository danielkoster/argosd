# ArgosD
Daemon for Argos, a Python project to keep track of series on IPTorrents.

## Requirements
- Python 3.2+

## Installation
- Clone this repository
- Create and activate a virtualenv
- Create an "argosd" user and group on your system
- Copy argosd/settings_local_template.py to argosd/settings_local.py and fill it with required data
- Run `pip install -r requirements.txt`
- Run `python setup.py install`

This adds a systemd service named "argosd" to your system.
You can start it manually with `systemctl start argosd`.

## Running unit tests
To run unit tests first install testing dependencies with `pip install -r requirements-test.txt`.
After this, run `nosetests` to start testing.
