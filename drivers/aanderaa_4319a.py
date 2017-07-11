# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
# University of Hawaii
import serial,traceback,logging


def parse_4319a(line):
    tmp = line.strip().split('\t')
    if '4319' not in tmp[0]:
        logging.debug('4319 tag not found')
        logging.debug(line)
        return None
    if len(tmp) != 4:
        logging.debug('Expected 4 fields')
        logging.debug(line)
        return None
    line = tmp
    tags = ['sn','ec','t']
    line[2] = float(line[2])
    line[3] = float(line[3])
    return dict(zip(tags,line[1:]))

def aanderaa_4319a_read(port):
    with serial.Serial(port,9600,timeout=1) as s:
        retry = 3
        for i in range(retry):
            s.write('\r\ndo sample\r\n')
            line = s.readline()
            return parse_4319a(line)


if '__main__' == __name__:
    while True:
        print(aanderaa_4319a_read('/dev/ttyUSB0'))
