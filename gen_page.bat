
echo off

REM see dbtag in capture_config.ini

REM python gen_plot.py -i 4 -v Temp_BMP180 -p ./www/node_004
REM python gen_plot.py -i 4 -v Pressure_BMP180 -p ./www/node_004
REM python gen_plot.py -i 4 -v Temp_MS5803 -p ./www/node_004
REM python gen_plot.py -i 4 -v Pressure_MS5803 -p ./www/node_004
REM python gen_plot.py -i 4 -v Amb_Si1145 -p ./www/node_004
REM python gen_plot.py -i 4 -v IR_Si1145 -p ./www/node_004

python gen_plot.py
python gen_page.py
