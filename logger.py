import logging
import app_config


LOG_FILE_PATH = app_config.LOG_FILE_PATH
LOG_MODE = app_config.LOG_FILE_MODE
LOG_LEVEL = logging.DEBUG


def init_logger(*args):
    logFormatter = logging.Formatter('%(asctime)s - %(levelname)-12s - %(name)-20s - %(filename)-24s - %(lineno)-4d - %(message)s')
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(LOG_FILE_PATH, mode=LOG_MODE)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
