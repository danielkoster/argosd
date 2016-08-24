# ArgosD
Daemon for Argos, a Python project to keep track of series on IPTorrents.

## Requirements
- Python 3.2+

## Installation
- Clone this repository
- Create and activate a virtualenv
- Create a "argosd" user and group on your system
- Run `pip install -r requirements.txt`
- Run `python setup.py install`

This adds a systemd service named "argosd" to your system.

## Running unit tests
To run unit tests first install testing dependencies with `pip install -r requirements-test.txt`.
After this, run `nosetests` to start testing.
