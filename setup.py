from setuptools import setup

from argosd import settings
from argosd.commands import ArgosInstallCommand


config = {
    'name': 'argosd',
    'description': ('Daemon for Argos, a Python project '
                    'to keep track of TV shows from an RSS feed.'),
    'author': 'Daniel Koster',
    'url': 'https://github.com/danielkoster/argosd',
    'version': '0.1.0',
    'data_files': [
        (settings.LOG_PATH, []),
        ('/etc/systemd/system/', ['install/argosd.service']),
    ],
    'cmdclass': {
        'install': ArgosInstallCommand,
    },
}

setup(**config)
