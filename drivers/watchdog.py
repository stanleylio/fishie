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
        # the return value doesn't work. TODO
        return self.bus.read_word_data(self.addr,10)


def reset_auto():
    good = [False,False]
    for bus in [1,2]:
        logging.debug('bus {}...'.format(bus))
        try:
            w = Watchdog(bus=bus)
            for i in range(3):
                w.reset()
            good[bus-1] = True
            #break
        except IOError:
            #logging.exception(traceback.format_exc())
            pass
    if any(good):
        for k,tmp in enumerate(good):
            if tmp:
                logging.debug('Found watchdog on bus {}'.format(k+1))
        return True
    else:
        logging.warning('No WDT found.')
        return False


if '__main__' == __name__:
    logging.basicConfig(level=logging.DEBUG)
    reset_auto()
