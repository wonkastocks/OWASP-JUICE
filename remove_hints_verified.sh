#!/bin/bash

SERVER="155.138.197.128"

echo "================================================"
echo "Removing SQL Injection Hints from wonkatech.org"
echo "================================================"
echo ""
echo "You'll need to enter your root password when prompted."
echo ""

# Step 1: Backup and remove hints
echo "[1/3] Backing up and cleaning login.php..."
ssh root@$SERVER << 'ENDSSH'
# Create backup
cp /var/www/html/login.php /var/www/html/login.php.backup_hints_$(date +%Y%m%d)

# Method 1: Remove the entire demo-info div
sed -i '/<div class="demo-info">/,/<\/div>/d' /var/www/html/login.php

# Method 2: If nested divs exist, use a more aggressive approach
perl -i -0pe 's/<div class="demo-info">.*?<\/div>//gs' /var/www/html/login.php

# Method 3: Remove any remaining hint text patterns
sed -i '/SQL Injection Demo Lab/d' /var/www/html/login.php
sed -i '/Valid Test Account:/d' /var/www/html/login.php
sed -i '/admin@wallys.com/d' /var/www/html/login.php
sed -i '/Password: 123456/d' /var/www/html/login.php
sed -i '/SQL Injection Tests:/d' /var/www/html/login.php
sed -i '/Database Dump:/d' /var/www/html/login.php
sed -i '/UNION SELECT.*FROM users/d' /var/www/html/login.php

echo "Hints removed from login.php"
ENDSSH

# Step 2: Clear any cache
echo "[2/3] Clearing cache..."
ssh root@$SERVER << 'ENDSSH'
# Clear PHP opcache if exists
if [ -f /usr/bin/cachetool ]; then
    cachetool opcache:reset
fi

# Clear any Cloudflare or other CDN cache would go here
# Clear browser cache is on client side

# Restart services
systemctl restart apache2
systemctl restart php7.4-fpm 2>/dev/null || systemctl restart php8.0-fpm 2>/dev/null || systemctl restart php8.1-fpm 2>/dev/null || true

echo "Cache cleared and services restarted"
ENDSSH

# Step 3: Verify the change
echo "[3/3] Verifying removal..."
echo ""
echo "Checking if hints are still present..."
ssh root@$SERVER "grep -c 'demo-info' /var/www/html/login.php || echo 'demo-info section not found (good!)'"
ssh root@$SERVER "grep -c 'admin@wallys' /var/www/html/login.php || echo 'Test account not found (good!)'"

echo ""
echo "================================================"
echo "DONE! Please check https://wonkatech.org/login.php"
echo "================================================"
echo ""
echo "If you still see hints, it might be cached:"
echo "1. Clear your browser cache (Ctrl+F5)"
echo "2. Try incognito/private mode"
echo "3. Check from a different browser"
echo ""