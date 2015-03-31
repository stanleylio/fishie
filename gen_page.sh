#/bin/bash

python gen_page.py
#cp -r ./www /var
rsync -avh --progress ./www/ /var/www
