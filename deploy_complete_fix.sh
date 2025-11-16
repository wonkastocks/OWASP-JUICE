#!/bin/bash

# Deploy the fixed files to remove hints and fix SQL errors
echo "Deploying fixes to server..."

# One-line deployment command
scp /Users/walterbarr_1/sql-injection-lab/fixed_index.php root@155.138.197.128:/var/www/html/index.php && \
scp /Users/walterbarr_1/sql-injection-lab/fixed_login.php root@155.138.197.128:/var/www/html/login.php && \
ssh root@155.138.197.128 "chown www-data:www-data /var/www/html/index.php /var/www/html/login.php && chmod 644 /var/www/html/index.php /var/www/html/login.php && systemctl restart apache2 && echo 'Deployment complete!'"

echo ""
echo "==================================="
echo "Fixes Deployed!"
echo "==================================="
echo ""
echo "Changes made:"
echo "✓ Removed password hints from login page"
echo "✓ Fixed SQL syntax handling for injection"
echo ""
echo "Test at: http://155.138.197.128/login.php"
echo ""
echo "SQL Injection tests:"
echo "  admin' --"
echo "  ' OR '1'='1' --"
echo "  ' OR 1=1 --"