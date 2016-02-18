#!/bin/bash

# Install Apache web server
# Again, it's more involved than this.
echo "Installing Apache"
echo "(require manual configuration... for now.)"
apt-get install libapache2-mod-wsgi php5-common libapache2-mod-php5 php5-cli php5-sqlite -y
nano /etc/apache2/ports.conf
#port
nano /etc/apache2/sites-enabled/000-default
#AddHandler cgi-script .cgi .py
a2ensite default
service apache2 reload
apachectl graceful
