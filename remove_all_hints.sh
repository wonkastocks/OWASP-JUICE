#!/bin/bash

# Complete removal of all SQL injection hints
echo "Removing ALL SQL injection hints from server..."

# One-line command to find and remove hints
ssh root@155.138.197.128 "find /var/www/html -type f \( -name '*.php' -o -name '*.html' -o -name '*.js' \) -exec grep -l 'SQL Injection Demo Lab\|admin@wallys.com\|123456\|Valid Test Account' {} \; -exec sed -i.bak -e '/SQL Injection Demo Lab/,/Database Dump:/d' -e '/Valid Test Account:/,/Database Dump:/d' -e '/admin@wallys.com/d' -e '/123456/d' {} \; && systemctl restart apache2"

echo "Hints removed!"