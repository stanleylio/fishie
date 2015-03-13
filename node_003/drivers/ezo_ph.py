from Adafruit_I2C import Adafruit_I2C
import time
from ConfigParser import SafeConfigParser,NoSectionError
from ezo import EZO
from os.path import join,dirname

# Driver for the Atlas Scientific EZO pH sensor


# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.29 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>


# from the experiments the sensor protocol seems fairly stable. impressive work Atlas-Sci.

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def PRINT(s):
    #pass
    print(s)

# Communication handler for the EZO pH sensor
# T value is set in the .ini file. It is sent to the sensor during
# instantiation and can be changed during runtime.
# Sensor is programmed to sleep between commands by default.
class EZO_pH(EZO):
    
    i2c = None
    MAX_LEN = 32
    
    def __init__(self,address=0x63,lowpower=True):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.lowpower = lowpower
        try:
            parser = SafeConfigParser()
            parser.read(join(dirname(__file__),'ezo.ini'))
            self.t(round(float(parser.get('ph','t')),0))
        except NoSectionError:
            PRINT('configuration file not found. Not syncing T value')

    def read(self):
        tmp = self._r('R').strip().split(',')
        if self.lowpower:
            self.sleep()
        return float(tmp[0])

    def pretty_print(self,r=None):
        if r is None:
            r = self.read()
        print 'pH = {:.2f}'.format(r)
        
    # super() and MRO... messy.
    def t(self,new=None):
        PRINT('EZO_pH:')
        return super(EZO_pH,self).t(new)


if '__main__' == __name__:
    ph = EZO_pH(lowpower=True)
    print 'Device Information (sensor type, firmware version):'
    print ph.device_information()
    print
    print 'Status:'
    print ph.status()
    print
    print 'Supply voltage:'
    print '{:.3f} volt'.format(ph.supply_v())
    print

    print 'Current T value (calibration parameter, not measured):'
    print '{:.0f} Deg.C'.format(ph.t())
    print
    #print 'Change T value to...'
    #print ph.t(25)      # NOT synced during instantiation
    #print
    print 'A sample read:'
    ph.pretty_print()
    #ph.sleep()
    
