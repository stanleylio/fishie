# Driver for the Atlas Scientific EZO EC (Electrical Conductivity) sensor

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.32 of the datasheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import time, logging, json
from .ezo import EZO
from os.path import join, dirname


logger = logging.getLogger(__name__)


# Communication handler for the EZO EC sensor
# K and T values are set in the .ini file. K is sent to the sensor
# during instantiation. Both can be changed during runtime.
# Sensor is programmed to sleep between commands by default.
class EZO_EC(EZO):
    def __init__(self, address=0x64, bus=1, lowpower=False):
        EZO.__init__(self, address=address, bus=bus, lowpower=lowpower)

        t = None
        try:
            configfn = join(dirname(__file__), 'ezo.json')
            t = json.load(open(configfn))['ezo_ec_t_celsius']
            self.t(t)
            logger.info('T value synced to {} Deg.C'.format(t))
        except:
            logger.warning('Error loading config file.')
        if t is None:
            logger.warning('T value not synced.')

        k = None
        try:
            configfn = join(dirname(__file__), 'ezo.json')
            k = json.load(open(configfn))['ezo_ec_k']
            self.k(k)
            logger.info('K value synced to {}'.format(k))
        except:
            logger.warning('Error loading config file.')
        if k is None:
            logger.warning('K value not synced.')

    # see P.39
    def read(self):
        tmp = self._r('R').strip().split(',')

        d = {'ec':float(tmp[0])}        # Electrical Conductivity
        
        if len(tmp) >= 2:
            d['tds'] = float(tmp[1])    # Total Dissolved Solids
        if len(tmp) >= 3:
            d['sal'] = float(tmp[2])    # Salinity
        if len(tmp) >= 4:
            d['sg'] = float(tmp[3])     # Specific Gravity

        if self.lowpower:
            self.sleep()
        return d

    # see P.40
    # If called without argument, read the current K value in the sensor.
    # If a new K value is supplied, send to sensor only if it is valid and is different from
    # the current K value in the sensor.
    # NOTE: data sheet does not specify how many decimal places the sensor accept and return
    # Experiments say: 2 decimal places. Try >=3 and you will mess up the sensor.
    # Implementation Note: I could abstract this into a general function like I did with the
    # other commands, but 1. there are only 'K' and 'T' two choices, and 2. the boundary check
    # of 'K' and 'T' are slightly different.
    def k(self, new=None):
        tmp = self._r('K,?', 0.3)    # always do a read first
        if tmp.startswith('?K,'):
            current = float(tmp[3:7])
            if new is None:
                if self.lowpower:
                    self.sleep()
                return current
            elif current != new:
                if new >= 0.1 and new <= 10:
                    logging.debug('update current K = {} to new K = {}'.format(current, new))
                    cmd = 'K,{:.2f}'.format(new)
                    self._r(cmd,0.3)    # ignore the response
                    if self.lowpower:
                        self.sleep()
                else:
                    logging.error('EZO_EC: invalid K value supplied')
            else:
                logging.debug('EZO_EC: supplied K == current K = {}, no update required'.format(current))
        else:
            logging.warning('EZO_EC: cannot retrieve K value from sensor')
        if self.lowpower:
            self.sleep()

    # super() and MRO... messy.
    def t(self, new=None):
        return super(EZO_EC, self).t(new, from_='EZO_EC: ')

    def pretty(self, r=None):
        if r is None:
            r = self.read()
        s = 'Conductivity: {} uS/cm'.format(r['ec'])
        if 'sal' in r:
            s = s + '\nSalinity: {}'.format(r['sal'])           # no defined unit, P.7
        if 'tds' in r:
            s = s + '\nTotal Dissolved Solid: {} mg/L'.format(r['tds'])
        if 'sg' in r:
            s = s + '\nSpecific Gravity: {}'.format(r['sg'])    # unitless, P.7
        return s


if '__main__' == __name__:

    bus = 1

    logging.basicConfig(level=logging.WARNING)
    
    ec = EZO_EC(bus=bus, lowpower=False)
    
    #print('Device Information (sensor type, firmware version): ' + ec.device_information())
    #print('Status: ' + ec.status())
    print('Supply voltage: {:.3f} volt'.format(ec.supply_v()))
    print('Current K value (of probe): {}'.format(ec.k()))
    print('Current T value (calibration parameter, not measured): {} Deg.C'.format(ec.t()))

    while True:
        tmp = ec.read()
        print(tmp)
