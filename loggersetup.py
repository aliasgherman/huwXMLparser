import logging
from logging.handlers import RotatingFileHandler


class LoggerSetup:
    '''
    This class sets up the Logger for the project. Ideally, no Print statements should be in the code so that automatic
    scripts can run in the background and logs can be generated in a file. Also a logging channel for stdout is created
    for runtime printing of the information/debug messages.
    '''

    def __init__(self, TAG, MAX_FILE_SIZE, BACKUP_COUNT, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL):
        '''
        Initialization of the logging class.
        :param TAG: TAG to appear in every logged message line. Any custom string
        :param MAX_FILE_SIZE: After this file size (in bytes) the log file will be rotated and previous file be backedup
        :param BACKUP_COUNT: Number of previous logfiles to backup after the size limit is reached on the logs
        :param FILE_LOG_LEVEL: The log level to be logged in the file (Like logging.NOTSET, logging.DEBUG, logging.INFO,
                logging.WARNING, logging.ERROR, logging.CRITICAL)
        :param CONSOLE_LOG_LEVEL:The log level to be logged in the stdout (Like logging.NOTSET, logging.DEBUG,
                logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
        '''
        self.TAG = TAG
        self.MAX_FILE_SIZE = MAX_FILE_SIZE
        self.BACKUP_COUNT = BACKUP_COUNT
        self.FILE_LOG_LEVEL = FILE_LOG_LEVEL
        self.CONSOLE_LOG_LEVEL = CONSOLE_LOG_LEVEL

    def run(self):
        '''
        Just sets up the logger and returns the logger instance which was setup with the init function.

        :return: logger instance
        '''
        LOG_TAG = 'HUW_XML_PARSER'
        self.myLogger = logging.getLogger(self.TAG)
        self.myLogger.setLevel(logging.DEBUG)
        self.fh = RotatingFileHandler(self.TAG + ".log", 'a', maxBytes=self.MAX_FILE_SIZE,
                                      backupCount=self.BACKUP_COUNT)
        self.fh.setLevel(self.FILE_LOG_LEVEL)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.CONSOLE_LOG_LEVEL)
        formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)
        self.myLogger.addHandler(self.ch)
        self.myLogger.addHandler(self.fh)
        return self.myLogger

    def close(self):
        try:
            self.fh.close()
            self.ch.close()
        except Exception as e:
            self.myLogger.error("Error while trying to close logger. Maybe this will not be reported :)")
