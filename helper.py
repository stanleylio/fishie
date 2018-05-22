# goal: get rid of this whole file.
import calendar
from datetime import datetime
#from numpy import diff,mean,median,size,flatnonzero,append,insert,absolute
import subprocess, logging
from os.path import exists


def dt2ts(dt=None):
    if dt is None:
        dt = datetime.utcnow()
    return calendar.timegm(dt.timetuple()) + (dt.microsecond)*(1e-6)

def ts2dt(ts=None):
    if ts is None:
        ts = dt2ts()
    return datetime.utcfromtimestamp(ts)

def getsize(path):
    """size of path (file or dir) in KB"""
    if not exists(path):
        raise IOError(path + ' does not exist')
    p = subprocess.Popen(['du', '-s', path],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    if len(err):
        logging.warning(err)
    return out.split('\t')[0]
