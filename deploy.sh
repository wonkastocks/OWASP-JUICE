#!/bin/bash

echo "Deploying clean login page to server..."
echo "You will be prompted for the password: $R00tbeer02"
echo ""

echo "Step 1: Copying file to server..."
scp /Users/walterbarr_1/sql-injection-lab/clean_login.php root@155.138.197.128:/root/clean_login.php

if [ $? -eq 0 ]; then
    echo "File copied successfully!"
    echo ""
    echo "Step 2: Deploying on server..."
    ssh root@155.138.197.128 << 'EOF'
        echo "Creating backup of current login.php..."
        cp /var/www/html/login.php /var/www/html/login.php.backup.$(date +%Y%m%d_%H%M%S)
        
        echo "Moving new file to web directory..."
        mv /root/clean_login.php /var/www/html/login.php
        
        echo "Setting proper ownership and permissions..."
        chown www-data:www-data /var/www/html/login.php
        chmod 644 /var/www/html/login.php
        
        echo "Restarting Apache..."
        systemctl restart apache2
        
        echo "Checking Apache status..."
        systemctl status apache2 --no-pager | head -5
        
        echo "Deployment complete!"
EOF
else
    echo "Failed to copy file to server. Please check credentials and connectivity."
    exit 1
fi