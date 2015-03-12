from ezo_ec import EZO_EC
import re

# script for EC sensor CALIBRATION
# just execute and follow the prompt:
#   python ezo_ec_calibrate.py

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.32 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015


class EZO_EC_CALIBRATION(EZO_EC):

    def cal_status(self):
        return self._r('Cal,?',0.3)

    def cal_clear(self):
        self._r('Cal,clear',2)

    def cal_dry(self):
        self._r('Cal,dry',2)

    def cal_one(self,val):
        self._r('Cal,one,{:.2f}'.format(val),2)

    def cal_low(self,val):
        self._r('Cal,low,{:.2f}'.format(val),2)

    def cal_high(self,val):
        self._r('Cal,high,{:.2f}'.format(val),2)

if '__main__' == __name__:
    ec = EZO_EC_CALIBRATION(lowpower=False)

    print 'Supply voltage:'
    print '{:.3f} volt'.format(ec.supply_v())
    print
    print 'Current K value (of probe):'
    print ec.k()
    print
    # K value should be set in the ezo.ini file.
    print 'Current T value (calibration parameter, not measured):'
    print '{:.0f} Deg.C'.format(ec.t())
    print
    print 'A sample read:'
    ec.pretty_print(ec.read())
    print
    #ec.sleep()

    tmp = ec.cal_status()
    if tmp.startswith('?CAL,'):
        tmp = int(tmp.strip().split(',')[-1])
        if 0 == tmp:
            print 'Sensor is NOT calibrated.'
        elif 1 == tmp:
            print 'Sensor has been calibrated (single point).'
        elif 2 == tmp:
            print 'Sensor has been calibrated (dual point).'
        else:
            print 'Huh? (P.44)'
    else:
        print 'Huh? (P.44)'

    print
    print '- - - - -'
    s = '''1: CLEAR calibration data only
2: SINGLE point calibration
3: DUAL points calibration
4: Set T value (water temperature, non-persistent)
5: Take a READing'''
    tmp = -1
    while tmp not in [1,2,3,4,5]:
        print s
        tmp = int(raw_input('Enter one of {1,2,3,4,5}:'))

    if 1 == tmp:
        print('Clearing old calibration data...')
        ec.cal_clear()
        print('... done.')
    elif 2 == tmp:
        print('SINGLE point calibration selected.')
        print('Clearing old calibration data...')
        ec.cal_clear()
        print('... done.')
        raw_input('Step 1 of 2: Dry Calibration. Make sure the probe is dry. Hit ENTER when ready...')
        print('Calibrating...')
        ec.cal_dry()
        print('... done.')
        tmp = ''
        while not re.match('\+?\-*\d+.*\d*',tmp):
            tmp = raw_input('Step 2 of 2: Wet probe calibration. Enter the EC value (in microsiemens) to calibrate:')
        tmp = float(tmp)
        print('{:.3f}uS. Calibrating...'.format(tmp))
        ec.cal_one(tmp)
        #print ec.read()
        print('Calibration Completed.')
    elif 3 == tmp:
        print('DUAL points calibration selected.')
        print('Clearing old calibration data...')
        ec.cal_clear()
        print('... done.')
        raw_input('Step 1 of 3: Dry Calibration. Make sure the probe is dry. Hit ENTER when ready...')
        print('Calibrating...')
        ec.cal_dry()
        print('... done.')

        tmp = ''
        while not re.match('\+?\-*\d+.*\d*',tmp):
            tmp = raw_input('Step 2 of 3: LOW point calibration. Enter the EC value (in microsiemens) to calibrate:')
        tmp = float(tmp)
        print('{:.2f}uS. Calibrating...'.format(tmp))
        ec.cal_low(tmp)
        print('... done.')
        
        tmp = ''
        while not re.match('\+?\-*\d+.*\d*',tmp):
            tmp = raw_input('Step 3 of 3: HIGH point calibration. Enter the EC value (in microsiemens) to calibrate:')
        tmp = float(tmp)
        print('{:.2f}uS. Calibrating...'.format(tmp))
        ec.cal_high(tmp)
        print('... done.')
        
        print('Calibration Completed.')
    elif 4 == tmp:
        tmp = float(raw_input('Enter new T value (in Deg.C):'))
        print('Setting new T value to {} Deg.C...'.format(tmp))
        ec.t(tmp)
        print('... done.')
    elif 5 == tmp:
        print('Reading...')
        try:
            while True:
                ec.pretty_print(ec.read())
                raw_input('Hit ENTER to read another, Ctrl+C to terminate...')
        except KeyboardInterrupt:
            print
            pass
    else:
        print('Huh?')

    ec.sleep()

