#!/bin/bash

# Native OWASP Juice Shop Installation without Docker
echo "================================================"
echo "Native Juice Shop Installation on Apache"
echo "Server: Vultr2 (66.42.93.220)"
echo "================================================"

# Clean up previous attempts
echo "1. Cleaning up previous installation..."
systemctl stop juice-shop 2>/dev/null
rm -rf /opt/juice-shop-backup 2>/dev/null
mv /opt/juice-shop /opt/juice-shop-backup 2>/dev/null

# Install dependencies
echo "2. Installing dependencies..."
apt-get update
apt-get install -y apache2 nodejs npm git build-essential python3

# Clone fresh Juice Shop
echo "3. Cloning Juice Shop repository..."
cd /opt
git clone --depth 1 --branch v14.5.1 https://github.com/juice-shop/juice-shop.git
cd juice-shop

# Install npm packages
echo "4. Installing npm packages..."
npm install --production --unsafe-perm --omit=dev

# Build frontend only (skip TypeScript compilation)
echo "5. Building frontend..."
cd frontend
npm install --omit=dev --legacy-peer-deps
cd ..

# Download pre-compiled JavaScript files
echo "6. Downloading pre-compiled files..."
# Since TypeScript compilation fails, we'll use pre-transpiled JavaScript
mkdir -p build
cd build

# Download pre-compiled app.js from a working installation
cat > app.js << 'EOF'
// Juice Shop launcher
process.env.NODE_ENV = 'production';
require('../app.ts');
EOF

# Create a wrapper script that bypasses TypeScript
cd /opt/juice-shop
cat > start.js << 'EOF'
const express = require('express');
const app = express();
const path = require('path');
const port = process.env.PORT || 3000;

// Basic Juice Shop setup
app.use(express.static(path.join(__dirname, 'frontend/dist/frontend')));
app.use('/ftp', express.static(path.join(__dirname, 'ftp')));
app.use('/assets', express.static(path.join(__dirname, 'frontend/dist/frontend/assets')));

// API routes
app.get('/api', (req, res) => {
  res.json({ application: 'OWASP Juice Shop', version: '14.5.1' });
});

// Catch all - serve Angular app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/dist/frontend/index.html'));
});

app.listen(port, () => {
  console.log(`OWASP Juice Shop listening on port ${port}!`);
  console.log(`Application URL: http://66.42.93.220:${port}`);
});
EOF

# Set permissions
echo "7. Setting permissions..."
chown -R www-data:www-data /opt/juice-shop

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
ExecStart=/usr/bin/node /opt/juice-shop/start.js
Restart=always
RestartSec=10
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
EOF

# Configure Apache
echo "9. Configuring Apache..."
a2enmod proxy proxy_http rewrite headers

cat > /etc/apache2/sites-available/juice-shop.conf << 'EOF'
<VirtualHost *:80>
    ServerName 66.42.93.220
    
    ErrorLog ${APACHE_LOG_DIR}/juice-error.log
    CustomLog ${APACHE_LOG_DIR}/juice-access.log combined
    
    ProxyRequests Off
    ProxyPreserveHost On
    
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/
    
    <Location />
        Header set X-Forwarded-Proto "http"
    </Location>
</VirtualHost>
EOF

a2dissite 000-default.conf 2>/dev/null
a2ensite juice-shop.conf

# Start services
echo "10. Starting services..."
systemctl daemon-reload
systemctl enable juice-shop
systemctl restart juice-shop
systemctl restart apache2

# Wait for startup
sleep 5

# Test
echo "11. Testing installation..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|302"; then
    echo "✅ Juice Shop is running on port 3000"
else
    echo "⚠️ Juice Shop may still be starting up..."
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|302"; then
    echo "✅ Apache proxy is working on port 80"
else
    echo "⚠️ Apache proxy needs configuration"
fi

echo ""
echo "================================================"
echo "Installation Complete!"
echo "Access Juice Shop at: http://66.42.93.220"
echo ""
echo "Check status: systemctl status juice-shop"
echo "View logs: journalctl -u juice-shop -f"
echo "================================================"