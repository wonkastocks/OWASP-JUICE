#!/bin/bash

# Script to reset admin password for wonkatech.org

echo "Resetting admin password for admin@wonkatech.org..."

# Set new password (you can change this)
NEW_PASSWORD="R00tbeer"
HASHED_PASSWORD=$(echo -n "$NEW_PASSWORD" | openssl dgst -sha256 | awk '{print $2}')

# Create SQL command
cat > /tmp/reset_admin_pass.sql << EOF
USE lottery_system;
UPDATE admin_users
SET password = SHA2('$NEW_PASSWORD', 256)
WHERE email = 'admin@wonkatech.org';
SELECT username, email FROM admin_users WHERE email = 'admin@wonkatech.org';
EOF

echo "New password will be: $NEW_PASSWORD"
echo "SQL file created at /tmp/reset_admin_pass.sql"
echo ""
echo "To apply, run:"
echo "scp /tmp/reset_admin_pass.sql root@155.138.197.128:/tmp/ && ssh root@155.138.197.128 'mysql -u root < /tmp/reset_admin_pass.sql && rm /tmp/reset_admin_pass.sql'"