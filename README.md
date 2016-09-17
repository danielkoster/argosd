# ArgosD
[![Build Status](https://travis-ci.org/danielkoster/argosd.svg?branch=master)](https://travis-ci.org/danielkoster/argosd)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b114513c09d042f68e07b6f52c4e029a)](https://www.codacy.com/app/daniel_28/argosd)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/b114513c09d042f68e07b6f52c4e029a)](https://www.codacy.com/app/daniel_28/argosd)

Daemon for Argos, a Python project to keep track of TV shows from an RSS feed.
This project is intended to be run on a Raspberry Pi, but should work on any
other system meeting the requirements.

After starting, a RESTful API is available on port 27467. You can find how to use
this API in the [API documentation](docs/api.md).

## Requirements
- Python 3.4+
- System using systemd

## Installation
See the [installation instructions](docs/installation.md)
for a step-by-step guide to install this application.
This adds a systemd service named "argosd" to your system
and creates /var/log/argosd/ where logfiles are stored.
You can start it manually with `systemctl start argosd`.

## Troubleshooting
If any issues occur, check /var/log/argosd/argosd.log for information.
For example, if you forget to enter the URL of your RSS feed in the settings file,
an error will be logged.

## Running unit tests
To run unit tests first install testing dependencies with `pip install -r requirements-test.txt`.
After this, run `nosetests tests` to start testing.

## Disclaimer
Downloading copyrighted content to which you do not own the rights might be illegal in your country.
The author of this project is **not** responsible for your use of it.
