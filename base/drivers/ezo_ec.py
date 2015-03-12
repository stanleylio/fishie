from Adafruit_I2C import Adafruit_I2C
import time
from ConfigParser import SafeConfigParser,NoSectionError
from ezo import EZO
from os.path import join,dirname

# Driver for the Atlas Scientific EZO EC (Electrical Conductivity) sensor


# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.32 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>


# from the experiments the sensor protocol seems fairly reliable. impressive work Atlas-Sci.

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def PRINT(s):
    #pass
    print(s)

# Communication handler for the EZO EC sensor
# K and T values are set in the .ini file. They are sent to the sensor during
# instantiation. Both can be changed during runtime.
# Sensor is programmed to sleep between commands by default.
class EZO_EC(EZO):
    
    i2c = None
    MAX_LEN = 32
    
    def __init__(self,address=0x64,lowpower=True):
        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.lowpower = lowpower
        try:
            parser = SafeConfigParser()
            parser.read(join(dirname(__file__),'ezo.ini'))
            self.k(float(parser.get('ec','k')))
            # the sensor actually store only integer T
            self.t(round(float(parser.get('ec','t')),0))
        except NoSectionError:
            PRINT('EZO_EC: configuration file not found. Not syncing K value')

    # see P.39
    def read(self):
        tmp = self._r('R').strip().split(',')
        d = {'ec':float(tmp[0]),    # Electrical Conductivity
             'tds':float(tmp[1]),   # Total Dissolved Solids
             'sal':float(tmp[2]),   # Salinity
             'sg':float(tmp[3])}    # Specific Gravity
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
    def k(self,new=None):
        tmp = self._r('K,?',0.3)    # always do a read first
        if tmp.startswith('?K,'):
            current = float(tmp[3:7])
            if new is None:
                if self.lowpower:
                    self.sleep()
                return current
            elif current != new:
                if new >= 0.1 and new <= 10:
                    PRINT('update current K = {} to new K = {}'.format(current,new))
                    cmd = 'K,{:.2f}'.format(new)
                    self._r(cmd,0.3)    # ignore the response
                    if self.lowpower:
                        self.sleep()
                else:
                    PRINT('EZO_EC: invalid K value supplied')
            else:
                PRINT('EZO_EC: supplied K == current K = {}, no update required'.format(current))
        else:
            PRINT('EZO_EC: cannot retrieve K value from sensor')
        if self.lowpower:
            self.sleep()

    # super() and MRO... messy.
    def t(self,new=None):
        PRINT('EZO_EC:')
        return super(EZO_EC,self).t(new)

    def pretty_print(self,r=None):
        if r is None:
            r = self.read()
        print 'Electrical Conductivity: {} uS'.format(r['ec'])
        print 'Salinity: {}'.format(r['sal'])           # no defined unit, P.7
        print 'Total Dissolved Solid: {} mg/L'.format(r['tds'])
        print 'Specific Gravity: {}'.format(r['sg'])    # unitless, P.7


if '__main__' == __name__:
    with EZO_EC(lowpower=True) as ec:
        print 'Device Information (sensor type, firmware version):'
        print ec.device_information()
        print
        print 'Status:'
        print ec.status()
        print
        print 'Supply voltage:'
        print '{:.3f} volt'.format(ec.supply_v())
        print
        print 'Current K value (of probe):'
        print ec.k()
        print
        #print 'Change K value to...'
        #print ec.k(1.2)    # synced during instantiation, but can be changed during runtime
        #print
        print 'Current T value (calibration parameter, not measured):'
        print '{:.0f} Deg.C'.format(ec.t())
        print
        #print 'Change T value to...'
        #print ec.t(25)      # NOT synced during instantiation
        #print
        print 'A sample read:'
        ec.pretty_print(ec.read())
        #ec.sleep()
    
