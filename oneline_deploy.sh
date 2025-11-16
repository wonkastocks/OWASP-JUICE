#!/bin/bash

# One-line deployment commands for Wally's Monkey Parts

echo "Copy and run these one-liners:"
echo ""
echo "# 1. Copy all files and setup database (single command):"
echo 'scp /Users/walterbarr_1/sql-injection-lab/wallys_*.php root@155.138.197.128:/var/www/html/ && scp /Users/walterbarr_1/sql-injection-lab/wallys_database_setup.sql root@155.138.197.128:/root/ && ssh root@155.138.197.128 "mysql < /root/wallys_database_setup.sql && chown www-data:www-data /var/www/html/wallys_*.php && chmod 644 /var/www/html/wallys_*.php && systemctl restart apache2"'
echo ""
echo "# Or if you prefer step by step:"
echo ""
echo "# Step 1: Copy files"
echo 'scp /Users/walterbarr_1/sql-injection-lab/wallys_*.{php,sql} root@155.138.197.128:/tmp/'
echo ""
echo "# Step 2: Setup everything"  
echo 'ssh root@155.138.197.128 "mv /tmp/wallys_*.php /var/www/html/ && mysql < /tmp/wallys_database_setup.sql && chown www-data:www-data /var/www/html/wallys_*.php && chmod 644 /var/www/html/wallys_*.php && systemctl restart apache2"'
echo ""
echo "Access at: http://155.138.197.128/wallys_login.php"