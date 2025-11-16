#!/bin/bash

echo "================================================"
echo "Upgrading OWASP Juice Shop to v18.0.0 on Vultr2"
echo "================================================"

# Install Node.js 22 first
echo "Installing Node.js 22..."
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt-get install -y nodejs

# Verify Node version
node -v

# Stop current service
systemctl stop juice-shop

# Restore from backup since last attempt failed
if [ -d /opt/juice-shop-v15-backup ]; then
    echo "Restoring from backup..."
    rm -rf /opt/juice-shop
    mv /opt/juice-shop-v15-backup /opt/juice-shop-v15-backup-old
fi

# Download v18.0.0 for Node 22
echo "Downloading Juice Shop v18.0.0 for Node 22..."
cd /opt
wget https://github.com/juice-shop/juice-shop/releases/download/v18.0.0/juice-shop-18.0.0_node22_linux_x64.tgz

# Extract
echo "Extracting v18.0.0..."
tar -xzf juice-shop-18.0.0_node22_linux_x64.tgz
rm juice-shop-18.0.0_node22_linux_x64.tgz

# Rename to standard directory
mv juice-shop_18.0.0 juice-shop 2>/dev/null || true

# Set permissions
chown -R www-data:www-data /opt/juice-shop

# Update systemd service
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
curl -s http://localhost:3000 | grep -o "OWASP Juice Shop.*" | head -1
systemctl status juice-shop --no-pager | head -10

echo "================================================"
echo "Upgrade to v18.0.0 Complete!"
echo "Access at: http://66.42.93.220:3000"
echo "================================================"
