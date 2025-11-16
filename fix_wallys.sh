#!/bin/bash

# Fix script for common issues with Wally's Monkey Parts deployment

cat << 'EOF'
If you encounter issues, run these fixes on the server:

1. Database connection errors:
ssh root@155.138.197.128
mysql -e "CREATE DATABASE IF NOT EXISTS wallys_monkey_parts;"
mysql -e "CREATE USER IF NOT EXISTS 'wallys_web'@'localhost' IDENTIFIED BY 'MonkeyWeb123!';"
mysql -e "GRANT ALL PRIVILEGES ON wallys_monkey_parts.* TO 'wallys_web'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"
mysql wallys_monkey_parts < /root/wallys_database_setup.sql

2. Permission errors:
chown -R www-data:www-data /var/www/html/wallys_*.php
chmod 644 /var/www/html/wallys_*.php
chown www-data:www-data /var/www/html/sql-lab-config.json
chmod 664 /var/www/html/sql-lab-config.json

3. Apache errors:
a2enmod php7.4 (or php8.0)
systemctl restart apache2

4. Check error logs:
tail -f /var/log/apache2/error.log

5. Test database connection:
mysql -u wallys_web -pMonkeyWeb123! wallys_monkey_parts -e "SELECT * FROM users;"

6. Enable debug mode:
Add ?debug=1 to the login URL to see SQL queries
EOF