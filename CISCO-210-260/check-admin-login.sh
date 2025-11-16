#!/bin/bash

# Check admin login setup

cat > /tmp/check_admin.sql << 'EOF'
USE lottery_system;

-- Check if admin_users table exists and its structure
SHOW TABLES LIKE 'admin_users';
DESCRIBE admin_users;

-- Check current admin users
SELECT * FROM admin_users;

-- Check if there's a users table instead
SHOW TABLES LIKE 'users';

-- Show all tables
SHOW TABLES;
EOF

echo "SQL commands created. Run:"
echo "scp /tmp/check_admin.sql root@155.138.197.128:/tmp/ && ssh root@155.138.197.128 'mysql -u root < /tmp/check_admin.sql'"