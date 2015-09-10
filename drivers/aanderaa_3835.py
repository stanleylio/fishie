#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. September 2015
import re

def PRINT(s):
    #pass
    print(s)

class Aanderaa_3835(object):
    msgfield = ['Oxygen','Saturation','Temperature']
    convf = [float,float,float]

    @staticmethod
    def parse_3835(line):
        d = None
        try:
            line = line.strip()
            r = '.*MEASUREMENT\s+3835\s+(?P<SN>\d+)\s+' +\
                  'Oxygen\:\s+(?P<Oxygen>[+-]*\d+\.*\d*)\s+' +\
                  'Saturation\:\s+(?P<Saturation>[+-]*\d+\.*\d*)\s+' +\
                  'Temperature\:\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
            r = re.match(r,line)
            if r is not None:
                d = {}
                for k,c in enumerate(Aanderaa_3835.msgfield):
                    d[c] = Aanderaa_3835.convf[k](r.group(c))
        except Exception as e:
            PRINT('parse_3835(): cannot parse: {}'.format(line))
            PRINT(e)
        return d


if '__main__' == __name__:
    c1 = 'MEASUREMENT	  3835	   506	Oxygen: 	   264.81	Saturation: 	    90.54	Temperature: 	    18.47'
    c2 = 'MEASUREMENT	  3835	   505	Oxygen: 	   287.81	Saturation: 	    95.10	Temperature: 	    16.82'
    c3 = 'only nixon can go to china'

    optode = Aanderaa_3835()
    print optode.parse_3835(c1)
    print optode.parse_3835(c2)
    print optode.parse_3835(c3)

