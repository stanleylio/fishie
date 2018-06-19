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
from .ezo_ph import EZO_pH
import sys, string, logging, json
from os.path import exists, join, dirname


class EZO_pH_CALIBRATION(EZO_pH):

    def cal_status(self):
        return self._r('Cal,?', 0.3)

    def cal_clear(self):
        self._r('Cal,clear', 2)

    def cal_mid(self, val):
        self._r('Cal,mid,{:.2f}'.format(val), 2)

    def cal_low(self, val):
        self._r('Cal,low,{:.2f}'.format(val), 2)

    def cal_high(self, val):
        self._r('Cal,high,{:.2f}'.format(val), 2)


if '__main__' == __name__:

    logging.basicConfig(level=logging.WARNING)
    
    MAX_RETRY = 5
    options = [
        (1, 'CLEAR calibration data'),
        (2, 'Calibrate for pH MIDPOINT (around 7; will clear all calibration)'),
        (3, 'Calibrate for LOW pH (optional)'),
        (4, 'Calibrate for HIGH pH (optional)'),
        (5, 'Set T value (sample temperature; non-persistent)'),
        (6, 'READ sensor'),
        (7, 'Print DEBUG info'),
        #(8, 'Put sensor to SLEEP'),
        (0, 'EXIT'),
        ]

    prompt = '\n'.join(['\t{}. {}'.format(a, b) for a,b in options])
    prompt = '\n' + prompt + '\nEnter one of {}:'.format(','.join([str(a) for a,_ in options]))

    ph = EZO_pH_CALIBRATION(bus=1, lowpower=False)

    print('\x1b[2J\x1b[;H')
    
    while True:

        print()
        
        for i in range(MAX_RETRY):
            try:
                tmp = ph.cal_status()
                if tmp is not None and tmp.startswith('?CAL,'):
                    tmp = int(tmp.strip().split(',')[-1])
                    if 0 == tmp:
                        print('Sensor is NOT calibrated.')
                        break
                    elif 1 == tmp:
                        print('Sensor has been calibrated (SINGLE point).')
                        break
                    elif 2 == tmp:
                        print('Sensor has been calibrated (DUAL point).')
                        break
                    elif 3 == tmp:
                        print('Sensor has been calibrated (THREE point).')
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
            continue

        print('Your choice: {}'.format(tmp))

        if 0 == tmp:
            print('Terminated by user.')
            sys.exit()
        elif 1 == tmp:
            print('Clearing existing calibration data...', end='')
            ph.cal_clear()
            print(' done.')
        elif 2 == tmp:
            print('Calibrate for pH midpoint...')
            tmp = float(input('Enter pH value: '))
            print('Calibrating to {}...'.format(tmp))
            ph.cal_mid(tmp)
            print('... done.')
        elif 3 == tmp:
            tmp = ph.cal_status()
            if tmp.startswith('?CAL,'):
                tmp = int(tmp.strip().split(',')[-1])
            if 0 == tmp:
                print('Midpoint calibration must be performed first. (consult datasheet)')
                print('LOW pH calibration NOT performed.')
            else:
                print('Calibrate for LOW pH...')
                tmp = float(input('Enter pH value: '))
                print('Calibrating to {}...'.format(tmp), end='')
                ph.cal_low(tmp)
                print(' done.')
        elif 4 == tmp:
            tmp = ph.cal_status()
            if tmp.startswith('?CAL,'):
                tmp = int(tmp.strip().split(',')[-1])
            if 0 == tmp:
                print('Midpoint calibration must be performed first. (consult datasheet)')
                print('HIGH pH calibration NOT performed.')
            else:
                print('Calibrate for HIGH pH...')
                tmp = float(input('Enter pH value: '))
                print('Calibrating to {}...'.format(tmp), end='')
                ph.cal_high(tmp)
                print(' done.')
        elif 5 == tmp:
            print('Current T value (configuration parameter, not measured): {} Deg.C'.format(ph.t()))
            tmp = float(input('Enter new T value (in Deg.C): '))
            print('Setting new T value to {} Deg.C... '.format(tmp), end='')
            ph.t(tmp)
            
            t = ph.t()
            print('T value set to {}.'.format(t))

            configfn = join(dirname(__file__), 'ezo.json')
            config = {}
            if exists(configfn):
                try:
                    config = json.load(open(configfn))
                except:
                    logging.debug('Failed to load ezo.json')
            config['ezo_ph_t_celsius'] = t
            json.dump(config, open(configfn, 'w'))
        elif 6 == tmp:
            try:
                while True:
                    print('pH = {:.2f}. Ctrl+C to terminate.'.format(ph.read()))
            except KeyboardInterrupt:
                pass
        elif 7 == tmp:
            print('Supply voltage: {}V; T value (configuration parameter, not measured): {:.1f} Deg.C'.format(ph.supply_v(), ph.t()))
#        elif 8 == tmp:
#            print('Put sensor to sleep...')
#            
#            for i in range(MAX_RETRY):
#                try:
#                    ph.sleep()
#                except OSError:
#                    pass
        else:
            print('Huh?')
