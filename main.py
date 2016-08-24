from argosd import argosd, settings
import logging

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

logfile_handler = logging.FileHandler('/var/log/argosd/argosd.log', 'w')
logfile_handler.setLevel(logging.DEBUG)
logfile_handler.setFormatter(formatter)

logger = logging.getLogger('argosd')

loglevel = logging.DEBUG if settings.DEBUG else logging.INFO
logger.setLevel(loglevel)
logger.addHandler(logfile_handler)

logger.info('ArgosD starting')

argosd = argosd.ArgosD()
argosd.run()
