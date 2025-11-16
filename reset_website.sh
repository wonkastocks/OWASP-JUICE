#!/bin/bash

# Reset script for Wally's Monkey Parts website
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

cat << 'EOF' > /tmp/reset_commands.sh
#!/bin/bash

echo "================================================"
echo "Resetting Wally's Monkey Parts Website"
echo "================================================"

# Stop services
echo "Stopping services..."
systemctl stop apache2
systemctl stop mysql

# Clear website directory
echo "Clearing website files..."
rm -rf /var/www/html/*
rm -rf /var/www/html/.htaccess 2>/dev/null

# Create placeholder page
cat > /var/www/html/index.html << 'INDEX_EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Site Reset</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        p {
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Website Reset Complete</h1>
        <p>The site has been cleared and is ready for your new project.</p>
        <p>All databases have been preserved for reference.</p>
    </div>
</body>
</html>
INDEX_EOF

# Set permissions
chown -R www-data:www-data /var/www/html/
chmod -R 755 /var/www/html/

# Start MySQL service
systemctl start mysql

# List all databases for reference
echo ""
echo "Existing databases (preserved):"
mysql -u root -e "SHOW DATABASES;"

# Create new empty database for fresh start
echo ""
echo "Creating fresh database: new_project_db"
mysql -u root -e "DROP DATABASE IF EXISTS new_project_db;"
mysql -u root -e "CREATE DATABASE new_project_db;"
mysql -u root -e "GRANT ALL PRIVILEGES ON new_project_db.* TO 'root'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"

# Start Apache service
systemctl start apache2

echo ""
echo "================================================"
echo "✓ RESET COMPLETE!"
echo "================================================"
echo ""
echo "Summary:"
echo "- Website files cleared"
echo "- Placeholder page created at http://155.138.197.128/"
echo "- All existing databases preserved"
echo "- New empty database 'new_project_db' created"
echo "- Apache and MySQL services running"
echo ""
echo "Backup location: /root/backups/wallys_monkey_parts_20250831_124630"
echo "================================================"
EOF

echo "Reset script created at /tmp/reset_commands.sh"