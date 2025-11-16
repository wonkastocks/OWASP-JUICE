#!/bin/bash

echo "Direct SSH fix for wonkatech.org login hints"
echo ""
echo "Since your password starts with $, you need to:"
echo "1. Enter it with single quotes when prompted"
echo "2. Or escape the $ with backslash"
echo ""
echo "Run this command and enter your password when prompted:"
echo ""
echo "ssh root@155.138.197.128"
echo ""
echo "Then once logged in, copy and paste these commands:"
echo ""
cat << 'COMMANDS'
# Remove the demo-info section
sed -i '/<div class="demo-info">/,/<\/div>/d' /var/www/html/login.php

# If that doesn't work, try this more aggressive approach
perl -i -0pe 's/<div class="demo-info">.*?<\/div>//gs' /var/www/html/login.php

# Remove any remaining hint text
sed -i '/SQL Injection Demo Lab/d' /var/www/html/login.php
sed -i '/Valid Test Account:/d' /var/www/html/login.php
sed -i '/admin@wallys.com/d' /var/www/html/login.php
sed -i '/Password: 123456/d' /var/www/html/login.php
sed -i '/SQL Injection Tests:/d' /var/www/html/login.php
sed -i '/Database Dump:/d' /var/www/html/login.php
sed -i '/UNION SELECT.*FROM users/d' /var/www/html/login.php

# Restart Apache
systemctl restart apache2

# Verify the changes
echo "Checking for demo-info section..."
grep -c 'demo-info' /var/www/html/login.php || echo "demo-info removed successfully!"

exit
COMMANDS