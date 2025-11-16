#!/bin/bash

# Direct deployment script for Wally's Monkey Parts SQL Injection Lab
SERVER="155.138.197.128"
echo "Deploying Wally's Monkey Parts to $SERVER"

# First, let's copy all files using a single scp command
echo "Copying files to server..."
scp /Users/walterbarr_1/sql-injection-lab/wallys_*.php root@$SERVER:/var/www/html/
scp /Users/walterbarr_1/sql-injection-lab/wallys_database_setup.sql root@$SERVER:/root/

# Now SSH and run setup commands
echo "Setting up database and permissions..."
ssh root@$SERVER << 'ENDSSH'
# Import database
mysql < /root/wallys_database_setup.sql

# Set permissions
chown www-data:www-data /var/www/html/wallys_*.php
chmod 644 /var/www/html/wallys_*.php

# Create/update config file
cat > /var/www/html/sql-lab-config.json << 'EOF'
{
    "lab_enabled": true,
    "last_modified": "2024-01-01 12:00:00",
    "modified_by": "system"
}
EOF

chown www-data:www-data /var/www/html/sql-lab-config.json
chmod 664 /var/www/html/sql-lab-config.json

# Restart Apache
systemctl restart apache2

echo "Deployment complete!"
ENDSSH

echo "Access the lab at: http://$SERVER/wallys_login.php"