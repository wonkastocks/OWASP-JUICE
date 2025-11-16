#!/bin/bash

# Deploy fix for the original vulnerable login system
echo "Fixing SQL Injection Lab on server..."

# One-line deployment as you prefer
scp /Users/walterbarr_1/sql-injection-lab/fix_mysqli_login.php root@155.138.197.128:/var/www/html/login.php && ssh root@155.138.197.128 "chown www-data:www-data /var/www/html/login.php && chmod 644 /var/www/html/login.php && systemctl restart apache2"

echo "Fix deployed!"
echo "Test at: http://155.138.197.128/login.php"
echo ""
echo "Try SQL injection:"
echo "Username: admin' --"
echo "Password: anything"