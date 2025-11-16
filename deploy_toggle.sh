#!/bin/bash

# Deploy SQL Injection Lab Toggle System
# This script copies the updated files to the server

SERVER_IP="155.138.197.128"
SERVER_USER="root"
WEB_DIR="/var/www/html"

echo "================================================"
echo "Deploying SQL Injection Lab Toggle System"
echo "================================================"
echo ""

# Create a temporary directory for staging
echo "Step 1: Preparing files for deployment..."
TEMP_DIR="/tmp/sql-lab-deploy-$(date +%s)"
mkdir -p $TEMP_DIR

# Copy files to temp directory
cp /Users/walterbarr_1/sql-injection-lab/web/index.php $TEMP_DIR/
cp /Users/walterbarr_1/sql-injection-lab/web/login.php $TEMP_DIR/
cp /Users/walterbarr_1/sql-injection-lab/web/dashboard.php $TEMP_DIR/
cp /Users/walterbarr_1/sql-injection-lab/web/admin_control.php $TEMP_DIR/
cp /Users/walterbarr_1/sql-injection-lab/web/logout.php $TEMP_DIR/

echo "Step 2: Creating backup on server..."
ssh $SERVER_USER@$SERVER_IP "mkdir -p /root/sql-lab-backup-$(date +%Y%m%d-%H%M%S) && cp -r $WEB_DIR/*.php /root/sql-lab-backup-$(date +%Y%m%d-%H%M%S)/ 2>/dev/null || true"

echo "Step 3: Copying files to server..."
scp $TEMP_DIR/*.php $SERVER_USER@$SERVER_IP:$WEB_DIR/

echo "Step 4: Setting permissions on server..."
ssh $SERVER_USER@$SERVER_IP "chown www-data:www-data $WEB_DIR/*.php && chmod 644 $WEB_DIR/*.php"

echo "Step 5: Creating default configuration file..."
ssh $SERVER_USER@$SERVER_IP "cat > $WEB_DIR/sql-lab-config.json << 'EOF'
{
    \"lab_enabled\": false,
    \"last_modified\": \"$(date '+%Y-%m-%d %H:%M:%S')\",
    \"modified_by\": \"system\"
}
EOF"

echo "Step 6: Setting permissions for config file..."
ssh $SERVER_USER@$SERVER_IP "chown www-data:www-data $WEB_DIR/sql-lab-config.json && chmod 664 $WEB_DIR/sql-lab-config.json"

echo "Step 7: Restarting Apache..."
ssh $SERVER_USER@$SERVER_IP "systemctl restart apache2"

echo "Step 8: Cleaning up temporary files..."
rm -rf $TEMP_DIR

echo ""
echo "================================================"
echo "✅ Deployment Complete!"
echo "================================================"
echo ""
echo "Access the lab at: http://$SERVER_IP/"
echo "Admin Control Panel: http://$SERVER_IP/admin_control.php"
echo ""
echo "The SQL injection lab is currently DISABLED by default."
echo "Admin users can toggle it on/off from the control panel."
echo ""