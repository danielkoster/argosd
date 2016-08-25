import logging

from argosd import argosd, settings


logformat = '[%(asctime)s] [%(levelname)s] %(message)s'
loglevel = logging.DEBUG if settings.DEBUG else logging.INFO
logfile = '/var/log/argosd/argosd.log'

logging.basicConfig(format=logformat, level=loglevel,
                    filename=logfile, filemode='a')

logging.info('ArgosD starting')

argosd = argosd.ArgosD()
argosd.run()
