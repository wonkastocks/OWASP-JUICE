#!/bin/bash

# Final fix - completely remove the demo-info section
SERVER="155.138.197.128"

echo "Final fix for wonkatech.org login page..."

# One-line command to remove the entire demo-info section
ssh root@$SERVER "cp /var/www/html/login.php /var/www/html/login.php.backup && sed -i '/<div class=\"demo-info\">/,/<\/div>/c\' /var/www/html/login.php && systemctl restart apache2"

echo "Demo info section removed!"