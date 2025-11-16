#!/bin/bash

# Script to remove SQL injection hints from wonkatech.org login page
SERVER="155.138.197.128"

echo "Removing SQL injection hints from wonkatech.org login page..."

# SSH into the server and remove the hint box
ssh root@$SERVER << 'ENDSSH'
echo "Finding login.php file..."

# Look for the login.php file
if [ -f /var/www/html/login.php ]; then
    echo "Found login.php, creating backup..."
    cp /var/www/html/login.php /var/www/html/login.php.backup_hints
    
    echo "Removing hint section..."
    
    # Remove the entire yellow hint box section
    # This removes everything between the SQL Injection Demo Lab div and its closing tag
    sed -i '/<div.*style.*background.*#fff3cd\|background.*#ffe4b5\|background.*#ffeaa7/,/<\/div>/d' /var/www/html/login.php
    sed -i '/<div.*class.*hint\|warning-box\|demo-box/,/<\/div>/d' /var/www/html/login.php
    sed -i '/SQL Injection Demo Lab/,/Database Dump:/d' /var/www/html/login.php
    sed -i '/Valid Test Account:/,/users WHERE user_type/d' /var/www/html/login.php
    
    # Remove any inline JavaScript that might be adding hints
    sed -i '/admin@wallys\.com/d' /var/www/html/login.php
    sed -i '/123456/d' /var/www/html/login.php
    sed -i '/UNION SELECT/d' /var/www/html/login.php
    
    echo "Hints removed from login.php"
fi

# Also check if there's an index.php that redirects to login
if [ -f /var/www/html/index.php ]; then
    echo "Checking index.php..."
    sed -i '/<div.*style.*background.*#fff3cd\|background.*#ffe4b5\|background.*#ffeaa7/,/<\/div>/d' /var/www/html/index.php
    sed -i '/SQL Injection Demo Lab/,/Database Dump:/d' /var/www/html/index.php
fi

# Restart Apache
systemctl restart apache2
echo "Apache restarted"
ENDSSH

echo "Hints removed successfully!"