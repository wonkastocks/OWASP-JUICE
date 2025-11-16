#!/bin/bash

# Quick OWASP Juice Shop Installation using pre-built release
echo "================================================"
echo "Quick Juice Shop Installation (Pre-built)"
echo "Server: Vultr2 (66.42.93.220)"
echo "================================================"

# Stop any existing installation
pkill -f "npm install" 2>/dev/null

# Install Apache and Node.js if not already installed
echo "1. Installing Apache and Node.js..."
apt-get update
apt-get install -y apache2 nodejs npm wget unzip

# Download pre-built Juice Shop
echo "2. Downloading pre-built Juice Shop..."
cd /opt
rm -rf juice-shop-old 2>/dev/null
mv juice-shop juice-shop-old 2>/dev/null
wget https://github.com/juice-shop/juice-shop/releases/download/v15.0.0/juice-shop-15.0.0_node18_linux_x64.zip

echo "3. Extracting Juice Shop..."
unzip -q juice-shop-15.0.0_node18_linux_x64.zip
rm juice-shop-15.0.0_node18_linux_x64.zip

# Set permissions
echo "4. Setting permissions..."
chown -R www-data:www-data /opt/juice-shop
chmod +x /opt/juice-shop/npm

# Create systemd service
echo "5. Creating systemd service..."
cat > /etc/systemd/system/juice-shop.service << 'EOF'
[Unit]
Description=OWASP Juice Shop
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/juice-shop
ExecStart=/usr/bin/node /opt/juice-shop/build/app.js
Restart=on-failure
RestartSec=10
Environment=NODE_ENV=ctf
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
EOF

# Configure Apache
echo "6. Configuring Apache..."
a2enmod proxy proxy_http proxy_wstunnel rewrite headers

cat > /etc/apache2/sites-available/juice-shop.conf << 'EOF'
<VirtualHost *:80>
    ServerName 66.42.93.220
    
    ErrorLog ${APACHE_LOG_DIR}/juice-error.log
    CustomLog ${APACHE_LOG_DIR}/juice-access.log combined
    
    ProxyRequests Off
    ProxyPreserveHost On
    
    # WebSocket support
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} =websocket [NC]
    RewriteRule /(.*)  ws://localhost:3000/$1 [P,L]
    RewriteCond %{HTTP:Upgrade} !=websocket [NC]
    RewriteRule /(.*)  http://localhost:3000/$1 [P,L]
    
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/
</VirtualHost>
EOF

# Enable site
a2dissite 000-default 2>/dev/null
a2ensite juice-shop

# Start services
echo "7. Starting services..."
systemctl daemon-reload
systemctl enable juice-shop
systemctl restart juice-shop
systemctl restart apache2

# Wait for startup
sleep 5

# Test
echo "8. Testing installation..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ Juice Shop is running on port 3000"
else
    echo "❌ Juice Shop failed to start"
    journalctl -u juice-shop --no-pager -n 20
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
    echo "✅ Apache proxy is working"
else
    echo "❌ Apache proxy failed"
fi

echo ""
echo "================================================"
echo "Installation Complete!"
echo "Access at: http://66.42.93.220"
echo "================================================"