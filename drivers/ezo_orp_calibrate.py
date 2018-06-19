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
from .ezo_orp import EZO_ORP
import sys, json, logging, string
from os.path import exists, join, dirname


class EZO_ORP_CALIBRATION(EZO_ORP):

    def cal_status(self):
        return self._r('Cal,?',0.3)

    def cal_clear(self):
        self._r('Cal,clear',2)

    def cal(self,val):
        self._r('Cal,{:.2f}'.format(val),2)


if '__main__' == __name__:
    
    logging.basicConfig(level=logging.WARNING)

    MAX_RETRY = 5
    options = [
        (1, 'CLEAR calibration data'),
        (2, 'Calibrate'),
        (3, 'READ sensor'),
        (4, 'Print DEBUG info'),
        (0, 'EXIT'),
        ]

    prompt = '\n'.join(['\t{}. {}'.format(a, b) for a,b in options])
    prompt = '\n' + prompt + '\nEnter one of {}:'.format(','.join([str(a) for a,_ in options]))

    orp = EZO_ORP_CALIBRATION(bus=1, lowpower=False)
    
    print('\x1b[2J\x1b[;H')

    while True:

        for i in range(MAX_RETRY):
            try:
                tmp = orp.cal_status()
                if tmp is not None and tmp.startswith('?CAL,'):
                    tmp = int(tmp.strip().split(',')[-1])
                    if 0 == tmp:
                        print('Sensor is NOT calibrated.')
                        break
                    elif 1 == tmp:
                        print('Sensor has been calibrated.')
                        break
                    else:
                        pass
                else:
                    pass
                logging.error('Invalid response from sensor: {}'.format(tmp))
            except OSError as e:
                logging.exception('wut?')

        r = input(prompt)
        try:
            tmp = int(''.join([c if c in string.digits else '' for c in r]))
        except ValueError:
            pass

        print('Your choice: {}'.format(tmp))

        if 0 == tmp:
            print('Terminated by user.')
            sys.exit()
        elif 1 == tmp:
            print('Clearing existing calibration data...', end='')
            orp.cal_clear()
            print(' done.')
        elif 2 == tmp:
            tmp = float(input('Enter calibration value in mV: '))
            print('Calibratiing...', end='')
            orp.cal(tmp)
            print(' done.')
        elif 3 == tmp:
            try:
                while True:
                    print('{:.2f} mV. Ctrl+C to terminate.'.format(orp.read()))
            except KeyboardInterrupt:
                pass
        elif 4 == tmp:
            print('Supply voltage: {:.3f}V'.format(orp.supply_v()))
        else:
            print('Huh?')
