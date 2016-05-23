import sys,traceback


def parse_SeaFET(m):
    tags = 'HEADER,DATE,TIME,PH_INT,PH_EXT,TEMP,TEMP_CTD,S_CTD,O_CTD,P_CTD,Vrs(FET|INT),Vrs(FET|EXT),V_THERM,V_SUPPLY,I_SUPPLY,HUMIDITY,V_5V,V_MBATT,V_ISO,V_ISOBATT,I_B,I_K,V_K,STATUS,CHECK SUM'
    tags = tags.split(',')
    try:
        if len(m) > 197:
            # the doc says so
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
        elif 3 == len(m) and m[0].startswith('kph'):
            return {'tag':m[0],'ticker':int(m[1]),'VbattmV':int(m[2])}
        return None
    except:
        traceback.print_exc()
        return None


if '__main__' == __name__:
    line = 'SATPHA0381,2016140,22.6361427,6.74344,6.28063,22.6203,22.5845,0.0111,5.801,nan,-1.03704423,-1.01856291,0.80557853,9.944,72,6.1,4.898,11.855,6.143,5.928,0,10,0.00000000,0x0000,148'
    
    d = parse_SeaFET(line)
    print d
    if d is not None and 'SATPHA0381' == d['HEADER']:
        print 'node-021'

    line = 'kph1,6318,303'
    d = parse_SeaFET(line)
    print d

    {'kph1':'node-021','kph2':'node-022','kph3':'node-023','SATPHA0381':'node-021'}





