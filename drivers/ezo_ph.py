# Driver for the Atlas Scientific EZO pH sensor

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH RPi/BBB
#
# See P.29 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
from .ezo import EZO
import time, logging, json
from os.path import join, dirname


logger = logging.getLogger(__name__)


class EZO_pH(EZO):
    '''Communication handler for the EZO pH sensor
    T value is set in ezo.json. It is sent to the sensor during
    instantiation and can be changed during runtime.
    Sensor is programmed to sleep between commands by default.
    
    '''

    def __init__(self, address=0x63, lowpower=False, bus=1):
        EZO.__init__(self, address=address, bus=bus, lowpower=lowpower)

        t = None
        configfn = join(dirname(__file__), 'ezo.json')
        try:
            t = json.load(open(configfn))['ezo_ph_t_celsius']
            self.t(t)
            logger.info('T value synced to {} Deg.C'.format(t))
        except:
            logger.exception('Error loading config file.')
        if t is None:
            logger.warning('T value not synced.')

    def read(self):
        tmp = self._r('R').strip().split(',')
        if self.lowpower:
            self.sleep()
        return float(tmp[0])

    def pretty_print(self, r=None):
        if r is None:
            r = self.read()
        print('pH = {:.2f}'.format(r))
        
    # super() and MRO... messy.
    def t(self, new=None):
        return super(EZO_pH, self).t(new, from_='EZO_pH: ')


if '__main__' == __name__:

    bus = 1

    logging.basicConfig(level=logging.DEBUG)

    ph = EZO_pH(bus=bus, lowpower=False)
    
    #print('Device Information (sensor type, firmware version): ' + ph.device_information())
    #print('Status: ' + ph.status())
    print('Supply voltage: {:.3f}V'.format(ph.supply_v()))
    print('Current T value (calibration parameter, not measured): {:.0f} Deg.C'.format(ph.t()))

    while True:
        print('pH = {}'.format(ph.read()))
