#!/bin/bash

echo "================================================"
echo "Upgrading OWASP Juice Shop to v18 on Vultr2"
echo "================================================"

# Stop current service
systemctl stop juice-shop

# Backup current installation
echo "Creating backup of v15..."
mv /opt/juice-shop /opt/juice-shop-v15-backup

# Download latest v18 release
echo "Downloading Juice Shop v18.0.1..."
cd /opt
wget https://github.com/juice-shop/juice-shop/releases/download/v18.0.1/juice-shop-18.0.1_node20_linux_x64.tgz

# Extract
echo "Extracting v18..."
tar -xzf juice-shop-18.0.1_node20_linux_x64.tgz
rm juice-shop-18.0.1_node20_linux_x64.tgz

# Rename to standard directory
mv juice-shop_18.0.1 juice-shop

# Set permissions
chown -R www-data:www-data /opt/juice-shop

# Update systemd service for Node 20
cat > /etc/systemd/system/juice-shop.service << 'SERVICEEOF'
[Unit]
Description=OWASP Juice Shop v18
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/juice-shop
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/usr/bin/node /opt/juice-shop/build/app.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Reload and restart
systemctl daemon-reload
systemctl restart juice-shop

sleep 5

# Test
echo "Testing v18 installation..."
curl -s http://localhost:3000 | grep -o "OWASP Juice Shop.*v[0-9]*" | head -1

echo "================================================"
echo "Upgrade Complete!"
echo "Access at: http://66.42.93.220:3000"
echo "================================================"
