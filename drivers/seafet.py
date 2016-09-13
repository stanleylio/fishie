import sys,traceback


def parse_SeaFET(m):
    tags = 'HEADER,DATE,TIME,PH_INT,PH_EXT,TEMP,TEMP_CTD,S_CTD,O_CTD,P_CTD,Vrs_FET_INT,Vrs_FET_EXT,V_THERM,V_SUPPLY,I_SUPPLY,HUMIDITY,V_5V,V_MBATT,V_ISO,V_ISOBATT,I_B,I_K,V_K,STATUS,CHECK SUM'
    tags = tags.split(',')

    # a hack+patch
    #m = ''.join([c if ord(c) < 128 else chr(ord(c) - 128) for c in m])
    #m = m[m.find('SATPHA'):]
    
    try:
        if len(m) > 197:    # the doc says so
            return None
        m = m.strip().split(',')
        if 25 == len(m) and m[23].startswith('0x'):   # can't get the "check sum" working.
            d = dict(zip(tags,m))
            for k in tags:
                if k not in ['CHECK SUM','STATUS','HEADER']:
                    d[k] = float(d[k])
                #else:
                #    del d[k]
            return d
        elif 8 == len(m) and m[0].startswith('kph'):
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
    line = 'kph2,4,4.526'
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

    print d.keys()
    print d['node']
