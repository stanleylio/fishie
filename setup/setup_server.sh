#!/bin/bash

# Install Apache web server
# Again, it's more involved than this.
echo "Installing Apache"
echo "(require manual configuration... for now.)"
#apt-get install php5-common libapache2-mod-php5 php5-cli php5-sqlite -y
nano /etc/apache2/ports.conf
#port
nano /etc/apache2/sites-enabled/000-default
#AddHandler cgi-script .cgi .py
a2ensite default
a2enmod cgi
#service apache2 reload
service apache2 restart
#apachectl graceful

#sudo usermod -a -G nuc www-data
#sudo usermod -a -G www-data nuc
#sudo chmod g+w sensor_data.db
