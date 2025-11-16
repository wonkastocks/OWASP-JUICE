#!/bin/bash

# Direct SSH fix for admin password
SERVER="155.138.197.128"
echo "This script will fix the admin password on $SERVER"
echo ""
echo "You'll need to enter your SSH password when prompted."
echo ""

# Create the SQL fix file
cat > /tmp/fix_admin.sql << 'EOF'
USE lottery_system;

-- Ensure admin_users table exists
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clear and insert admin with SHA256 hash
DELETE FROM admin_users WHERE email = 'admin@wonkatech.org';
INSERT INTO admin_users (username, email, password)
VALUES ('admin', 'admin@wonkatech.org', SHA2('R00tbeer', 256));

-- Also update users table if it exists
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELETE FROM users WHERE email = 'admin@wonkatech.org';
INSERT INTO users (email, password, role)
VALUES ('admin@wonkatech.org', SHA2('R00tbeer', 256), 'admin');

-- Show results
SELECT 'Admin password has been reset' as status;
SELECT email, LEFT(password, 20) as pwd_preview FROM admin_users WHERE email = 'admin@wonkatech.org';
EOF

echo "Step 1: Copying SQL file to server..."
scp /tmp/fix_admin.sql root@$SERVER:/tmp/

echo ""
echo "Step 2: Executing SQL to fix password..."
ssh root@$SERVER "mysql -u root lottery_system < /tmp/fix_admin.sql && rm /tmp/fix_admin.sql"

echo ""
echo "Step 3: Checking PHP login method..."
ssh root@$SERVER "grep -B2 -A5 'SHA2\|sha256\|md5\|password' /var/www/html/admin/admin_login.php 2>/dev/null | head -20"

echo ""
echo "Done! You should now be able to login with:"
echo "Email: admin@wonkatech.org"
echo "Password: R00tbeer"
echo ""
echo "Login at: https://wonkatech.org/admin/admin_login.php"