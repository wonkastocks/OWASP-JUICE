#!/bin/bash

# Deploy Admin Panel to WonkaTech CTF Server
echo "🚀 Deploying Admin Panel to WonkaTech CTF Server..."

# Server details
SERVER="root@155.138.197.128"
REMOTE_PATH="/var/www/html/admin"

# Create remote directory
echo "📁 Creating admin directory on server..."
ssh $SERVER "mkdir -p $REMOTE_PATH"

# Copy all admin files
echo "📤 Copying admin files..."
scp -r /Users/walterbarr_1/sql-injection-lab/admin/* $SERVER:$REMOTE_PATH/

# Set proper permissions
echo "🔐 Setting permissions..."
ssh $SERVER << 'EOF'
    chown -R www-data:www-data /var/www/html/admin
    chmod -R 755 /var/www/html/admin
    chmod 640 /var/www/html/admin/config.php
    
    # Ensure session directory exists
    mkdir -p /var/lib/php/sessions
    chown www-data:www-data /var/lib/php/sessions
    chmod 700 /var/lib/php/sessions
    
    # Restart Apache
    systemctl restart apache2
    
    echo "✅ Admin panel deployed successfully!"
EOF

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📌 Admin Panel Access:"
echo "   URL: http://155.138.197.128/admin/admin_login.php"
echo "   Email: admin@wonkatech.com"
echo "   Password: WonkaAdmin2024!"
echo ""
echo "🔒 Security Note: Consider changing the admin password in config.php"