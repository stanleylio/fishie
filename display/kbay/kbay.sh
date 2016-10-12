#!/bin/bash

clear

input=/home/nuc/data/base-004/log/tsraw.txt
output_dir=/var/www/uhcm/img/kbay

cat $input | grep -a kph1 > $output_dir/monty.txt
cat $input | grep -a kph2 > $output_dir/coco.txt

python vbattplot.py $output_dir/monty.txt
python vbattplot.py $output_dir/coco.txt
