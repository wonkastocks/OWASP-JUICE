#!/bin/bash

# Complete fix for SQL injection lab - one-line deployment
echo "Deploying complete fix to server..."

# Copy and execute everything in one line
scp /Users/walterbarr_1/sql-injection-lab/fix_mysqli_login.php root@155.138.197.128:/var/www/html/login.php && \
scp /Users/walterbarr_1/sql-injection-lab/ensure_database.sql root@155.138.197.128:/root/ && \
ssh root@155.138.197.128 "mysql < /root/ensure_database.sql && chown www-data:www-data /var/www/html/login.php && chmod 644 /var/www/html/login.php && systemctl restart apache2 && echo 'Fix complete!'"

echo ""
echo "==================================="
echo "SQL Injection Lab Fixed!"
echo "==================================="
echo ""
echo "Test URL: http://155.138.197.128/login.php"
echo ""
echo "Valid login:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "SQL Injection test:"
echo "  Username: admin' --"
echo "  Password: anything"
echo ""
echo "Or try:"
echo "  Username: ' OR '1'='1' --"
echo "  Password: anything"