#!/bin/bash

# Full deployment script for Wally's Monkey Parts
# You'll need to enter your password when prompted

SERVER="155.138.197.128"
LOCAL_DIR="/Users/walterbarr_1/sql-injection-lab"

echo "=========================================="
echo "Deploying Wally's Monkey Parts SQL Lab"
echo "=========================================="
echo ""
echo "You'll be prompted for the root password multiple times."
echo "Password should be in your MCP server config."
echo ""

# Step 1: Copy database file
echo "[1/5] Copying database setup file..."
scp $LOCAL_DIR/wallys_database_setup.sql root@$SERVER:/root/

# Step 2: Copy PHP files
echo "[2/5] Copying PHP files to web directory..."
scp $LOCAL_DIR/wallys_login.php $LOCAL_DIR/wallys_dashboard.php $LOCAL_DIR/wallys_logout.php root@$SERVER:/var/www/html/

# Step 3: Setup database and permissions
echo "[3/5] Setting up database and permissions..."
ssh root@$SERVER << 'ENDSSH'
echo "Creating database..."
mysql -e "DROP DATABASE IF EXISTS wallys_monkey_parts;"
mysql < /root/wallys_database_setup.sql

echo "Setting file permissions..."
chown www-data:www-data /var/www/html/wallys_*.php
chmod 644 /var/www/html/wallys_*.php

echo "Creating config file..."
cat > /var/www/html/sql-lab-config.json << 'EOF'
{
    "lab_enabled": true,
    "last_modified": "2024-01-01 12:00:00",
    "modified_by": "system"
}
EOF

chown www-data:www-data /var/www/html/sql-lab-config.json
chmod 664 /var/www/html/sql-lab-config.json

echo "Restarting Apache..."
systemctl restart apache2

echo "Verifying files..."
ls -la /var/www/html/wallys_*.php
ENDSSH

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Access the lab at:"
echo "http://$SERVER/wallys_login.php"
echo ""
echo "Test SQL Injection:"
echo "Username: admin' --"
echo "Password: anything"
echo ""
echo "Or use valid credentials:"
echo "Username: admin"
echo "Password: MonkeyBusiness123!"
echo ""