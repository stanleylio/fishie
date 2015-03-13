from ezo_ec import EZO_EC
from ezo_do import EZO_DO
from ezo_ph import EZO_pH
from ezo_orp import EZO_ORP

# put the EZO sensors to sleep

# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

if '__main__' == __name__:
    with EZO_EC() as ec,\
         EZO_DO() as do,\
         EZO_pH() as ph,\
         EZO_ORP() as orp:

        print 'Supply voltage of'
        print 'EC, DO, pH, ORP in V'
        print [ec.supply_v(),do.supply_v(),ph.supply_v(),orp.supply_v()]
        
        ec.sleep()
        do.sleep()
        ph.sleep()
        orp.sleep()
        
