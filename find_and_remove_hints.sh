#!/bin/bash

# Find and remove the SQL injection hints from the server
echo "Finding and removing SQL injection hints..."

# SSH into server and search for the hint content
ssh root@155.138.197.128 << 'ENDSSH'
echo "Searching for files containing the hint text..."

# Search for files containing the specific text
grep -r "SQL Injection Demo Lab" /var/www/html/ 2>/dev/null
grep -r "admin@wallys.com" /var/www/html/ 2>/dev/null
grep -r "123456" /var/www/html/ 2>/dev/null

# Find all PHP and HTML files and check them
find /var/www/html -type f \( -name "*.php" -o -name "*.html" \) -exec grep -l "SQL Injection Demo Lab\|admin@wallys.com\|123456" {} \;

echo ""
echo "Files found with hints. Please provide the exact file path showing the hints."
ENDSSH