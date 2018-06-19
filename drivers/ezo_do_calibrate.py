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
from .ezo_do import EZO_DO
import sys, string, logging, json
from os.path import exists, join, dirname


class EZO_DO_CALIBRATION(EZO_DO):

    def cal_status(self):
        return self._r('Cal,?', 0.3)

    def cal_clear(self):
        self._r('Cal,clear', 2)

    def cal_atm(self):
        self._r('Cal', 2)

    def cal_0(self):
        self._r('Cal,0', 2)


if '__main__' == __name__:

    logging.basicConfig(level=logging.WARNING)

    MAX_RETRY = 5
    options = [
        (1, 'CLEAR calibration data'),
        (2, 'Calibrate to ATMOSPHEREIC oxygen level'),
        (3, 'Calibrate to ZERO Dissolved Oxygen'),
        (4, 'Set T value (sample temperature; non-persistent)'),
        (5, 'Set P value (sample pressure; non-persistent)'),
        (6, 'Set S value (sample conductivity; non-persistent)'),
        (7, 'READ sensor'),
        (8, 'Print DEBUG info'),
        (0, 'EXIT'),
        ]

    prompt = '\n'.join(['\t{}. {}'.format(a, b) for a,b in options])
    prompt = '\n' + prompt + '\nEnter one of {}:'.format(','.join([str(a) for a,_ in options]))

    do = EZO_DO_CALIBRATION(bus=1, lowpower=False)

    while True:

        print()

        for i in range(MAX_RETRY):
            try:
                tmp = do.cal_status()
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

        if 1 == tmp:
            print('Clearing existing calibration data...', end='')
            do.cal_clear()
            print(' done.')
        elif 2 == tmp:
            print('Calibratiing to atmospheric oxygen level...', end='')
            do.cal_atm()
            print(' done.')
        elif 3 == tmp:
            print('Calibratiing to zero DO...', end='')
            do.cal_0()
            print(' done.')
        elif 4 == tmp:
            print('Current T value (configuration parameter, not measured): {} Deg.C'.format(do.t()))
            tmp = float(input('Enter new T value (in Deg.C): '))
            print('Setting new T value to {} Deg.C... '.format(tmp), end='')
            do.t(tmp)
            
            t = do.t()
            print('T value set to {}.'.format(t))

            configfn = join(dirname(__file__), 'ezo.json')
            config = {}
            if exists(configfn):
                try:
                    config = json.load(open(configfn))
                except:
                    logging.debug('Failed to load ezo.json')
            config['ezo_do_t_celsius'] = t
            json.dump(config, open(configfn, 'w'))
        elif 5 == tmp:
            print('Current P value (configuration parameter, not measured): {} kPa'.format(do.p()))
            tmp = float(input('Enter new P value (in kPa): '))
            print('Setting new P value to {} kPa... '.format(tmp), end='')
            do.p(tmp)
            
            p = do.p()
            print('P value set to {}.'.format(p))

            configfn = join(dirname(__file__), 'ezo.json')
            config = {}
            if exists(configfn):
                try:
                    config = json.load(open(configfn))
                except:
                    logging.debug('Failed to load ezo.json')
            config['ezo_do_p_kPa'] = p
            json.dump(config, open(configfn, 'w'))
        elif 6 == tmp:
            print('Current S value (configuration parameter, not measured): {} uS/cm'.format(do.s()))
            tmp = float(input('Enter new S value (in uS/cm): '))
            print('Setting new S value to {} uS/cm... '.format(tmp), end='')
            do.s(tmp)
            
            s = do.s()
            print('S value set to {}.'.format(s))

            configfn = join(dirname(__file__), 'ezo.json')
            config = {}
            if exists(configfn):
                try:
                    config = json.load(open(configfn))
                except:
                    logging.debug('Failed to load ezo.json')
            config['ezo_do_s_uS'] = s
            json.dump(config, open(configfn, 'w'))
        elif 7 == tmp:
            try:
                while True:
                    print('{}. Ctrl+C to terminate.'.format(do.pretty()))
            except KeyboardInterrupt:
                pass
        elif 8 == tmp:
            print('Supply voltage: {:.3f}V'.format(do.supply_v()))
            print('Current T value (supplied for calibration, not measured): {:.1f} Deg.C'.format(do.t()))
            print('Current S value (salinity, supplied for calibration, not measured): ', end='')
            tmp = do.s()
            if tmp[1]:
                print('{:.2f} ppt'.format(tmp[0]))
            else:
                print('{:.1f} uS/cm'.format(tmp[0]))
            print('Current P value (water pressure, supplied for calibration, not measured): {} kPa'.format(do.p()))
        else:
            print('Huh?')
