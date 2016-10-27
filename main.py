import logging
import multiprocessing

from argosd import argosd, settings


if __name__ == '__main__':
    # Spawn fresh processes, without inheriting resources
    multiprocessing.set_start_method('spawn')

    logformat = '[%(asctime)s] [%(thread)d] [%(levelname)s] %(message)s'
    loglevel = logging.DEBUG if settings.DEBUG else logging.INFO
    logfile = '{}/argosd.log'.format(settings.LOG_PATH)

    logging.basicConfig(format=logformat, level=loglevel,
                        filename=logfile, filemode='a')

    # Don't let schedule's logger write to our logfile,
    # schedule logs an info-event for each action.
    logger = logging.getLogger('schedule')
    logger.propagate = False

    argosd = argosd.ArgosD()
    argosd.run()
