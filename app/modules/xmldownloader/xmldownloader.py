import os
from datetime import datetime
from stat import S_ISDIR, S_ISREG
import logging
from logging.handlers import RotatingFileHandler

import pysftp

temp = datetime.now()
DIRFILTER = "AUTOBAKDATA{:04d}{:02d}{:02d}".format(temp.year, temp.month, temp.day)
#print("Will look for directory with filter " + DIRFILTER)


class XMLDownloader:
    AUTOBAK = 1
    GEXPORT = 2
    NEEXPORT = 3

    def __init__(self,  HOST_LIST, FOL_LIST, LOCALFOLDER, type=AUTOBAK, PATHFILTER = ""):
        self.logger = self.setupLogger()
        self.logger.warning(
            "Please note that this utility does not use hostkeys to verify the hosts. If this is insecure for "
            "your setup, then kindly update the code or submit a feature request.")
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.PATHFILTER = PATHFILTER
        self.HOST_LIST = HOST_LIST
        self.FOL_LIST = FOL_LIST
        self.LOCALFOLDER = LOCALFOLDER
        self.type = type		
        if self.PATHFILTER.strip() == "":
            self.PATHFILTER = DIRFILTER

    def setupLogger(self):
        '''
        Just sets up the logger and returns the logger instance which was setup with the init function.

        :return: logger instance
        '''
        LOG_TAG = 'PARSER_XML'
        self.myLogger = logging.getLogger(LOG_TAG )
        self.myLogger.setLevel(logging.DEBUG)
        self.fh = RotatingFileHandler(LOG_TAG  + ".log", 'a', maxBytes=20*1024*1024,
                                      backupCount=20)
        self.fh.setLevel(logging.INFO)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        #self.sh = logging.StreamHandler()  #This is a stringIO based logger.
        #self.sh.setLevel(logging.INFO)
        #self.sh.setStream(self.loggerString)

        formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')
        self.ch.setFormatter(formatter)
        #self.sh.setFormatter(formatter)
        self.fh.setFormatter(formatter)

        self.myLogger.addHandler(self.ch)
        self.myLogger.addHandler(self.fh)
        #self.myLogger.addHandler(self.sh)
        return self.myLogger


    def get_r_portable(self, sftp, remotedir, localdir, preserve_mtime=False):
        for entry in sftp.listdir(remotedir):
            remotepath = remotedir + "/" + entry
            localpath = os.path.join(localdir, entry)
            mode = sftp.stat(remotepath).st_mode
            if S_ISDIR(mode):
                try:
                    os.makedirs(localpath)
                except OSError:  # dir exists
                    pass
                self.get_r_portable(sftp, remotepath, localpath, preserve_mtime)
            elif S_ISREG(mode):
                if self.PATHFILTER.strip() != "":
                    if str(remotepath).lower().find(self.PATHFILTER.lower()) > -1:
                        sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)
                        self.logger.info("Current remotepath is : " + str(remotepath) + ", Filter is " + self.PATHFILTER.strip().lower())

    def run(self):
        if self.type == self.AUTOBAK:
            REMOTEFOLDER = "/ftproot/"
        else:
            self.logger.info("Other types not implemented yet.")
            return

        for host in self.HOST_LIST:
            self.logger.info("Attempting connection to " + host[0])
            with pysftp.Connection(host[0], username=host[1], password=host[2], cnopts=self.cnopts) as sftp:
                try:
                    for dirs in self.FOL_LIST:
                        self.logger.info("Attempting download from " + dirs + "on " + host[0])
                        currdir = REMOTEFOLDER + dirs + "/Data/"
                        self.logger.info("Joining via os = " + os.path.join(REMOTEFOLDER, dirs,
                                                                            "/Data/") + " , currdir = " + currdir)
                        try:
                            self.get_r_portable(sftp, currdir, self.LOCALFOLDER, True)
                        except Exception as e:
                            self.logger.error("Exception in dir exploration" + str(e))

                except Exception as e:
                    self.logger.error("Exception " + str(e))
