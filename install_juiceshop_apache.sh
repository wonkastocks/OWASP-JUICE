#!/bin/bash

# OWASP Juice Shop Installation Script for Ubuntu with Apache
# No Docker, No SSH server - Direct installation

echo "================================================"
echo "OWASP Juice Shop Installation on Apache"
echo "Server: Vultr2 (66.42.93.220)"
echo "================================================"

# Update system
echo "1. Updating system packages..."
apt-get update && apt-get upgrade -y

# Install required packages
echo "2. Installing Apache, Node.js, and dependencies..."
apt-get install -y apache2 curl git build-essential sqlite3

# Install Node.js 18.x (required for Juice Shop)
echo "3. Installing Node.js 18.x..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Verify installations
echo "4. Verifying installations..."
node --version
npm --version
apache2 -v

# Clone Juice Shop repository
echo "5. Cloning OWASP Juice Shop..."
cd /opt
git clone https://github.com/juice-shop/juice-shop.git
cd juice-shop

# Checkout stable version
echo "6. Checking out stable version..."
git checkout v15.0.0

# Install dependencies and build
echo "7. Installing Juice Shop dependencies..."
npm install --production --unsafe-perm

# Create systemd service
echo "8. Creating systemd service..."
cat > /etc/systemd/system/juice-shop.service << 'EOF'
[Unit]
Description=OWASP Juice Shop
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/juice-shop
ExecStart=/usr/bin/node app.js
Restart=on-failure
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
EOF

# Set proper permissions
echo "9. Setting permissions..."
chown -R www-data:www-data /opt/juice-shop

# Enable required Apache modules
echo "10. Configuring Apache modules..."
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
a2enmod rewrite
a2enmod headers

# Create Apache virtual host configuration
echo "11. Creating Apache configuration..."
cat > /etc/apache2/sites-available/juice-shop.conf << 'EOF'
<VirtualHost *:80>
    ServerName 66.42.93.220
    ServerAlias juiceshop.local
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/juice-shop-error.log
    CustomLog ${APACHE_LOG_DIR}/juice-shop-access.log combined
    
    # Proxy settings
    ProxyRequests Off
    ProxyPreserveHost On
    
    # WebSocket support
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} =websocket [NC]
    RewriteRule /(.*)           ws://localhost:3000/$1 [P,L]
    RewriteCond %{HTTP:Upgrade} !=websocket [NC]
    RewriteRule /(.*)           http://localhost:3000/$1 [P,L]
    
    # Proxy to Node.js application
    ProxyPass / http://localhost:3000/
    ProxyPassReverse / http://localhost:3000/
    
    # Headers for proper proxying
    <Location />
        Header set X-Forwarded-Proto "http"
        Header set X-Forwarded-Port "80"
    </Location>
</VirtualHost>
EOF

# Disable default site and enable Juice Shop
echo "12. Enabling Juice Shop site..."
a2dissite 000-default
a2ensite juice-shop

# Create data directory
echo "13. Creating data directory..."
mkdir -p /opt/juice-shop/data
chown www-data:www-data /opt/juice-shop/data

# Start and enable services
echo "14. Starting services..."
systemctl daemon-reload
systemctl enable juice-shop
systemctl start juice-shop
systemctl restart apache2

# Wait for Juice Shop to start
echo "15. Waiting for Juice Shop to start..."
sleep 10

# Check service status
echo "16. Checking service status..."
systemctl status juice-shop --no-pager
systemctl status apache2 --no-pager

# Test if Juice Shop is accessible
echo "17. Testing Juice Shop..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo "✅ Juice Shop is running on port 3000"
else
    echo "❌ Juice Shop is not responding on port 3000"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
    echo "✅ Apache proxy is working on port 80"
else
    echo "❌ Apache proxy is not working"
fi

# Configure firewall
echo "18. Configuring firewall..."
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo "Juice Shop is accessible at:"
echo "  http://66.42.93.220"
echo ""
echo "Service Management:"
echo "  systemctl status juice-shop"
echo "  systemctl restart juice-shop"
echo "  systemctl stop juice-shop"
echo ""
echo "Logs:"
echo "  journalctl -u juice-shop -f"
echo "  tail -f /var/log/apache2/juice-shop-*.log"
echo "================================================"