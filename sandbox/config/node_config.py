# name
# node_id (int)
# node_tag (str)

# broadcast_port
# broadcast_baud

# storage
# dbtag, dbtype, dbformat

# communication
# msgfield


config = {
    'type': 'node',
    'node_id': 4,
    'broadcast_port': '/dev/ttyO1',
    'broadcast_baud': 9600,
    'wait': 30

    
}


def read_capability():
    config = {}
    config['node'] = {'id': 4,
                      'broadcast_port': '/dev/ttyO1',
                      'broadcast_baud': 9600,
                      'wait': 30}

    dbcols = [
        ('Timestamp', 'TIMESTAMP UNIQUE', ''),
        ('EZO_EC', 'REAL', 'uS'),
        ('EZO_Sal', 'REAL', ''),
        ('EZO_DO', 'REAL', 'mg/L'),
        ('EZO_pH', 'REAL', ''),
        ('EZO_ORP', 'REAL', 'mV'),
        ('Pressure_BMP180', 'REAL', 'Pa'),
        ('Temp_BMP180', 'REAL', 'Deg.C'),
        ('Pressure_MS5803', 'REAL', 'kPa'),
        ('Temp_MS5803', 'REAL', 'Deg.C'),
        ('WindSpeed', 'REAL', 'm/s'),
        ('UV_Si1145', 'REAL', ''),
        ('IR_Si1145', 'REAL', 'lux'),
        ('Amb_Si1145', 'REAL', 'lux'),
        ('O2Concentration_4330f', 'REAL', 'uM'),
        ('AirSaturation_4330f', 'REAL', '%'),
        ('Temperature_4330f', 'REAL', 'Deg.C'),
        ('CalPhase_4330f', 'REAL', 'Deg'),
        ('TCPhase_4330f', 'REAL', 'Deg'),
        ('C1RPh_4330f', 'REAL', 'Deg'),
        ('C2RPh_4330f', 'REAL', 'Deg'),
        ('C1Amp_4330f', 'REAL', 'mV'),
        ('C2Amp_4330f', 'REAL', 'mV'),
        ('RawTemp_4330f', 'REAL', 'mV')
        ]

    tmp = zip(*dbcols)
    dbtag = tmp[0]
    dbtype = tmp[1]
    dbunit = tmp[2]
    
    config['node_004'] = {
        'msgfield': ['Timestamp','EZO_EC','EZO_Sal','EZO_DO','EZO_pH','EZO_ORP',
                     'Pressure_BMP180','Temp_BMP180','Pressure_MS5803','Temp_MS5803',
                     'WindSpeed',
                     'UV_Si1145','IR_Si1145','Amb_Si1145',
                     'O2Concentration_4330f','AirSaturation_4330f','Temperature_4330f',
                     'CalPhase_4330f','TCPhase_4330f',
                     'C1RPh_4330f','C2RPh_4330f','C1Amp_4330f','C2Amp_4330f',
                     'RawTemp_4330f',
                     'Checksum'],
        'name': 'BBB Experimental',
        'optode_port': '/dev/ttyUSB0',

        'dbtag': dbtag,
        'dbtype': dbtype,
        'dbunit': dbunit
    }
    return config





if '__main__' == __name__:

    config = read_capability()

    dbtag = config['node_004']['dbtag']
    dbtype = config['node_004']['dbtype']
    dbunit = config['node_004']['dbunit']
    assert len(dbtag) == len(dbtype)
    assert len(dbtype) == len(dbunit)

    #for a in zip(dbtag,dbtype,dbunit):
    #    print '{},'.format(str(a))

    





















