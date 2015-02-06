from ezo_orp import EZO_ORP
import re

# script for ORP sensor CALIBRATION
# just execute and follow the prompt:
#   python ezo_orp_calibrate.py

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.25 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015


class EZO_ORP_CALIBRATION(EZO_ORP):

    def cal_status(self):
        return self._r('Cal,?',0.3)

    def cal_clear(self):
        self._r('Cal,clear',2)

    def cal(self,val):
        self._r('Cal,{:.2f}'.format(val),2)


if '__main__' == __name__:
    orp = EZO_ORP_CALIBRATION(lowpower=False)
    print 'Supply voltage:'
    print '{} volt'.format(orp.supply_v())
    print

    tmp = orp.cal_status()
    if tmp.startswith('?CAL,'):
        tmp = int(tmp.strip().split(',')[-1])
        if 0 == tmp:
            print 'Sensor is NOT calibrated.'
        elif 1 == tmp:
            print 'Sensor has been calibrated.'
        else:
            print 'Huh?'
    else:
        print 'Huh?'

    print
    print '- - - - -'

    s = '''1: CLEAR calibration datum only
2: Calibrate
3: Take a READing'''
    tmp = -1
    while tmp not in [1,2,3]:
        print s
        tmp = int(raw_input('Enter one of {1,2,3}:'))

    if 1 == tmp:
        print('Clearing old calibration datum...')
        orp.cal_clear()
        print('... done.')
    elif 2 == tmp:
        tmp = float(raw_input('Enter calibration value in mV:'))
        print('Calibratiing...')
        orp.cal(tmp)
        print('... done.')
    elif 3 == tmp:
        print 'Reading...'
        try:
            while True:
                print '{:.2f} mV'.format(orp.read())
                raw_input('Hit ENTER to read another, Ctrl+C to terminate...')
        except KeyboardInterrupt:
            print
            pass
    else:
        print('Huh?')

    orp.sleep()

