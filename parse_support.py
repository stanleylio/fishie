#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import sys,traceback,re,json
sys.path.append('drivers')
from datetime import datetime
from z import check
from aanderaa_3835 import Aanderaa_3835

def PRINT(s):
    #pass
    print(s)

# print to terminal the given dictionary of readings
def pretty_print(d):
    # print the units as well? nah...
    max_len = max([len(k) for k in d.keys()])
    print '= '*(max_len + 4)
    if 'node_id' in d.keys():
        print 'From node_{:03d}:'.format(d['node_id'])
    if 'ReceptionTime' in d.keys():
        tmp = d['ReceptionTime']
        if isinstance(tmp,float):
            tmp = datetime.fromtimestamp(tmp)
        print 'Received at {}'.format(tmp)
    if 'Timestamp' in d.keys():
        tmp = d['Timestamp']
        if isinstance(tmp,float):
            tmp = datetime.fromtimestamp(tmp)
        print 'Sampled at {}'.format(tmp)
    for k in [k for k in sorted(d.keys()) if all([k != t for t in ['Timestamp','node_id','ReceptionTime']])]:
        print '{}{}{}'.format(k,' '*(max_len + 4 - len(k)),d[k])
    
def parse_message(line):
    try:
        line = line.strip()
        # - - - - -
        # wouldn't need id_node() if there weren't the two exceptions.
        # even forced the AAnderra driver here... they don't belong here.
        node_id = id_node(line)
        if node_id in [1,2]:
            d = Aanderaa_3835.parse_3835(line)
            if d is not None:
                d['node_id'] = id_node(line)
                return d
        # - - - - -
        # handle the BBB messages
        # BBB messages have crc32 checksums
        if check(line):
            line = line[:-8]
            tmp = json.loads(line)
            node_id = int(tmp['from'][5:8])
            d = tmp['payload']
            d['node_id'] = node_id
            d['Timestamp'] = datetime.fromtimestamp(d['Timestamp'])
            return d
        else:
            PRINT('parse_message(): CRC failure')
    except:
        PRINT('parse_message(): duh')
        PRINT(line)
        traceback.print_exc()
        return None

# handle the identification of the non-BBB nodes
# does NOT handle id-ing the BBB nodes
def id_node(line):
    line = line.strip()
    try:
        if all(w in line for w in ['MEASUREMENT','3835','505']):
            return 1
        elif all(w in line for w in ['MEASUREMENT','3835','506']):
            return 2
        else:
            return None
    except:
        PRINT('id_node(): error identifying: ' + line)
        traceback.print_exc()
        return None


if '__main__' == __name__:
    t1 = '	%# MEASUREMENT	4330F	829	O2Concentration(uM)	268.277	AirSaturation(%)	96.838	Temperature(Deg.C)	21.188	CalPhase(Deg)	27.767	TCPhase(Deg)	29.411	C1RPh(Deg)	-56.514	C2RPh(Deg)	-85.925	C1Amp(mV)	907.9	C2Amp(mV)	896.5	RawTemp(mV)	255.7'
    t2 = '%# MEASUREMENT	4330F	829	O2Concentration(uM)	268.277	AirSaturation(%)	96.838	Temperature(Deg.C)	21.188	CalPhase(Deg)	27.767	TCPhase(Deg)	29.411	C1RPh(Deg)	-56.514	C2RPh(Deg)	-85.925	C1Amp(mV)	907.9	C2Amp(mV)	896.5	RawTemp(mV)	255.7'
    t3 = '  KSDLKMF:^@#_$_gibberish*(#@&%\t  .'
    t4 = '	MEASUREMENT	  3835	   506	Oxygen: 	   251.39	Saturation: 	    91.01	Temperature: 	    21.34'
    t5 = 'MEASUREMENT	  3835	   506	Oxygen: 	   251.39	Saturation: 	    91.01	Temperature: 	    21.34'
    t6 = '	%# MEASUREMENT	4330F	829	O2Concentration(uM)	268.635	AirSaturation(%)	96.961	Temperature(Deg.C)	21.184	CalPhase(Deg)	27.754	TCPhase(Deg)	29.399	C1RPh(Deg)	33.471	C2RPh(Deg)	4.072	C1Amp(mV)	908.3	C2Amp(mV)	896.7	RawTemp(mV)	255.8'
    t7 = '	MEASUREMENT	  3835	   505	Oxygen: 	   277.17	Saturation: 	    97.14	Temperature: 	    19.70'
    t8 = '	MEASUREMENT	  3835	   599	Oxygen: 	   277.17	Saturation: 	    97.14	Temperature: 	    19.70'
    t9 = 'node_004,1424585261.082,0.0,0.0,3.4,14.0,227.9,100725,25.2,102.23,25.22,0,14,401,290,bb0e2744'
    t10 = 'node_003,1428655463.930822,271.913,100.005,22.152,27.247,29.814,33.633,3.819,315.8,466.0,224.3,2896,4121,548,fc0d9152'
    t11 = '{"from":"node_004","payload":{"Temp_MS5803":25.65,"Pressure_BMP180":101117,"Amb_Si1145":287,"EZO_ORP":-26.7,"EZO_DO":3.99,"Pressure_MS5803":102.4,"IR_Si1145":532,"Timestamp":1428690061.93023,"EZO_pH":14.0,"EZO_Sal":0.0,"Temp_BMP180":25.8,"EZO_EC":0.0,"UV_Si1145":13}}f717a449'
    t12 = 'MEASUREMENT	  3835	   599	Oxygen: 	   277.17	Saturation: 	    97.14	Temperature: 	    19.70'

