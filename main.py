from argosd import argosd
import logging

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

logfile_handler = logging.FileHandler('/var/log/argosd/argosd.log', 'w')
logfile_handler.setLevel(logging.DEBUG)
logfile_handler.setFormatter(formatter)

logger = logging.getLogger('argosd')
logger.setLevel(logging.DEBUG)
logger.addHandler(logfile_handler)

logger.info('ArgosD starting')

argosd = argosd.ArgosD()
argosd.run()
