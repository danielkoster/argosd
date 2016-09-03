from distutils.core import setup
import os

config = {
    'name': 'argosd',
    'description': ('Daemon for Argos, a Python project '
                    'to keep track of TV shows from an RSS feed.'),
    'author': 'Daniel Koster',
    'url': 'https://github.com/danielkoster/argosd',
    'version': '0.1.0',
    'data_files': [
        ('/var/log/argosd', []),
        ('/etc/systemd/system/', ['install/argosd.service']),
    ],
}

setup(**config)

# Make log directory world writable (777)
os.chmod('/var/log/argosd', 0o777)
