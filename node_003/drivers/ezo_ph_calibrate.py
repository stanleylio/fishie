from ezo_ph import EZO_pH
import re

# script for pH sensor calibration
# just execute and follow the prompt:
#   python ezo_ph_calibrate.py

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.29 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015


class EZO_pH_CALIBRATION(EZO_pH):

    def cal_status(self):
        return self._r('Cal,?',0.3)

    def cal_clear(self):
        self._r('Cal,clear',2)

    def cal_mid(self,val):
        self._r('Cal,mid,{:.2f}'.format(val),2)

    def cal_low(self,val):
        self._r('Cal,low,{:.2f}'.format(val),2)

    def cal_high(self,val):
        self._r('Cal,high,{:.2f}'.format(val),2)


if '__main__' == __name__:
    ph = EZO_pH_CALIBRATION(lowpower=False)
    print 'Supply voltage:'
    print '{} volt'.format(ph.supply_v())
    print
    print 'Current T value (supplied for calibration, not measured):'
    print '{} Deg.C'.format(ph.t())
    print

    tmp = ph.cal_status()
    if tmp.startswith('?CAL,'):
        tmp = int(tmp.strip().split(',')[-1])
        if 0 == tmp:
            print 'Sensor is NOT calibrated.'
        elif 1 == tmp:
            print 'Sensor has been calibrated (SINGLE point).'
        elif 2 == tmp:
            print 'Sensor has been calibrated (DUAL point).'
        elif 3 == tmp:
            print 'Sensor has been calibrated (THREE point).'
        else:
            print 'Huh?'
    else:
        print 'Huh?'

    print
    print '- - - - -'

    s = '''1: CLEAR calibration data only
2: Calibrate for pH MIDPOINT (around 7; will clear all calibration)
3: Calibrate for LOW pH (optional)
4: Calibrate for HIGH pH (optional)
5: Set T value (water temperature, non-persistent)
6: Take a READing'''
    tmp = -1
    while tmp not in [1,2,3,4,5,6]:
        print s
        tmp = int(raw_input('Enter one of {1,2,3,4,5,6}:'))

    if 1 == tmp:
        print('Clearing old calibration data...')
        ph.cal_clear()
        print('... done.')
    elif 2 == tmp:
        print('Calibrate for pH midpoint...')
        tmp = float(raw_input('Enter pH value:'))
        print('Calibrating to {}...'.format(tmp))
        ph.cal_mid(tmp)
        print('... done.')
    elif 3 == tmp:
        tmp = ph.cal_status()
        if tmp.startswith('?CAL,'):
            tmp = int(tmp.strip().split(',')[-1])
        if 0 == tmp:
            print('Midpoint calibration must be performed first. (P.38)')
            print('LOW pH calibration NOT performed.')
        else:
            print('Calibrate for LOW pH...')
            tmp = float(raw_input('Enter pH value:'))
            print('Calibrating to {}...'.format(tmp))
            ph.cal_low(tmp)
            print('... done.')
    elif 4 == tmp:
        tmp = ph.cal_status()
        if tmp.startswith('?CAL,'):
            tmp = int(tmp.strip().split(',')[-1])
        if 0 == tmp:
            print('Midpoint calibration must be performed first. (P.38)')
            print('HIGH pH calibration NOT performed.')
        else:
            print('Calibrate for HIGH pH...')
            tmp = float(raw_input('Enter pH value:'))
            print('Calibrating to {}...'.format(tmp))
            ph.cal_high(tmp)
            print('... done.')
    elif 5 == tmp:
        tmp = float(raw_input('Enter new T value (in Deg.C):'))
        print('Setting new T value to {} Deg.C...'.format(tmp))
        ph.t(tmp)
        print('... done.')
    elif 6 == tmp:
        print 'Reading...'
        try:
            while True:
                print 'pH = {:.2f}'.format(ph.read())
                raw_input('Hit ENTER to read another, Ctrl+C to terminate...')
        except KeyboardInterrupt:
            print
            pass
    else:
        print('Huh?')

    ph.sleep()
    
