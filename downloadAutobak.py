import os
from datetime import datetime
from stat import S_ISDIR, S_ISREG

import pysftp

temp = datetime.now()
DIRFILTER = "AUTOBAKDATA{:04d}{:02d}{:02d}".format(temp.year, temp.month, temp.day)
print("Will look for directory with filter " + DIRFILTER)


class XMLDownloader:
    AUTOBAK = 1
    GEXPORT = 2
    NEEXPORT = 3

    def __init__(self, logger):
        self.logger = logger
        self.logger.warn(
            "Please note that this utility does not use hostkeys to verify the hosts. If this is insecure for "
            "your setup, then kindly update the code or submit a feature request.")
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None

    def get_r_portable(self, sftp, remotedir, localdir, preserve_mtime=False):
        for entry in sftp.listdir(remotedir):
            remotepath = remotedir + "/" + entry
            localpath = os.path.join(localdir, entry)
            mode = sftp.stat(remotepath).st_mode
            if S_ISDIR(mode):
                try:
                    os.mkdir(localpath)
                except OSError:  # dir exists
                    pass
                self.get_r_portable(sftp, remotepath, localpath, preserve_mtime)
            elif S_ISREG(mode):
                self.logger.info("Current remotepath is : " + str(remotepath))
                sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)

    def run(self, HOST_LIST, FOL_LIST, LOCALFOLDER, type=AUTOBAK):
        if type == self.AUTOBAK:
            REMOTEFOLDER = "/ftproot/"
        else:
            self.logger.info("Other types not implemented yet.")
            return

        for host in HOST_LIST:
            self.logger.info("Attempting connection to ", host[0])
            with pysftp.Connection(host[0], username=host[1], password=host[2], cnopts=self.cnopts) as sftp:
                try:
                    for dirs in FOL_LIST:
                        self.logger.info("Attempting download from " + dirs + "on " + host[0])
                        currdir = REMOTEFOLDER + dirs + "/Data/"
                        self.logger.info("Joining via os = " + os.path.join(REMOTEFOLDER, dirs,
                                                                            "/Data/") + " , currdir = " + currdir)
                        try:
                            self.get_r_portable(sftp, currdir, LOCALFOLDER, True)
                        except Exception as e:
                            self.logger.error("Exception in dir exploration" + str(e))

                except Exception as e:
                    self.logger.error("Exception " + str(e))
