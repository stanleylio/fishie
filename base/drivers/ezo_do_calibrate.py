from ezo_do import EZO_DO
import re

# script for DO sensor CALIBRATION
# just execute and follow the prompt:
#   python ezo_do_calibrate.py

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.31 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015


class EZO_DO_CALIBRATION(EZO_DO):

    def cal_status(self):
        return self._r('Cal,?',0.3)

    def cal_clear(self):
        self._r('Cal,clear',2)

    def cal_atm(self):
        self._r('Cal',2)

    def cal_0(self):
        self._r('Cal,0',2)


if '__main__' == __name__:
    do = EZO_DO_CALIBRATION(lowpower=False)
    print 'Supply voltage:'
    print '{} volt'.format(do.supply_v())
    print
    print 'Current T value (supplied for calibration, not measured):'
    print '{} Deg.C'.format(do.t())
    print
    print 'Current S value (salinity, supplied for calibration, not measured):'
    tmp = do.s()
    if tmp[1]:
        print '{} ppt'.format(tmp[0])
    else:
        print '{} uS'.format(tmp[0])
    print
    print 'Current P value (water pressure, supplied for calibration, not measured):'
    print '{} kPa'.format(do.p())
    print

    tmp = do.cal_status()
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
2: Calibrate to ATMOSPHEREIC oxygen level
3: Calibrate to ZERO Dissolved Oxygen
4: Set T value (water temperature, non-persistent)
5: Take a READing'''
    tmp = -1
    while tmp not in [1,2,3,4,5]:
        print s
        tmp = int(raw_input('Enter one of {1,2,3,4,5}:'))

    if 1 == tmp:
        print('Clearing old calibration data...')
        do.cal_clear()
        print('... done.')
    elif 2 == tmp:
        print('Calibratiing to atmospheric oxygen level...')
        do.cal_atm()
        print('... done.')
    elif 3 == tmp:
        print('Calibratiing to zero D.O....')
        do.cal_0()
        print('... done.')
    elif 4 == tmp:
        tmp = float(raw_input('Enter new T value (in Deg.C):'))
        print('Setting new T value to {} Deg.C...'.format(tmp))
        do.t(tmp)
        print('... done.')
    elif 5 == tmp:
        print 'Reading...'
        try:
            while True:
                print do.pretty()
                raw_input('Hit ENTER to read another, Ctrl+C to terminate...')
        except KeyboardInterrupt:
            print
            pass
    else:
        print('Huh?')

    do.sleep()

