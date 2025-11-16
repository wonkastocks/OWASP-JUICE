#!/bin/bash

# Create backup first
echo "Creating backup..."
mkdir -p /root/backups/$(date +%Y%m%d_%H%M%S)
cp -r /var/www/html/admin /root/backups/$(date +%Y%m%d_%H%M%S)/ 2>/dev/null
cp -r /var/www/html/*.php /root/backups/$(date +%Y%m%d_%H%M%S)/ 2>/dev/null

echo "=== Fixing Apache Port Conflict ==="
# Check what's using port 443
lsof -i :443 | grep LISTEN

# Kill any process using port 443 that's not cloudflared
lsof -i :443 | grep -v cloudflared | awk '{print $2}' | xargs kill -9 2>/dev/null

# Update Apache to use port 80 only (let Cloudflare handle SSL)
sed -i 's/Listen 443/# Listen 443/g' /etc/apache2/ports.conf
sed -i 's/<VirtualHost \*:443>/<VirtualHost *:80>/g' /etc/apache2/sites-available/*.conf

# Start Apache
systemctl start apache2 || service apache2 start || /etc/init.d/apache2 start
systemctl status apache2 --no-pager | head -5

echo "=== Fixing MySQL/MariaDB ==="
# Start MySQL if not running
systemctl start mysql || service mysql start || /etc/init.d/mysql start

# Check if database exists
mysql -u root -e "CREATE DATABASE IF NOT EXISTS ctf_platform;" 2>/dev/null

# Create tables if needed
mysql -u root ctf_platform << 'EOF' 2>/dev/null
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    instance_url VARCHAR(255),
    verified INT DEFAULT 0,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expiry DATETIME,
    last_activity DATETIME
);

CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin if not exists
INSERT IGNORE INTO admin_users (username, password) 
VALUES ('admin', '$2y$10$YourHashedPasswordHere');
EOF

echo "=== Updating Cloudflare Configuration ==="
# Update cloudflare config to point to port 80
cat > /etc/cloudflared/config.yml << 'EOF'
tunnel: ctf-platform
credentials-file: /root/.cloudflared/ctf-platform.json

ingress:
  - hostname: wonkatech.com
    service: http://localhost:80
  - hostname: www.wonkatech.com
    service: http://localhost:80
  - hostname: juice1.wonkatech.com
    service: http://localhost:3001
  - hostname: juice2.wonkatech.com
    service: http://localhost:3002
  - hostname: juice3.wonkatech.com
    service: http://localhost:3003
  - hostname: juice4.wonkatech.com
    service: http://localhost:3004
  - hostname: juice5.wonkatech.com
    service: http://localhost:3005
  - service: http_status:404
EOF

# Restart cloudflared
systemctl restart cloudflared

echo "=== Checking Services ==="
echo "Apache:"
systemctl status apache2 --no-pager | head -3
echo ""
echo "MySQL:"
systemctl status mysql --no-pager | head -3
echo ""
echo "Cloudflared:"
systemctl status cloudflared --no-pager | head -3
echo ""
echo "Docker containers:"
docker ps | grep juice | wc -l
echo ""
echo "Platform accessible at: https://wonkatech.com"
echo "Admin panel at: https://wonkatech.com/admin/"
echo "Juice instances at: https://juice[1-5].wonkatech.com"