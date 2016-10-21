#!/usr/bin/python
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import sys,time,os,traceback,smbus,logging


class Watchdog(object):
    def __init__(self,addr=0x51,bus=1):
        self.addr = addr
        self.bus = smbus.SMBus(bus)

    def reset(self):
        return self.bus.read_word_data(self.addr,10)


def reset_auto():
    good = False
    for bus in [1,2]:
        try:
            w = Watchdog(bus=bus)
            for i in range(10):
                w.reset()
            good = True
            #break
        except IOError:
            #print('nope.')
            #traceback.print_exc()
            pass
    if good:
        logging.debug('Found watchdog on bus {}'.format(bus))
    else:
        logging.error('No WDT found.')


if '__main__' == __name__:
    logging.basicConfig(level=logging.DEBUG)
    reset_auto()
