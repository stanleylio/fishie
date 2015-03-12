from Adafruit_I2C import Adafruit_I2C
import time
from ezo import EZO

# Driver for the Atlas Scientific EZO ORP sensor


# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.25 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>


# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def PRINT(s):
    #pass
    print(s)

# Communication handler for the EZO ORP sensor
# T value is set in the .ini file. It is sent to the sensor during
# instantiation and can be changed during runtime.
# Sensor is programmed to sleep between commands by default.
class EZO_ORP(EZO):
    
    i2c = None
    MAX_LEN = 32
    
    def __init__(self,address=0x62,lowpower=True):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.lowpower = lowpower

    def read(self):
        tmp = self._r('R').strip().split(',')
        if self.lowpower:
            self.sleep()
        return float(tmp[0])

    # ORP has no T parameter - the only exception in the EZO series
    # I don't see an elegant solution to this: copy the same t() for
    # all other sensors, or make one exception in ORP here, neither
    # solution is perfect
    def t(self,new=None):
        # and no I DON'T want to call super()
        class ParameterNotDefinedError(NotImplementedError):
            pass
        raise ParameterNotDefinedError('ORP sensor does not define a T parameter')

    def pretty_print(self,r=None):
        if r is None:
            r = self.read()
        print 'orp = {:.2f} mV'.format(r)
        

if '__main__' == __name__:
    orp = EZO_ORP(lowpower=True)
    print 'Device Information (sensor type, firmware version):'
    print orp.device_information()
    print
    print 'Status:'
    print orp.status()
    print
    print 'Supply voltage:'
    print '{:.3f} volt'.format(orp.supply_v())
    print
    print 'A sample read:'
    orp.pretty_print()
    #orp.sleep()
    
