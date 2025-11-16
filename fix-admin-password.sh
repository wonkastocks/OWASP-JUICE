#!/bin/bash

# Comprehensive admin password fix for WonkaTech

echo "Creating comprehensive admin password fix..."

cat > /tmp/fix_admin_password.sql << 'EOF'
USE lottery_system;

-- First, check if admin_users table exists
SHOW TABLES LIKE 'admin_users';

-- If it doesn't exist, create it
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Delete any existing admin accounts to avoid duplicates
DELETE FROM admin_users WHERE email = 'admin@wonkatech.org';

-- Insert new admin with multiple password hash formats
-- Try SHA2 256 first (most common)
INSERT INTO admin_users (username, email, password)
VALUES ('admin', 'admin@wonkatech.org', SHA2('R00tbeer', 256));

-- Show the result
SELECT id, username, email, LEFT(password, 20) as password_preview FROM admin_users WHERE email = 'admin@wonkatech.org';

-- Also check if there's a users table with admin role
SHOW TABLES LIKE 'users';

-- If users table exists, also update there
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Update or insert in users table as well
DELETE FROM users WHERE email = 'admin@wonkatech.org';
INSERT INTO users (email, password, role)
VALUES ('admin@wonkatech.org', SHA2('R00tbeer', 256), 'admin');

-- Also try MD5 format in case the PHP uses that
UPDATE admin_users SET password = MD5('R00tbeer') WHERE email = 'admin@wonkatech.org' AND LENGTH(password) < 64;

-- Show both tables
SELECT 'admin_users table:' as table_name;
SELECT * FROM admin_users WHERE email = 'admin@wonkatech.org';
SELECT 'users table:' as table_name;
SELECT * FROM users WHERE email = 'admin@wonkatech.org' LIMIT 1;
EOF

echo "SQL file created at /tmp/fix_admin_password.sql"
echo ""
echo "Step 1: Copy the SQL file to server:"
echo "scp /tmp/fix_admin_password.sql root@155.138.197.128:/tmp/"
echo ""
echo "Step 2: Execute the SQL commands:"
echo "ssh root@155.138.197.128 'mysql -u root < /tmp/fix_admin_password.sql'"
echo ""
echo "Step 3: Check the PHP code to see what hash method is used:"
echo "ssh root@155.138.197.128 'grep -A 5 \"password\" /var/www/html/admin/admin_login.php | head -20'"
echo ""
echo "The password will be set to: R00tbeer"
echo "Login with: admin@wonkatech.org"