from Adafruit_I2C import Adafruit_I2C
import time
from ConfigParser import SafeConfigParser,NoSectionError
from ezo import EZO
from os.path import join,dirname

# Driver for the Atlas Scientific EZO DO (Dissolved Oxygen) sensor


# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.31 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>


# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def PRINT(s):
    #pass
    print(s)

# Communication handler for the EZO DO sensor
# S, P and T values are synced to the sensor during instantiation. They can
# also be changed during runtime.
# Sensor is programmed to sleep between commands by default. Disable the
# lowpower mode if the LED is need for debugging purpose.
class EZO_DO(EZO):

    i2c = None
    MAX_LEN = 32
    
    def __init__(self,address=0x61,lowpower=True):

        self.i2c = Adafruit_I2C(address)
        self.address = address
        self.lowpower = lowpower
        try:
            parser = SafeConfigParser()
            parser.read(join(dirname(__file__),'ezo.ini'))
            tmp = parser.get('do','s')
            if tmp.endswith('us'):
                tmp = float(tmp[:-2])
                self.s(tmp,ppt=False)
            elif tmp.endswith('ppt'):
                tmp = float(tmp[:-3])
                self.s(tmp,ppt=True)
            else:
                PRINT('EZO_DO: invalid stuff in configuration file')
            self.p(float(parser.get('do','p')))
            self.t(round(float(parser.get('ec','t')),0))    # 0 decimal places is what the sensor actually store
        except NoSectionError:
            PRINT('EZO_DO: configuration file not found. Not syncing S,P and T value')

    # see P.38
    # mg/L
    def read(self):
        tmp = self._r('R').strip().split(',')
        if self.lowpower:
            self.sleep()
        return float(tmp[0])

    def pretty(self,r=None):
        if r is None:
            r = self.read()
        return '{:.02f}mg/L or {:.02f}uM'.format(r,r/32e-3)

    # see P.40
    # return a tuple, (value,is_ppt)
    # is_ppt is True if the unit is part per thousand, False if the unit is microsiemens
    def s(self,new=None,ppt=False):
        tmp = self._r('S,?',0.3)
        if tmp.startswith('?S,'):
            tmp = tmp.strip().split(',')
            current = float(tmp[1])
            # to distinguish 37.5 ppt from 37.5 microsiemens - just in case.
            wasppt = (3 == len(tmp) and 'ppt' == tmp[2])
            if new is None:         # it's just a read
                if self.lowpower:
                    self.sleep()
                return current,wasppt
            elif current != new or ppt != wasppt:
                if ppt:     # in part per thousand
                    PRINT('update current S = {} to new S = {} ppt'.format(current,new))
                    self._r('S,{},PPT'.format(new),0.3) # ignore the response
                else:       # in microsiemens. integer only
                    if new != int(new):
                        new = int(new)
                        PRINT('EZO_DO: integer only when in microsiemens (round to {}us)'.format(new))
                    PRINT('update current S = {} to new S = {} us'.format(current,new))
                    self._r('S,{}'.format(new),0.3)     # ignore the response
            else:
                PRINT('EZO_DO: supplied S == current S = {}, no update required'.format(current))
        else:
            PRINT('EZO_DO: cannot retrieve S value from sensor')

        if self.lowpower:
            self.sleep()

    # see P.41
    # unit = kPa
    def p(self,new=None):
        tmp = self._r('P,?',0.3)
        if tmp.startswith('?P,'):
            current = float(tmp.strip().split(',')[1])
            if new is None:
                if self.lowpower:
                    self.sleep()
                return current
            elif current != new:
                PRINT('update current P = {} kPa to new P = {} kPa'.format(current,new))
                self._r('P,{:.1f}'.format(new),0.3)    # ignore the response
                if self.lowpower:
                    self.sleep()
            else:
                PRINT('EZO_DO: supplied P == current P = {} kPa, no update required'.format(current))
        else:
            PRINT('EZO_DO: cannot retrieve P value from sensor')
        if self.lowpower:
            self.sleep()
        
    # super() and MRO... messy.
    def t(self,new=None):
        PRINT('EZO_DO:')
        return super(EZO_DO,self).t(new)


if '__main__' == __name__:
    with EZO_DO(lowpower=True) as do:
        print 'Device Information (sensor type, firmware version):'
        print do.device_information()
        print
        print 'Status:'
        print do.status()
        print
        print 'Supply voltage:'
        print '{} volt'.format(do.supply_v())
        print
        print 'Current T value (supplied for calibration, not measured):'
        print '{:.0f} Deg.C'.format(do.t())
        print
        print 'Current S value (salinity, supplied for calibration, not measured):'
        tmp = do.s()
        if tmp[1]:
            print '{} ppt'.format(tmp[0])
        else:
            print '{} us'.format(tmp[0])
        #do.s(10,ppt=True)
        #do.s(0)
        print
        print 'Current P value (water pressure, supplied for calibration, not measured):'
        print '{} kPa'.format(do.p())
        print
        #print 'Change T value to...'
        #do.t(20)      # NOT synced during instantiation
        #print
        print 'A sample read:'
        #print '{:.2f} mg/L'.format(do.read())
        print do.pretty()
        print
        #do.p(101.3)

