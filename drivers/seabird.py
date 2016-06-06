import sys,traceback


def parse_Seabird(m):
    pass
    '''tags = 'HEADER,DATE,TIME,PH_INT,PH_EXT,TEMP,TEMP_CTD,S_CTD,O_CTD,P_CTD,Vrs_FET_INT,Vrs_FET_EXT,V_THERM,V_SUPPLY,I_SUPPLY,HUMIDITY,V_5V,V_MBATT,V_ISO,V_ISOBATT,I_B,I_K,V_K,STATUS,CHECK SUM'
    tags = tags.split(',')
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
        elif 3 == len(m) and m[0].startswith('seabird'):
            return {'tag':m[0],'ticker':int(m[1]),'Vbatt':int(m[2])}
    except:
        traceback.print_exc()
    return None'''


if '__main__' == __name__:
    pass
