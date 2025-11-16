#!/bin/bash

# Check how the login actually works

echo "Checking admin login PHP file..."
echo ""
echo "Run this command to see how password is checked:"
echo "ssh root@155.138.197.128 'grep -A 10 -B 5 password /var/www/html/admin/admin_login.php'"
echo ""
echo "Also check for password hashing method:"
echo "ssh root@155.138.197.128 'grep -r \"SHA2\\|sha256\\|md5\\|password_hash\\|password_verify\" /var/www/html/admin/*.php | head -20'"