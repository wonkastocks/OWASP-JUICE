#!/bin/bash

echo "================================================"
echo "Installing REAL OWASP Juice Shop on Vultr2"
echo "================================================"

# Kill existing processes
pkill -f node
systemctl stop juice-shop 2>/dev/null

# Clean up
rm -rf /opt/juice-shop /opt/juiceshop-app /opt/juice

# Download the actual pre-built Juice Shop
echo "Downloading Juice Shop v15.0.0..."
cd /opt
wget https://github.com/juice-shop/juice-shop/releases/download/v15.0.0/juice-shop-15.0.0_node18_linux_x64.tgz

# Extract
echo "Extracting..."
tar -xzf juice-shop-15.0.0_node18_linux_x64.tgz
rm juice-shop-15.0.0_node18_linux_x64.tgz

# The extraction creates a juice-shop_15.0.0 directory
mv juice-shop_15.0.0 juice-shop 2>/dev/null || mv juice-shop-* juice-shop

# Set permissions
chown -R www-data:www-data /opt/juice-shop
chmod +x /opt/juice-shop/npm 2>/dev/null

# Create systemd service
cat > /etc/systemd/system/juice-shop.service << 'EOF'
[Unit]
Description=OWASP Juice Shop
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/juice-shop
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/usr/bin/node /opt/juice-shop/build/app.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Apache
a2enmod proxy proxy_http rewrite headers

cat > /etc/apache2/sites-available/juice-shop.conf << 'EOF'
<VirtualHost *:80>
    ServerName 66.42.93.220
    
    ProxyRequests Off
    ProxyPreserveHost On
    
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/
</VirtualHost>
EOF

a2ensite juice-shop
a2dissite 000-default
systemctl restart apache2

# Start Juice Shop
systemctl daemon-reload
systemctl enable juice-shop
systemctl restart juice-shop

sleep 5

# Test
echo "Testing..."
curl -s http://localhost:3000 | grep -q "OWASP" && echo "✅ Juice Shop is running!" || echo "❌ Not working yet"

echo "================================================"
echo "Access at: http://66.42.93.220"
echo "================================================"