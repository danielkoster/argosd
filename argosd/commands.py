import os
import stat
from pwd import getpwnam
from setuptools.command.install import install

from argosd import settings


class ArgosInstallCommand(install):
    """Custom setup.py install command."""

    def run(self):
        """Runs the default installer and sets rights on log directory."""
        install.run(self)

        # Make argosd user owned of log directory
        uid = getpwnam('argosd').pw_uid
        gid = getpwnam('argosd').pw_gid
        os.chown(settings.LOG_PATH, uid, gid)

        # User has full access, others can read
        mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
            stat.S_IRGRP | stat.S_IROTH
        os.chmod(settings.LOG_PATH, mode)
