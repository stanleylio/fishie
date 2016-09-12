#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import sys,traceback,re,json,importlib
from datetime import datetime
from z import check
from drivers.seafet import parse_SeaFET
from drivers.seabird import parse_Seabird


def PRINT(s):
    pass
    #print(s)


def pretty_print(d):
    """Pretty-print to terminal the given dictionary of readings"""
    # print the units as well? nah...
    max_len = max([len(k) for k in d.keys()])
    print '= '*(max_len + 4)
    if 'node' in d.keys():
        print 'From {}:'.format(d['node'])
        #print 'From node-{:03d}:'.format(d['node-id'])
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
    for k in [k for k in sorted(d.keys()) if all([k != t for t in ['Timestamp','node','ReceptionTime']])]:
        print '{}{}{}'.format(k,' '*(max_len + 4 - len(k)),d[k])


def parse_message(line):
    """Identify the origin of a given message;
parse into dict() if it's from a known node."""
    try:
        line = line.strip()

        # is it one of the ultrasonic tide gauge?        
        if re.match('^us\d+,.+',line):
            try:
                line = line.split(',')
                if 'us1' == line[0]:
                    d = {'node':'node-008',
                         'ticker':int(line[1]),
                         'd2w':float(line[2]),
                         'VbattmV':int(line[3])}
                    return d
                elif 'us2' == line[0]:
                    d = {'node':'node-009',
                         'ticker':int(line[1]),
                         'd2w':float(line[2]),
                         'VbattmV':int(line[3])}
                    return d
                elif 'us3' == line[0]:
                    d = {'node':'node-010',
                         'ticker':int(line[1]),
                         'd2w':float(line[2]),
                         'VbattmV':int(line[3])}
                    return d
            except:
                PRINT('Not a ultrasonic message:')
                PRINT(line)

        # is it one of the SeaFET pH sensors?
        d = parse_SeaFET(line)
        if d is not None:
            if ('HEADER' in d and 'SATPHA0358' == d['HEADER']) or ('tag' in d and 'kph1' == d['tag']):
                d['node'] = 'node-021'  # Monty @ Site #13
                return d
            if ('HEADER' in d and 'SATPHA0371' == d['HEADER']) or ('tag' in d and 'kph2' == d['tag']):
                d['node'] = 'node-022'  # Coco @ Site #4
                return d
            if ('HEADER' in d and 'SATPHA0381' == d['HEADER']) or ('tag' in d and 'kph3' == d['tag']):
                d['node'] = 'node-023'  # in Glazer Lab
                return d
        else:
            PRINT('Not a SeaFET message:')
            PRINT(line)

        # is it a Seabird CTD?
        d = parse_Seabird(line)
        if d is not None:
            if ('sn' in d and d['sn'] == '01607354') or ('tag' in d and 'seabird1' == d['tag']):
                node_id = 'node-025'
                from config import node
                node = importlib.import_module('config.{}.{}'.format(node.site,node_id.replace('-','_')))

                # this:
                #d = {c['dbtag']:d[c['comtag']] for c in node.conf}
                # turned into this:
                tmp = {}
                for c in node.conf:
                    if c['dbtag'] in d:     # for the uC msg
                        tmp[c['dbtag']] = d[c['dbtag']]
                    elif c['comtag'] is not None and c['comtag'] in d:  # for seabird sensor msg
                        tmp[c['dbtag']] = d[c['comtag']]
                d = tmp
                # ... because seabird is a hybrid: most fields have comtag (sal), few don't (e.g. Vbatt).
                d['node'] = node_id
                return d
            '''if ('sn' in d and d['sn'] == '???????') or ('tag' in d and 'seabird2' == d['tag']):
                node_id = 'node-026'
                from config import node
                node = importlib.import_module('config.{}.{}'.format(node.site,node_id.replace('-','_')))
                d = {c['dbtag']:d[c['comtag']] for c in node.conf}
                d['node'] = node_id
                return d'''

        # is it from one of the Beaglebone nodes?        
        if check(line):
            line = line[:-8]
            tmp = json.loads(line)
            if re.match('^node[-_]\d{3}$',tmp['from']):
                node_id = tmp['from']
                d = tmp['payload']
                d['ts'] = datetime.fromtimestamp(d['ts'])

# what a mess.
                from config import node
                node = importlib.import_module('config.{}.{}'.format(node.site,node_id.replace('-','_')))

                d = {c['dbtag']:d[c['comtag']] for c in node.conf}
                d['node'] = node_id
# If RF isolation cannot be guaranteed, node transmissions should carry site ID as well. But (site-id,node-id)
# is the same as having a wider field of just node-id. There is no risk of running out of IDs. So...
# just make all node having unique node-ID. "Site (ID)" is just for webpage display.

# Also, parse_message() can still parse messages from all sites. If a node is not defined in the database it
# will just be ignored by the db.
                return d
            elif re.match('^base[-_]\d{3}$',tmp['from']):
                PRINT('Command from base station {}; ignore.'.format(tmp['from']))
            else:
                PRINT('Not a BBB node message:')
                PRINT(line)
        else:
            PRINT('CRC failed as a BBB node message:')
            PRINT(line)
    except:
        PRINT('parse_message(): duh')
        PRINT(line)
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
    t13 = '{"from":"node-004","payload":{"C2Amp":1180.9,"T_180":34.7,"T_4330f":36.386,"sal":0.0,"T_5803":34.69,"TCPhase":27.952,"ts":1444958592.790913,"ec":7.28,"Air":90.86,"C2RPh":4.402,"P_180":101664,"P_5803":101.57,"C1RPh":32.354,"CalPhase":25.823,"C1Amp":702.4,"RawTemp":-295.9,"O2":192.554}}e002b5aa'
    t14 = '{"to":"base","from":"node_003","payload":{"Thermistor_FLNTU":533,"Temp_MS5803":25.9,"C2Amp_4330f":457.8,"O2Concentration_4330f":355.968,"C1RPh_4330f":30.444,"Chlorophyll_FLNTU":210,"Pressure_MS5803":111.87,"RawTemp_4330f":80.0,"AirSaturation_4330f":142.241,"Turbidity_FLNTU":563,"Timestamp":1444965312.228783,"Temperature_4330f":26.599,"C1Amp_4330f":255.7,"CalPhase_4330f":22.899,"TCPhase_4330f":26.351,"C2RPh_4330f":4.093}}457b3a41'

    #print parse_message(t13)
    #print parse_message(t14)

    print parse_message('kph2,27,4.785')
    
