
-- node #4
--Timestamp,EZO_EC,EZO_Sal,EZO_DO,EZO_pH,EZO_ORP,Pressure_BMP180,Temp_BMP180,Pressure_MS5803,Temp_MS5803,WindSpeed,UV_Si1145,IR_Si1145,Amb_Si1145

-- aanderaa 4330f
--O2Concentration,AirSaturation,Temperature,CalPhase,TCPhase,C1RPh,C2RPh,C1Amp,C2Amp,RawTemp

-- aanderaa 3835
--Oxygen,Saturation,Temperature

--.read add_coilumn.sql

.schema
SELECT * FROM node_003 ORDER BY Timestamp DESC LIMIT 3;

ALTER TABLE node_003 ADD Pressure_MS5803 REAL;
ALTER TABLE node_003 ADD Temp_MS5803 REAL;

-- SQLite does NOT support DROP COLUMN so this won't work:
--ALTER TABLE node_004 DROP COLUMN O2Concentration;

.schema
SELECT * FROM node_003 ORDER BY Timestamp DESC LIMIT 3;

