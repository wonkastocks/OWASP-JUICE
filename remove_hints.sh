#!/bin/bash

# Script to remove the yellow hint box from the login page
echo "Removing password hints from login page..."

# SSH command to remove the hint section from the login page
ssh root@155.138.197.128 << 'ENDSSH'
# Find and remove the hint box from any PHP/HTML files
echo "Searching for files with SQL injection hints..."

# Check common locations
for file in /var/www/html/index.php /var/www/html/login.php /var/www/html/index.html /var/www/html/login.html; do
    if [ -f "$file" ]; then
        echo "Checking $file..."
        
        # Backup the file first
        cp "$file" "${file}.backup"
        
        # Remove the yellow hint box section (multiple patterns to catch different formats)
        # Remove anything between SQL Injection Demo Lab and the closing div
        sed -i '/<div.*SQL Injection Demo Lab/,/<\/div>/d' "$file"
        sed -i '/SQL Injection Demo Lab/,/Database Dump:/d' "$file"
        sed -i '/Valid Test Account:/,/Database Dump:/d' "$file"
        sed -i '/admin@wallys.com.*123456/d' "$file"
        sed -i '/SQL Injection Tests:/,/anything/d' "$file"
        
        # Also remove any yellow warning boxes with hints
        sed -i '/<div style.*background.*#fff3cd/,/<\/div>/d' "$file"
        sed -i '/<div class="hint"/,/<\/div>/d' "$file"
        
        echo "Cleaned $file"
    fi
done

# Restart Apache to ensure changes take effect
systemctl restart apache2
echo "Apache restarted"
ENDSSH

echo ""
echo "Hints removed from login page!"
echo "Walkthrough saved in: SQL_INJECTION_WALKTHROUGH.md"