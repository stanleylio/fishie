from sqlalchemy import Table,Column,MetaData,Integer
from sqlalchemy.types import Float,String
from sqlalchemy.ext.declarative import declarative_base
from os.path import expanduser


Base = declarative_base()


class node_001_Sample(Base):
    __tablename__ = 'node_001'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    P_180 = Column('P_180',Float(precision=32))
    T_180 = Column('T_180',Float(precision=32))
    P_5803 = Column('P_5803',Float(precision=32))
    T_5803 = Column('T_5803',Float(precision=32))
    #ec = Column('ec',Float(precision=32))
    #sal = Column('sal',Float(precision=32))
    O2Concentration = Column('O2Concentration',Float(precision=32))
    AirSaturation = Column('AirSaturation',Float(precision=32))
    Temperature = Column('Temperature',Float(precision=32))
    CalPhase = Column('CalPhase',Float(precision=32))
    TCPhase = Column('TCPhase',Float(precision=32))
    C1RPh = Column('C1RPh',Float(precision=32))
    C2RPh = Column('C2RPh',Float(precision=32))
    C1Amp = Column('C1Amp',Float(precision=32))
    C2Amp = Column('C2Amp',Float(precision=32))
    RawTemp = Column('RawTemp',Float(precision=32))

    def __repr__(self):
        return str(self.__dict__)


class node_003_Sample(Base):
    __tablename__ = 'node_003'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    P_5803 = Column('P_5803',Float(precision=32))
    T_5803 = Column('T_5803',Float(precision=32))
    EC_4319A = Column('EC_4319A',Float(precision=32))
    T_4319A = Column('T_4319A',Float(precision=32))
    Chlorophyll_FLNTU = Column('Chlorophyll_FLNTU',Float(precision=32))
    Turbidity_FLNTU = Column('Turbidity_FLNTU',Float(precision=32))
    O2_4330F = Column('O2_4330F',Float(precision=32))
    Air_4330F = Column('Air_4330F',Float(precision=32))
    T_4330F = Column('T_4330F',Float(precision=32))

    def __repr__(self):
        return str(self.__dict__)

    
class node_004_Sample(Base):
    __tablename__ = 'node_004'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    P_180 = Column('P_180',Float(precision=32))
    T_180 = Column('T_180',Float(precision=32))
    P_5803 = Column('P_5803',Float(precision=32))
    T_5803 = Column('T_5803',Float(precision=32))
    #ec = Column('ec',Float(precision=32))
    #sal = Column('sal',Float(precision=32))
    O2Concentration = Column('O2Concentration',Float(precision=32))
    AirSaturation = Column('AirSaturation',Float(precision=32))
    Temperature = Column('Temperature',Float(precision=32))
    CalPhase = Column('CalPhase',Float(precision=32))
    TCPhase = Column('TCPhase',Float(precision=32))
    C1RPh = Column('C1RPh',Float(precision=32))
    C2RPh = Column('C2RPh',Float(precision=32))
    C1Amp = Column('C1Amp',Float(precision=32))
    C2Amp = Column('C2Amp',Float(precision=32))
    RawTemp = Column('RawTemp',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)


class node_007_Sample(Base):
    __tablename__ = 'node_007'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    P_180 = Column('P_180',Float(precision=32))
    T_180 = Column('T_180',Float(precision=32))
    P_280 = Column('P_280',Float(precision=32))
    T_280 = Column('T_280',Float(precision=32))
    RH_280 = Column('RH_280',Float(precision=32))
    UV_Si1145 = Column('UV_Si1145',Float(precision=32))
    IR_Si1145 = Column('IR_Si1145',Float(precision=32))
    Amb_Si1145 = Column('Amb_Si1145',Float(precision=32))
    Wind_average = Column('Wind_average',Float(precision=32))
    Wind_gust = Column('Wind_gust',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)
    

class node_008_Sample(Base):
    __tablename__ = 'node_008'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    d2w = Column('d2w',Float(precision=32))
    VbattmV = Column('VbattmV',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)
    
    
class node_009_Sample(Base):
    __tablename__ = 'node_009'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    d2w = Column('d2w',Float(precision=32))
    VbattmV = Column('VbattmV',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)
    
    
class node_010_Sample(Base):
    __tablename__ = 'node_010'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    d2w = Column('d2w',Float(precision=32))
    Vbatt = Column('Vbatt',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)
    

class node_011_Sample(Base):
    __tablename__ = 'node_011'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    d2w = Column('d2w',Float(precision=32))
    VbattmV = Column('VbattV',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)
    

class node_012_Sample(Base):
    __tablename__ = 'node_012'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    d2w = Column('d2w',Float(precision=32))
    VbattmV = Column('VbattV',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    
    def __repr__(self):
        return str(self.__dict__)
    

class node_021_Sample(Base):
    __tablename__ = 'node_021'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    Vbatt = Column('Vbatt',Float(precision=32))
    DATE = Column('DATE',Float(precision=32))
    TIME = Column('TIME',Float(precision=32))
    PH_INT = Column('PH_INT',Float(precision=32))
    PH_EXT = Column('PH_EXT',Float(precision=32))
    TEMP = Column('TEMP',Float(precision=32))
    TEMP_CTD = Column('TEMP_CTD',Float(precision=32))
    S_CTD = Column('S_CTD',Float(precision=32))
    O_CTD = Column('O_CTD',Float(precision=32))
    P_CTD = Column('P_CTD',Float(precision=32))
    Vrs_FET_INT = Column('Vrs_FET_INT',Float(precision=32))
    Vrs_FET_EXT = Column('Vrs_FET_EXT',Float(precision=32))
    V_THERM = Column('V_THERM',Float(precision=32))
    V_SUPPLY = Column('V_SUPPLY',Float(precision=32))
    I_SUPPLY = Column('I_SUPPLY',Float(precision=32))
    HUMIDITY = Column('HUMIDITY',Float(precision=32))
    V_5V = Column('V_5V',Float(precision=32))
    V_MBATT = Column('V_MBATT',Float(precision=32))
    V_ISO = Column('V_ISO',Float(precision=32))
    V_ISOBATT = Column('V_ISOBATT',Float(precision=32))
    I_B = Column('I_B',Float(precision=32))
    I_K = Column('I_K',Float(precision=32))
    V_K = Column('V_K',Float(precision=32))
    STATUS = Column('STATUS',String(16))
    
    def __repr__(self):
        return str(self.__dict__)
    

class node_022_Sample(Base):
    __tablename__ = 'node_022'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    Vbatt = Column('Vbatt',Float(precision=32))
    DATE = Column('DATE',Float(precision=32))
    TIME = Column('TIME',Float(precision=32))
    PH_INT = Column('PH_INT',Float(precision=32))
    PH_EXT = Column('PH_EXT',Float(precision=32))
    TEMP = Column('TEMP',Float(precision=32))
    TEMP_CTD = Column('TEMP_CTD',Float(precision=32))
    S_CTD = Column('S_CTD',Float(precision=32))
    O_CTD = Column('O_CTD',Float(precision=32))
    P_CTD = Column('P_CTD',Float(precision=32))
    Vrs_FET_INT = Column('Vrs_FET_INT',Float(precision=32))
    Vrs_FET_EXT = Column('Vrs_FET_EXT',Float(precision=32))
    V_THERM = Column('V_THERM',Float(precision=32))
    V_SUPPLY = Column('V_SUPPLY',Float(precision=32))
    I_SUPPLY = Column('I_SUPPLY',Float(precision=32))
    HUMIDITY = Column('HUMIDITY',Float(precision=32))
    V_5V = Column('V_5V',Float(precision=32))
    V_MBATT = Column('V_MBATT',Float(precision=32))
    V_ISO = Column('V_ISO',Float(precision=32))
    V_ISOBATT = Column('V_ISOBATT',Float(precision=32))
    I_B = Column('I_B',Float(precision=32))
    I_K = Column('I_K',Float(precision=32))
    V_K = Column('V_K',Float(precision=32))
    STATUS = Column('STATUS',String(16))
    
    def __repr__(self):
        return str(self.__dict__)
    
    
class node_025_Sample(Base):
    __tablename__ = 'node_025'
    id = Column('id',Integer,primary_key=True)
    ReceptionTime = Column('ReceptionTime',Float(precision=32))
    Timestamp = Column('Timestamp',Float(precision=32))
    ticker = Column('ticker',Float(precision=32))
    Vbatt = Column('Vbatt',Float(precision=32))
    salinity_seabird = Column('salinity_seabird',Float(precision=32))
    pressure_seabird = Column('pressure_seabird',Float(precision=32))
    temperature_seabird = Column('temperature_seabird',Float(precision=32))
    conductivity_seabird = Column('conductivity_seabird',Float(precision=32))
    v0_seabird = Column('v0_seabird',Float(precision=32))
    dt_seabird = Column('dt_seabird',String(19))
    sn_seabird = Column('sn_seabird',String(16))

    def __repr__(self):
        return str(self.__dict__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#dbname = 'uhcm'
engine = create_engine('mysql+mysqldb://root:' + open(expanduser('~/mysql_cred')).read().strip() + '@localhost/uhcm',
                       pool_recycle=3600,
                       echo=False)
#engine.execute('CREATE DATABASE IF NOT EXISTS ' + dbname)
#engine.execute('USE ' + dbname)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def addSample(s):
    session.add(s)
    session.commit()

