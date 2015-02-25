#/bin/bash

#see dbtag in node_config.ini

#python gen_plot.py -i 4 -v Temp_BMP180 -p ./www/node_004
#python gen_plot.py -i 4 -v Pressure_BMP180 -p ./www/node_004
#python gen_plot.py -i 4 -v Temp_MS5803 -p ./www/node_004
#python gen_plot.py -i 4 -v Pressure_MS5803 -p ./www/node_004
#python gen_plot.py -i 4 -v Amb_Si1145 -p ./www/node_004
#python gen_plot.py -i 4 -v IR_Si1145 -p ./www/node_004

python gen_plot.py
python gen_page.py

cp -r ./www /var
