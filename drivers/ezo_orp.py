# Driver for the Atlas Scientific EZO ORP sensor

# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.25 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
from .ezo import EZO
import time, logging, json
from os.path import join, dirname


logger = logging.getLogger(__name__)


# Communication handler for the EZO ORP sensor
# T value is set in the .ini file. It is sent to the sensor during
# instantiation and can be changed during runtime.
# Sensor is programmed to sleep between commands by default.
class EZO_ORP(EZO):
    
    def __init__(self, address=0x62, bus=1, lowpower=False):
        EZO.__init__(self, address=address, bus=bus, lowpower=lowpower)

    def read(self):
        tmp = self._r('R').strip().split(',')
        if self.lowpower:
            self.sleep()
        return float(tmp[0])

    # ORP has no T parameter
    def t(self, new=None):
        logging.warning('ORP sensor has no T parameter')

    def pretty_print(self, r=None):
        if r is None:
            r = self.read()
        print('orp = {:.2f} mV'.format(r))
        

if '__main__' == __name__:

    bus = 1

    logging.basicConfig(level=logging.DEBUG)

    orp = EZO_ORP(bus=bus, lowpower=False)

    #print('Device Information (sensor type, firmware version): ' + orp.device_information())
    #print('Status: ' + orp.status())
    print('Supply voltage: {:.3f}V'.format(orp.supply_v()))

    while True:
        print('{} mV'.format(orp.read()))
