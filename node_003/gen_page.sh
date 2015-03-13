#/bin/bash

#see dbtag in node_config.ini

python gen_plot.py
python gen_page.py

cp -r ./www /var
