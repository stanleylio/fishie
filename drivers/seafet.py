import sys,traceback
sys.path.append('..')
from helper import dt2ts
from datetime import datetime,timedelta


# So two clarifications:
#   1. "The sum of all bytes" refers to everything before the "checksum" (so including the last comma;
#   2. The "checksum" field is not treated as "bytes" (8-bit characters) but instead as an integer.
def check_line(m):
    try:
        return 0 == (sum([ord(tmp) for tmp in m[0:m.rfind(',')+1]]) +
                     int(m.split(',')[-1])) % 256
    except:
        return False


tags = 'HEADER,DATE,TIME,PH_INT,PH_EXT,TEMP,TEMP_CTD,S_CTD,O_CTD,P_CTD,Vrs_FET_INT,Vrs_FET_EXT,V_THERM,V_SUPPLY,I_SUPPLY,HUMIDITY,V_5V,V_MBATT,V_ISO,V_ISOBATT,I_B,I_K,V_K,STATUS,CHECK SUM'
tags = tags.split(',')

def parse_SeaFET(line):
    try:
        if len(line) > 197:    # the doc says so
            return None

        m = line.strip().split(',')
        
        if check_line(line.strip()):
            d = dict(zip(tags,m))
            for k in tags:
                if k not in ['CHECK SUM','STATUS','HEADER','DATE']:
                    d[k] = float(d[k])
                #else:
                #    del d[k]
            # "instrument time"
            d['Timestamp'] = dt2ts(datetime.strptime(d['DATE'],'%Y%j') + timedelta(hours=d['TIME']))
            return d

        if 8 == len(m) and m[0] in ['kph1','kph2','kph3']:
            return {'tag':m[0],'tx_id':float(m[1]),'bad_char_count':float(m[2]),
                    'ticker':float(m[3]),'last_transmitted':float(m[4]),
                    'last_received':float(m[5]),'Vcc':float(m[6]),'Vbatt':m[7]}
        #elif 3 == len(m) and m[0].startswith('kph'):
            #return {'tag':m[0],'ticker':int(m[1]),'Vbatt':float(m[2])}
    except:
        traceback.print_exc()
        #pass
    return None


if '__main__' == __name__:
    #line = 'SATPHA0381,2016140,22.6361427,6.74344,6.28063,22.6203,22.5845,0.0111,5.801,nan,-1.03704423,-1.01856291,0.80557853,9.944,72,6.1,4.898,11.855,6.143,5.928,0,10,0.00000000,0x0000,148'
    #line = 'kph1,6318,303'
    #line = 'asdfaswlefjuawo;fj'
    #line = 'kph2,4,4.526'
    #line = 'kph2,25,0,3600,3266,3264,3.248,4.670'
    #line = 'kph2,27897,23,4181400,4181245,4181243,3.243,4.215'
    line = 'SATPHA0371,2016306,8.2669678,7.96194,7.99229,24.4627,24.2046,34.2334,4.413,nan,-0.97720563,-0.92704624,0.76134235,9.847,40,22.1,4.939,9.752,6.175,5.780,298,10,0.00000000,0x0000,229'
    d = parse_SeaFET(line)
    
    if d is not None:
        if 'HEADER' in d and 'SATPHA0381' == d['HEADER']:
            d['node'] = 'node-021'
        elif 'tag' in d and 'kph1' == d['tag']:
            d['node'] = 'node-021'
        elif 'tag' in d and 'kph2' == d['tag']:
            d['node'] = 'node-022'
        #elif 'tag' in d and 'kph3' == d['tag']:
            #d['node'] = 'node-023'

    #print d.keys()
    #print d['node']
    for k,v in d.iteritems():
        print k,v
