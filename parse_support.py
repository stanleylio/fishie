#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015
import re,time,glob
from os.path import join,exists,getmtime,dirname
from datetime import datetime,timedelta
from ConfigParser import RawConfigParser,NoSectionError
from config_support import read_config
from z import check


def PRINT(s):
    pass
    #print(s)

# for caching the capabilities of the nodes
# for efficiency (don't want to read the config file for each message received)
def read_capability():
    node_config = read_config(join(dirname(__file__),'node_config.ini'),pattern='^node_\d{3}$')
    nodes = {}

    for node in node_config.keys():
        #PRINT(node)
        node_id = int(node[5:])
        name = node_config[node]['name']
        dbtag = [c.strip() for c in node_config[node]['dbtag'].split(',')]
        dbtype = [c.strip() for c in node_config[node]['dbtype'].split(',')]
        dbunit = [c.strip() for c in node_config[node]['dbunit'].split(',')]
        msgfield = None
        try:
            msgfield = [c.strip() for c in node_config[node]['msgfield'].split(',')]
        except Exception as e:
            PRINT('read_capability(): msgfield not found (optional for node).')
        convf = None
        try:
            convf = [eval(v) for v in node_config[node]['convf'].split(',')]
        except Exception as e:
            PRINT('read_capability(): convf not found (optional for node).')

        assert len(dbtag) == len(dbtype),\
               'dbtag and dbtype should have the same length'
#        assert len(msgfield) == len(convf),\
#               'msgfield and convf should have the same length'

        nodes[node_id] = {'name':name,
                          'dbtag':dbtag,
                          'dbtype':dbtype,
                          'dbunit':dbunit,
                          'msgfield':msgfield,
                          'convf':convf}
    return nodes

# print to terminal the given dictionary of readings
def pretty_print(d):
    # print the units as well? nah...
    max_len = max([len(k) for k in d.keys()])
    print '= '*(max_len + 4)
    if 'node_id' in d.keys():
        print 'From node_{:03d}:'.format(d['node_id'])
    if 'ReceptionTime' in d.keys():
        print 'Received at {}'.format(d['ReceptionTime'])
    if 'Timestamp' in d.keys():
        print 'Sampled at {}'.format(d['Timestamp'])
    for k in [k for k in sorted(d.keys()) if all([k != t for t in ['Timestamp','node_id','ReceptionTime']])]:
        print '{}{}{}'.format(k,' '*(max_len + 4 - len(k)),d[k])
    

class NodeMessageParser(object):
    def __init__(self):
        # parse and cache the message formats of known nodes using the configuration ini file
        self.node_capability = read_capability()

    def parse_message(self,line):
        line = line.strip()
        node_id = self.id_node(line)
        if node_id is not None:
            # magic numbers are PURE EVIL
            # those optodes add so many special cases everywhere...
            if node_id in [1,2]:
                d = self.parse_3835(line,node_id=node_id)
            else:
                if check(line):
                    d = self.parse_bbb_node(line)
                else:
                    PRINT('NodeMessageParser::parse_message(): CRC error: ' + line)
            # bonus: node_id
            if d is not None:
                d['node_id'] = node_id
                return d
            else:
                return None
        else:
            PRINT('NodeMessageParser::parse_message(): unknown message: ' + line)
            return None

    # hard-coded magic stuff everywhere...
    def id_node(self,line):
        line = line.strip()
        try:
            if re.match('^node_\d{3}',line):
                return int(line[5:8])
            # in a perfect world, this ends here
            elif all(w in line for w in ['MEASUREMENT','3835','505']):
                return 1
            elif all(w in line for w in ['MEASUREMENT','3835','506']):
                return 2
            elif all(w in line for w in ['MEASUREMENT','4330F','829']):
                return 3
            else:
                return None
        except Exception as e:
            PRINT('NodeMessageParser::id_node(): error identifying: ' + line)
            PRINT(e)
            return None

    # parse a BBB node message
    def parse_bbb_node(self,line):
        line = line.strip()
        node_id = int(line[5:8])
        
        fields = line.split(',')[1:]        # omit the 'node_nnn' field
        # would be nice to define a conversion function for the node_nnn field as well...
        msgfield = self.node_capability[node_id]['msgfield']
        convf = self.node_capability[node_id]['convf']
        assert len(msgfield) == len(fields),'msgfield and fields should have the same length'
        assert len(fields) == len(convf),'fields and convf should have the same length'

        d = {}
        try:
            d['node_id'] = node_id
            for p in zip(msgfield,fields,convf):
                d[p[0]] = p[2](p[1])
        except:
            PRINT('parse_support:parse_bbb_node(): error parsing {}'.format(line))
            pass
        return d

    # I hate these magic functions. mixing domain-specific information with the control
    # logic is always bad.
    def parse_4330f(self,line,node_id=None):

# 1. this shouldn't be here at all. this function is for parsing messages from the 4330f
# it shoudn't concern itself with node id.
        if node_id is None:
            node_id = self.id_node(line)

# 2. if this is specifically designed for 4330f, then these should be included in this
# function and not be in the config file - it's not like the messages format is going to
# change and the user needs to update the config file often.
        cols = self.node_capability[node_id]['msgfield']
        convf = self.node_capability[node_id]['convf']

        d = None
        try:
            line = line.strip()
            r = '.*MEASUREMENT\s+4330F\s+(?P<SN>\d+)\s+' +\
                  'O2Concentration\(uM\)\s+(?P<O2Concentration>[+-]*\d+\.*\d*)\s+' +\
                  'AirSaturation\(\%\)\s+(?P<AirSaturation>[+-]*\d+\.*\d*)\s+' +\
                  'Temperature\(Deg\.C\)\s+(?P<Temperature>[+-]*\d+\.*\d*)\s+' +\
                  'CalPhase\(Deg\)\s+(?P<CalPhase>[+-]*\d+\.*\d*)\s+' +\
                  'TCPhase\(Deg\)\s+(?P<TCPhase>[+-]*\d+\.*\d*)\s+' +\
                  'C1RPh\(Deg\)\s+(?P<C1RPh>[+-]*\d+\.*\d*)\s+' +\
                  'C2RPh\(Deg\)\s+(?P<C2RPh>[+-]*\d+\.*\d*)\s+' +\
                  'C1Amp\(mV\)\s+(?P<C1Amp>[+-]*\d+\.*\d*)\s+' +\
                  'C2Amp\(mV\)\s+(?P<C2Amp>[+-]*\d+\.*\d*)\s+' +\
                  'RawTemp\(mV\)\s+(?P<RawTemp>[+-]*\d+\.*\d*).*'
            r = re.match(r,line)
            if r is not None:
                d = {}
                for k,c in enumerate(cols):
                    d[c] = convf[k](r.group(c))
        except Exception as e:
            PRINT('parse_4330f(): cannot parse: {}'.format(line))
            PRINT(e)
        return d

    def parse_3835(self,line,node_id=None):
        if node_id is None:
            node_id = self.id_node(line)
        
        cols = self.node_capability[node_id]['msgfield']
        convf = self.node_capability[node_id]['convf']

        d = None
        try:
            line = line.strip()
            r = '.*MEASUREMENT\s+3835\s+(?P<SN>\d+)\s+' +\
                  'Oxygen\:\s+(?P<Oxygen>[+-]*\d+\.*\d*)\s+' +\
                  'Saturation\:\s+(?P<Saturation>[+-]*\d+\.*\d*)\s+' +\
                  'Temperature\:\s+(?P<Temperature>[+-]*\d+\.*\d*).*'
            r = re.match(r,line)
            if r is not None:
                d = {}
                for k,c in enumerate(cols):
                    d[c] = convf[k](r.group(c))
        except Exception as e:
            PRINT('parse_3835(): cannot parse: {}'.format(line))
            PRINT(e)
        return d


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

    nmp = NodeMessageParser()

    print '- - - - -'
    print nmp.id_node(t1)
    print nmp.id_node(t2)
    print nmp.id_node(t3)
    print nmp.id_node(t4)
    print nmp.id_node(t5)
    print nmp.id_node(t6)
    print nmp.id_node(t7)
    print nmp.id_node(t8)
    print nmp.id_node(t9)

#    print '- - - - -'
#    t = t6
#    print t
#    p = nmp.parse_4330f(t)
#    print '- - -'
#    for k,v in enumerate(p):
#        print '{}: {}'.format(v,p[v])

#    print '- - - - -'
#    print t4
#    p = nmp.parse_3835(t4)
#    for k,v in enumerate(p):
#        print '{}: {}'.format(v,p[v])

    print '- - - - -'
    print read_config('node_config.ini')

    print '- - - - -'
    print read_capability()    
