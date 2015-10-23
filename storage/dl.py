#!/usr/bin/python
import urllib2

#baseurl = 'http://www.soest.hawaii.edu/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/PoH/'
baseurl = 'http://www2.hawaii.edu/~hlio/base-003/storage/'

def fetch_db():
    files = ['sensor_data.db','sensor_data.db-shm','sensor_data.db-wal']

    for v in files:
        url = baseurl + v

        print('Downloading {}'.format(url))
        response = urllib2.urlopen(url)
        html = response.read()

        with open(v,'wb') as f:
            f.write(html)

    print('Done.')


def fetch_raw():
    url = baseurl + 'raw.txt'

    print('Downloading {}'.format(url))
    response = urllib2.urlopen(url)
    html = response.read()
    with open('raw.txt','wb') as f:
        f.write(html)
    print('Done.')


if '__main__' == __name__:
    import sys
    sys.path.append('..')
    import config
    from config.config_support import *
    
    if not is_node() and not is_base():
        fetch_db()
    else:
        # will overwrite the existing database files (if any)!
        raw_input('comment these out if you want to run this')

