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
from .ezo_ec import EZO_EC
import sys, json, logging, string
from os.path import exists, join, dirname


class EZO_EC_CALIBRATION(EZO_EC):

    def cal_status(self):
        return self._r('Cal,?', 0.3)

    def cal_clear(self):
        self._r('Cal,clear', 2)

    def cal_dry(self):
        self._r('Cal,dry', 2)

    def cal_one(self, val):
        self._r('Cal,one,{:.2f}'.format(val), 2)

    def cal_low(self, val):
        self._r('Cal,low,{:.2f}'.format(val), 2)

    def cal_high(self, val):
        self._r('Cal,high,{:.2f}'.format(val), 2)


if '__main__' == __name__:

    logging.basicConfig(level=logging.WARNING)

    MAX_RETRY = 5
    options = [
        (1, 'CLEAR calibration data'),
        (2, 'SINGLE point calibration'),
        (3, 'DUAL points calibration'),
        (4, 'Set T value (sample temperature, non-persistent)'),
        (5, 'Set K value (probe scaling factor, non-persistent)'),
        (6, 'READ sensor'),
        (7, 'Print DEBUG info'),
        (0, 'EXIT'),
        ]

    prompt = '\n'.join(['\t{}. {}'.format(a, b) for a,b in options])
    prompt = '\n' + prompt + '\nEnter one of {}:'.format(','.join([str(a) for a,_ in options]))

    ec = EZO_EC_CALIBRATION(bus=1, lowpower=False)

    print('\x1b[2J\x1b[;H')

    while True:

        print()

        for i in range(MAX_RETRY):
            try:
                tmp = ec.cal_status()
                if tmp is not None and tmp.startswith('?CAL,'):
                    tmp = int(tmp.strip().split(',')[-1])
                    if 0 == tmp:
                        print('Sensor is NOT calibrated.')
                        break
                    elif 1 == tmp:
                        print('Sensor has been calibrated (single point).')
                        break
                    elif 2 == tmp:
                        print('Sensor has been calibrated (dual point).')
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
            ec.cal_clear()
            print(' done.')
        elif 2 == tmp:
            print('SINGLE point calibration selected.')
            print('Clearing existing calibration data...')
            ec.cal_clear()

            # DRY
            input('Step 1 of 2: Hit ENTER when probe is DRY:')
            print('Calibrating...', end='')
            ec.cal_dry()
            print(' done.')

            # WET
            while True:
                try:
                    tmp = input('Step 2 of 2: WET probe calibration. Enter the EC value (in microsiemens) to calibrate:')
                    tmp = float(tmp)
                    break
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            print('Calibrating to {:.1f}uS/cm...'.format(tmp), end='')
            ec.cal_one(tmp)
            print(' done.')

        elif 3 == tmp:
            print('DUAL points calibration selected.')
            print('Clearing existing calibration data...')
            ec.cal_clear()

            # DRY
            input('Step 1 of 3: Hit ENTER when probe is dry:')
            print('Calibrating...', end='')
            ec.cal_dry()
            print(' done.')

            # LOW
            while True:
                try:
                    tmp = input('Step 2 of 3: LOW point calibration. Enter the EC value (in microsiemens) to calibrate:')
                    tmp = float(tmp)
                    break
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            print('Calibrating to {:.1f}uS/cm...'.format(tmp), end='')
            ec.cal_low(tmp)
            print(' done.')

            # HIGH
            while True:
                try:
                    tmp = input('Step 3 of 3: HIGH point calibration. Enter the EC value (in microsiemens) to calibrate:')
                    tmp = float(tmp)
                    break
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            print('Calibrating to {:.1f}uS/cm...'.format(tmp), end='')
            ec.cal_high(tmp)
            print(' done.')
        elif 4 == tmp:
            print('Current T value (configuration parameter, not measured): {} Deg.C'.format(ec.t()))
            tmp = float(input('Enter new T value (in Deg.C): '))
            print('Setting new T value to {} Deg.C... '.format(tmp), end='')
            ec.t(tmp)
            
            t = ec.t()
            print('T value set to {}.'.format(t))

            configfn = join(dirname(__file__), 'ezo.json')
            config = {}
            if exists(configfn):
                try:
                    config = json.load(open(configfn))
                except:
                    logging.debug('Failed to load ezo.json')
            config['ezo_ec_t_celsius'] = t
            json.dump(config, open(configfn, 'w'))
        elif 5 == tmp:
            print('Current K value: {}'.format(ec.k()))
            tmp = float(input('Enter new K value: '))
            print('Setting new K value to {}... '.format(tmp), end='')
            ec.k(tmp)
            
            k = ec.k()
            print('K value set to {}.'.format(k))

            configfn = join(dirname(__file__), 'ezo.json')
            config = {}
            if exists(configfn):
                try:
                    config = json.load(open(configfn))
                except:
                    logging.debug('Failed to load ezo.json')
            config['ezo_ec_k'] = k
            json.dump(config, open(configfn, 'w'))
        elif 6 == tmp:
            try:
                while True:
                    r = ec.read()
                    print('{:.2f} uS/cm, {:.1f} PSU, TDS={:.1f}, Specific Gravity={:.3f}. Ctrl+C to terminate.'.format(r['ec'], r['sal'], r['tds'], r['sg']))
            except KeyboardInterrupt:
                pass
        elif 7 == tmp:
            print('Supply voltage: {:.3f} V'.format(ec.supply_v()))
            print('Current probe K value (configuration parameter): {}'.format(ec.k()))
            print('Current T value (configuration parameter, not measured): {:.1f} Deg.C'.format(ec.t()))
        else:
            print('Huh?')
