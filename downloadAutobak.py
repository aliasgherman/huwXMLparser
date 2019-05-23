import pysftp
from datetime import datetime

HOST_LIST = [ ["10.200.163.7", "ftpuser", "Vod_ftp_2015"],
                ["10.200.163.15", "ftpuser", "Vod_ftp_2015"],
                ["10.200.163.230", "ftpuser", "Changeme_123"]]

LOCALFOLDER = "E:\\AAM\\TEST\\"
REMOTEFOLDER = "/ftproot/"
FOL_LIST = ["BTS3900", "BTS3900 LTE", "BTS5900 5G", "BTS5900 LTE", "PICO BTS3900", "DBS3900 IBS", "MICRO BTS3900"]


cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

temp = datetime.now()
DIRFILTER = "AUTOBAKDATA{:04d}{:02d}{:02d}".format(temp.year, temp.month, temp.day)
print("Will look for directory with filter " + DIRFILTER)



import os
from stat import S_IMODE, S_ISDIR, S_ISREG

def get_r_portable(sftp, remotedir, localdir, preserve_mtime=False):
    for entry in sftp.listdir(remotedir):
        remotepath = remotedir + "/" + entry
        localpath = os.path.join(localdir, entry)            
        mode = sftp.stat(remotepath).st_mode
        if S_ISDIR(mode):
            try:
                os.mkdir(localpath)
            except OSError:     # dir exists
                pass
            get_r_portable(sftp, remotepath, localpath, preserve_mtime)
        elif S_ISREG(mode):
            sftp.get(remotepath, localpath, preserve_mtime=preserve_mtime)
            
            
for host in HOST_LIST:
    print("Attempting connection to ", host[0])
    with pysftp.Connection(host[0],username=host[1], password=host[2], cnopts = cnopts) as sftp:
        try:
            for dirs in FOL_LIST:
                print("Attempting download from ", dirs, "on ", host[0])
                currdir = REMOTEFOLDER + dirs + "/Data/"
                try:
                    get_r_portable(sftp, currdir, LOCALFOLDER, True)
                except Exception as e:
                    print("Exception in dir exploration", e)


        except Exception as e:
            print("Exception", e)            
