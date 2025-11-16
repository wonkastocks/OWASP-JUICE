#!/bin/bash

# Swap admin_login.php with test_login.php and remove test_login.php

echo "=== Backing up current admin_login.php ==="
cp /var/www/html/admin/admin_login.php /var/www/html/admin/admin_login.php.backup_$(date +%s)

echo "=== Replacing admin_login.php with test_login.php ==="
cp /var/www/html/admin/test_login.php /var/www/html/admin/admin_login.php

echo "=== Removing test_login.php ==="
rm /var/www/html/admin/test_login.php

echo "=== Setting correct permissions ==="
chown www-data:www-data /var/www/html/admin/admin_login.php
chmod 755 /var/www/html/admin/admin_login.php

echo "=== Verifying the swap ==="
ls -la /var/www/html/admin/admin_login.php
ls -la /var/www/html/admin/test_login.php 2>/dev/null || echo "test_login.php successfully removed"

echo "=== Admin login page swap completed! ==="