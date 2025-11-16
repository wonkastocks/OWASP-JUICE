#!/bin/bash

echo "Deploying clean login page without hints..."

# First, find which file has the hints and replace it
scp /Users/walterbarr_1/sql-injection-lab/clean_wallys_login.html root@155.138.197.128:/tmp/clean_login.html && \
ssh root@155.138.197.128 << 'ENDSSH'
# Find the file with the hints
echo "Looking for login files..."
if grep -q "SQL Injection Demo Lab" /var/www/html/index.html 2>/dev/null; then
    echo "Found hints in index.html"
    cp /tmp/clean_login.html /var/www/html/index.html
    chown www-data:www-data /var/www/html/index.html
elif grep -q "SQL Injection Demo Lab" /var/www/html/login.html 2>/dev/null; then
    echo "Found hints in login.html"
    cp /tmp/clean_login.html /var/www/html/login.html
    chown www-data:www-data /var/www/html/login.html
elif grep -q "SQL Injection Demo Lab" /var/www/html/index.php 2>/dev/null; then
    echo "Found hints in index.php - replacing HTML section"
    # For PHP files, we need to be more careful
    cp /var/www/html/index.php /var/www/html/index.php.backup
    # Remove the hint section from PHP file
    sed -i '/<div.*background.*#fff3cd/,/<\/div>/d' /var/www/html/index.php
    sed -i '/SQL Injection Demo Lab/,/Database Dump:/d' /var/www/html/index.php
else
    echo "Checking default index..."
    # Just replace the default index
    cp /tmp/clean_login.html /var/www/html/index.html
    chown www-data:www-data /var/www/html/index.html
fi

# Also check for any JavaScript that might be adding the hints
find /var/www/html -name "*.js" -exec grep -l "SQL Injection Demo Lab" {} \; -exec rm {} \;

systemctl restart apache2
echo "Clean login page deployed!"
ENDSSH

echo ""
echo "Deployment complete!"
echo "The yellow hint box has been removed."
echo "Students can use the separate walkthrough document: SQL_INJECTION_WALKTHROUGH.md"