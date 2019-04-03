#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import sys, re, json, importlib, logging, binascii, time
from os.path import expanduser
sys.path.append(expanduser('~'))
from datetime import datetime
from node.z import check
from node.drivers.seafet import parse_SeaFET
from node.drivers.seabird import parse_Seabird
from node.helper import dt2ts


logger = logging.getLogger(__name__)


def pretty_print(d):
    """Pretty-print to terminal the given dictionary of readings"""
    # print the units as well? nah...
    max_len = max([len(k) for k in d.keys()])
    #print('= '*(max_len + 4))
    if 'node' in d.keys():
        print('From {}:'.format(d['node']))
        #print 'From node-{:03d}:'.format(d['node-id'])
    if 'ReceptionTime' in d.keys():
        tmp = d['ReceptionTime']
        if isinstance(tmp, float):
            tmp = datetime.fromtimestamp(tmp)
        print('Received at {}'.format(tmp))
    if 'Timestamp' in d.keys():
        tmp = d['Timestamp']
        if isinstance(tmp, float):
            tmp = datetime.fromtimestamp(tmp)
        print('Sampled at {}'.format(tmp))
    if 'ts' in d.keys():
        tmp = d['ts']
        if isinstance(tmp, float):
            tmp = datetime.fromtimestamp(tmp)
        print('Sampled at {}'.format(tmp))
    #for k in [k for k in sorted(d.keys()) if all([k != t for t in ['Timestamp','node','ReceptionTime']])]:
        #print('{}{}{}'.format(k,' '*(max_len + 4 - len(k)),d[k]))
    #what was I thinking...
    #for k in sorted(filter(lambda x: x not in ['Timestamp','node','ReceptionTime'],d.keys())):
    #what was I thinking...
    for k in sorted(set(d.keys()) - set(['Timestamp', 'node', 'ReceptionTime', 'ts'])):
        #print('{}{}{}'.format(k, ' '*(max_len + 4 - len(k)), d[k]))
        print('{{: <{}}}{{}}'.format(max_len + 4).format(k, d[k]))


def parse_message(line):
    """Identify the origin of a given message;
parse into dict() if it's from a known node."""
    try:
        line = line.strip()

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
            #logger.info('Not a SeaFET message:')
            #logger.info(line)
            pass

        # is it a Seabird CTD?
        d = parse_Seabird(line)
        if d is not None:
            if ('sn' in d and d['sn'] == '01607354') or ('tag' in d and 'seabird1' == d['tag']):
                node_id = 'node-025'
                assert 'node' not in d
                d['node'] = node_id
                return d
        else:
            #logger.info('Not a Seabird message:')
            #logger.info(line)
            pass

        # is it from one of the Beaglebone nodes?
        if check(line):
            line = line[:-8]
            tmp = json.loads(line)
            if re.match('^node[-_]\d{3}$', tmp['from']):
                node_id = tmp['from']
                d = tmp['payload']

                try:
                    #node = importlib.import_module('node.config.{}.{}'.format(get_site(node_id), node_id.replace('-', '_')))
                    #node = import_node_config(node_id)
                    #d = {c['dbtag']:d[c.get('comtag', c['dbtag'])] for c in node.conf}
                    assert 'node' not in d
                    d['node'] = node_id
                    return d
                except ImportError:
                    # the JSON messages are self-descriptive with checksum, I don't need no comtag-dbtag conversion.
                    logger.warning('config file for {} not defined'.format(node_id))
                    d['node'] = node_id
                    return d
            elif re.match('^base[-_]\d{3}$', tmp['from']):
                d = tmp.get('payload', None)
                d['node'] = tmp['from']
                if d is None:
                    logger.debug('Don\'t know what that was; ignore.'.format(tmp['from']))
                return d
            else:
                logger.debug('Not a BBB node message (unrecognized node ID):')
                logger.debug(line)
        else:
            logger.debug('Not a BBB node message (CRC failure):')
            logger.debug(line)
            #pass
    except:
        logger.warning('parse_message(): duh')
        logger.exception(line)
    return None


if '__main__' == __name__:

    logging.basicConfig(level=logging.DEBUG)
    
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

    #print parse_message('kph2,27,4.785')
    
    #t = 'node-003,R,2016-11-02 01:47:14,102.05,24.66,251.400,99.415,26.080,82.988,25.536,3055,4130,b3844b99'
    #print(parse_message(t))
    #t = 'node-003,R,2016-11-02 01:47:34,102.02,24.65,251.015,99.262,26.079,82.988,25.541,3056,4130,7ad3f9ba'
    #print(parse_message(t))
    #t = 'node-003,R,2016-11-02 01:47:54,102.10,24.65,250.859,99.191,26.074,82.988,25.555,3056,4130,029d3041'
    #print(parse_message(t))
    #t = 'node-003,R,2016-11-02 01:48:15,102.04,24.65,250.793,99.168,26.076,82.988,25.565,3056,4130,aa65fdf4'
    #print(parse_message(t))
    #t = 'node-003,R,2016-11-02 01:48:35,102.03,24.65,251.286,99.342,26.064,82.988,25.579,3056,4130,52510df2'
    #print(parse_message(t))

    print(pretty_print(parse_message(t11)))

