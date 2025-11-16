#!/bin/bash

# Direct removal of hints from wonkatech.org login.php
SERVER="155.138.197.128"

echo "Removing SQL injection hints from wonkatech.org..."

# SSH and directly edit the file
ssh root@$SERVER << 'ENDSSH'
echo "Backing up login.php..."
cp /var/www/html/login.php /var/www/html/login.php.backup_$(date +%Y%m%d_%H%M%S)

echo "Removing the demo-info div section..."

# Create a Python script to remove the hints
cat > /tmp/remove_hints.py << 'PYTHON'
import re

# Read the login.php file
with open('/var/www/html/login.php', 'r') as f:
    content = f.read()

# Remove the entire demo-info div and its contents
# This pattern matches the div with class="demo-info" and everything inside it
content = re.sub(r'<div\s+class=["\']demo-info["\']>.*?</div>\s*', '', content, flags=re.DOTALL)

# Also remove any inline styles or sections containing the hint text
content = re.sub(r'<div[^>]*>.*?SQL Injection Demo Lab.*?</div>', '', content, flags=re.DOTALL)
content = re.sub(r'<h3>.*?SQL Injection Demo Lab.*?</h3>', '', content, flags=re.DOTALL)
content = re.sub(r'admin@wallys\.com.*?123456', '', content, flags=re.DOTALL)
content = re.sub(r'Password:.*?123456.*?<', '<', content)
content = re.sub(r'Email:.*?admin@wallys\.com.*?<', '<', content)
content = re.sub(r'UNION SELECT.*?user_type.*?admin.*?--', '', content, flags=re.DOTALL)

# Write back the cleaned content
with open('/var/www/html/login.php', 'w') as f:
    f.write(content)

print("Hints removed successfully")
PYTHON

# Run the Python script
python3 /tmp/remove_hints.py

# Alternative: Use sed to remove the demo-info section
sed -i '/<div class="demo-info">/,/<\/div>/d' /var/www/html/login.php

# Double-check by removing any remaining hint text
sed -i '/SQL Injection Demo Lab/d' /var/www/html/login.php
sed -i '/Valid Test Account:/d' /var/www/html/login.php
sed -i '/admin@wallys.com/d' /var/www/html/login.php
sed -i '/Password: 123456/d' /var/www/html/login.php
sed -i '/SQL Injection Tests:/d' /var/www/html/login.php
sed -i '/Database Dump:/d' /var/www/html/login.php
sed -i '/UNION SELECT/d' /var/www/html/login.php

# Restart services
systemctl restart apache2
systemctl restart php7.4-fpm 2>/dev/null || systemctl restart php8.0-fpm 2>/dev/null || true

echo "Cleanup complete!"
ENDSSH

echo "Hints have been removed from wonkatech.org/login.php"