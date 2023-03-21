import datetime
import logging
import multiprocessing


def gen_log(name='test'):
    # Set up logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    my_time = datetime.datetime.now()
    handler = logging.FileHandler(name + "." + str(my_time.year) + str(my_time.month) + str(my_time.day) +
                                  str(my_time.hour) + str(my_time.minute) + str(my_time.second) + ".log")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # FIXME platforms... Options...

    return logger


def error_logger(logger, error):
    logger.error(error)


def info_logger(logger, info):
    logger.info(info)