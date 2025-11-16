#!/bin/bash

# One-line deployment for Wally's Monkey Parts
# Following your preferred format: scp file root@server:/path/ && ssh root@server "commands"

echo "Run this command to deploy everything:"
echo ""
echo 'scp /Users/walterbarr_1/sql-injection-lab/wallys_database_setup.sql root@155.138.197.128:/root/ && scp /Users/walterbarr_1/sql-injection-lab/wallys_*.php root@155.138.197.128:/var/www/html/ && ssh root@155.138.197.128 "mysql < /root/wallys_database_setup.sql && chown www-data:www-data /var/www/html/wallys_*.php && chmod 644 /var/www/html/wallys_*.php && echo '"'"'{"lab_enabled":true,"last_modified":"2024-01-01","modified_by":"system"}'"'"' > /var/www/html/sql-lab-config.json && chown www-data:www-data /var/www/html/sql-lab-config.json && chmod 664 /var/www/html/sql-lab-config.json && systemctl restart apache2 && echo Deployment complete"'
echo ""
echo "Or copy this shorter version (assumes you'll enter password 3 times):"
echo ""
echo "Step 1 - Copy database:"
echo "scp wallys_database_setup.sql root@155.138.197.128:/root/"
echo ""
echo "Step 2 - Copy PHP files:" 
echo "scp wallys_*.php root@155.138.197.128:/var/www/html/"
echo ""
echo "Step 3 - Setup everything:"
echo 'ssh root@155.138.197.128 "mysql < /root/wallys_database_setup.sql && chown www-data:www-data /var/www/html/wallys_*.php && chmod 644 /var/www/html/wallys_*.php && systemctl restart apache2"'