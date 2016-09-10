# ArgosD
[![Build Status](https://travis-ci.org/danielkoster/argosd.svg?branch=master)](https://travis-ci.org/danielkoster/argosd)

Daemon for Argos, a Python project to keep track of TV shows from an RSS feed.
This project is intended to be run on a Raspberry Pi, but should work on any
other system meeting the requirements.

After starting, a RESTful API is available on port 27467. This can be used
to update which TV shows you would like to keep track of, and to list the episodes
that have been downloaded. This API requires Basic Auth, the username is `argosd`
and you can choose your own password in the settings_local file.

## Requirements
- Python 3.4+
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

## Troubleshooting
If any issues occur, check /var/log/argosd/argosd.log for information.
For example, if you forget to enter a RSS_FEED in the settings, an error will be logged.

## Running unit tests
To run unit tests first install testing dependencies with `pip install -r requirements-test.txt`.
After this, run `nosetests` to start testing.

## Disclaimer
Downloading copyrighted content to which you do not own the rights might be illegal in your contry.
The author of this project is **not** responsible for your use of it.
