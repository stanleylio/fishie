# Driver for the Atlas Scientific EZO DO (Dissolved Oxygen) sensor
#
# <IMPORTANT>
# SENSOR COMES IN SERIAL MODE. SWITCH TO I2C MODE TO USE WITH BBB
#
# See P.31 of the data sheet for instruction
# Notice on Step 5: "remove the short..." THIS MUST BE DONE WHILE THE LED is still BLUE
# </IMPORTANT>
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
from .ezo import EZO
import time, logging, json
from os.path import join, dirname


logger = logging.getLogger(__name__)


# Communication handler for the EZO DO sensor
# S, P and T values are synced to the sensor during instantiation. They can
# also be changed during runtime.
# Sensor is programmed to sleep between commands by default. Disable the
# lowpower mode if the LED is need for debugging purpose.
class EZO_DO(EZO):

    # need to think it through. I want to the methods to return the units as well, but
    # I also want to be able to get just the units without instantiating a class
    units = {'read':'mg/L', 'read_uM':'uM'}
    # but really, should be able to query the nodes for units too...
    # plotting and processing code shouldn't need to know the existence of THIS driver script.

    def __init__(self, address=0x61, lowpower=False, bus=1):
        EZO.__init__(self, address=address, bus=bus, lowpower=lowpower)
        
        t = None
        configfn = join(dirname(__file__), 'ezo.json')
        try:
            t = json.load(open(configfn))['ezo_do_t_celsius']
            self.t(t)
            logger.info('T value synced to {} Deg.C'.format(t))
        except:
            logger.exception('Error loading config file.')
        if t is None:
            logger.warning('T value not synced.')

        s = None
        configfn = join(dirname(__file__), 'ezo.json')
        try:
            s = json.load(open(configfn))['ezo_do_s_uS']
            self.s(s, ppt=False)
            logger.info('S value synced to {} uS/cm'.format(s))
        except:
            logger.exception('Error loading config file.')
        if s is None:
            logger.warning('S value not synced.')

        p = None
        configfn = join(dirname(__file__), 'ezo.json')
        try:
            p = json.load(open(configfn))['ezo_do_p_kPa']
            self.p(p, ppt=False)
            logger.info('P value synced to {} kPa'.format(p))
        except:
            logger.exception('Error loading config file.')
        if p is None:
            logger.warning('P value not synced.')

    # see P.38
    # in mg/L
    def read(self):
        tmp = self._r('R').strip().split(',')
        if self.lowpower:
            self.sleep()
        return float(tmp[0])

    # in uM
    # if a reading is passed, return it after unit conversion
    # not used. even with this function, the plotting code will still need to be customized
    # to know to use this function.
    def read_uM(self, val=None):
        if val is None:
            val = self.read()
        return val/32e-3

    def pretty(self, r=None):
        if r is None:
            r = self.read()
        return '{:.02f}mg/L or {:.02f}uM'.format(r, r/32e-3)

    # see P.40
    # return a tuple, (value,is_ppt)
    # is_ppt is True if the unit is part per thousand, False if the unit is microsiemens
    def s(self, new=None, ppt=False):
        tmp = self._r('S,?', 0.3)
        if tmp.startswith('?S,'):
            tmp = tmp.strip().split(',')
            current = float(tmp[1])
            # to distinguish 37.5 ppt from 37.5 microsiemens - just in case.
            wasppt = (3 == len(tmp) and 'ppt' == tmp[2])
            if new is None:         # it's just a read
                if self.lowpower:
                    self.sleep()
                return current, wasppt
            elif current != new or ppt != wasppt:
                if ppt:     # in part per thousand
                    logger.info('update current S = {} to new S = {} ppt'.format(current, new))
                    self._r('S,{},PPT'.format(new), 0.3) # ignore the response
                else:       # in microsiemens. integer only
                    if new != int(new):
                        new = int(new)
                        logger.debug('EZO_DO: integer only when in microsiemens (round to {}us)'.format(new))
                    logger.info('update current S = {} to new S = {} us'.format(current, new))
                    self._r('S,{}'.format(new), 0.3)     # ignore the response
            else:
                logger.debug('EZO_DO: supplied S == current S = {}, no update required'.format(current))
        else:
            logger.error('EZO_DO: cannot retrieve S value from sensor')

        if self.lowpower:
            self.sleep()

    # see P.41
    # unit = kPa
    def p(self, new=None):
        tmp = self._r('P,?', 0.3)
        if tmp.startswith('?P,'):
            current = float(tmp.strip().split(',')[1])
            if new is None:
                if self.lowpower:
                    self.sleep()
                return current
            elif current != new:
                logger.debug('update current P = {} kPa to new P = {} kPa'.format(current, new))
                self._r('P,{:.1f}'.format(new), 0.3)    # ignore the response
                if self.lowpower:
                    self.sleep()
            else:
                logger.debug('EZO_DO: supplied P == current P = {} kPa, no update required'.format(current))
        else:
            logger.error('EZO_DO: cannot retrieve P value from sensor')
        if self.lowpower:
            self.sleep()
        
    # super() and MRO... messy.
    def t(self, new=None):
        return super(EZO_DO, self).t(new, from_='EZO_DO: ')


if '__main__' == __name__:

    bus = 1

    logging.basicConfig(level=logging.WARNING)
    
    do = EZO_DO(bus=1, lowpower=False)
    
    #print('Device Information (sensor type, firmware version): ' + do.device_information())
    #print('Status: ' + do.status())
    print('Supply voltage: {:.3f}V'.format(do.supply_v()))
    print('Current T value (configuration parameter, not measured): {:.1f} Deg.C'.format(do.t()))
    print('Current P value (configuration parameter, not measured): {:.1f} kPa'.format(do.p()))
    tmp = do.s()
    print('Current S value (configuration parameter, not measured):', end='')
    if tmp[1]:
        print('{:.2f} ppt'.format(tmp[0]))
    else:
        print('{:.1f} uS/cm'.format(tmp[0]))
    
    while True:
        do.pretty()
