import calendar, subprocess, logging, pika
from datetime import datetime
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

def is_rpi():
    return exists('/etc/os-release') and 'Raspbian' in open('/etc/os-release').readline()

def init_rabbit(name, password, *, exchange='uhcm', host='localhost'):
    credentials = pika.PlainCredentials(name, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, '/', credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
    return connection, channel
