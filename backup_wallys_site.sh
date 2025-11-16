#!/bin/bash

# Backup script for Wally's Monkey Parts website
# Creates timestamped backups of website files and database

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/root/backups/wallys_monkey_parts_${TIMESTAMP}"
REMOTE_HOST="root@155.138.197.128"

echo "================================================"
echo "Wally's Monkey Parts - Full Site Backup"
echo "Timestamp: ${TIMESTAMP}"
echo "================================================"

# Create local backup directory
mkdir -p /tmp/wallys_backup_${TIMESTAMP}

# Step 1: Create backup directory on server
echo ""
echo "Step 1: Creating backup directory on server..."
ssh ${REMOTE_HOST} "mkdir -p ${BACKUP_DIR}"

# Step 2: Backup website files
echo ""
echo "Step 2: Backing up website files..."
ssh ${REMOTE_HOST} "cd /var/www/html && tar -czf ${BACKUP_DIR}/website_files.tar.gz ."
echo "✓ Website files backed up to ${BACKUP_DIR}/website_files.tar.gz"

# Step 3: Backup database
echo ""
echo "Step 3: Backing up MySQL database..."
ssh ${REMOTE_HOST} "mysqldump -u root wallysdb > ${BACKUP_DIR}/wallysdb_backup.sql"
ssh ${REMOTE_HOST} "gzip ${BACKUP_DIR}/wallysdb_backup.sql"
echo "✓ Database backed up to ${BACKUP_DIR}/wallysdb_backup.sql.gz"

# Step 4: Create restore script
echo ""
echo "Step 4: Creating restore script..."
ssh ${REMOTE_HOST} "cat > ${BACKUP_DIR}/restore.sh" << 'EOF'
#!/bin/bash

echo "================================================"
echo "Wally's Monkey Parts - Restore Script"
echo "================================================"

# Restore website files
echo "Restoring website files..."
rm -rf /var/www/html/*
tar -xzf website_files.tar.gz -C /var/www/html/
chown -R www-data:www-data /var/www/html/
chmod -R 755 /var/www/html/

# Restore database
echo "Restoring database..."
mysql -u root -e "DROP DATABASE IF EXISTS wallysdb;"
mysql -u root -e "CREATE DATABASE wallysdb;"
gunzip -c wallysdb_backup.sql.gz | mysql -u root wallysdb

# Restart services
systemctl restart apache2
systemctl restart mysql

echo "✓ Restoration complete!"
EOF

ssh ${REMOTE_HOST} "chmod +x ${BACKUP_DIR}/restore.sh"
echo "✓ Restore script created at ${BACKUP_DIR}/restore.sh"

# Step 5: Create backup manifest
echo ""
echo "Step 5: Creating backup manifest..."
ssh ${REMOTE_HOST} "cat > ${BACKUP_DIR}/MANIFEST.txt" << EOF
Wally's Monkey Parts - Backup Manifest
=======================================
Backup Date: $(date)
Timestamp: ${TIMESTAMP}

Contents:
- website_files.tar.gz : Complete /var/www/html directory
- wallysdb_backup.sql.gz : MySQL database dump
- restore.sh : Automated restore script
- MANIFEST.txt : This file

To restore:
1. cd ${BACKUP_DIR}
2. sudo ./restore.sh
EOF

echo "✓ Manifest created"

# Step 6: Download backup to local machine (optional)
echo ""
read -p "Download backup to local machine? (y/n): " download_choice
if [[ "$download_choice" == "y" ]]; then
    echo "Downloading backup..."
    scp -r ${REMOTE_HOST}:${BACKUP_DIR} /tmp/wallys_backup_${TIMESTAMP}/
    echo "✓ Backup downloaded to /tmp/wallys_backup_${TIMESTAMP}/"
fi

echo ""
echo "================================================"
echo "✓ BACKUP COMPLETE!"
echo "================================================"
echo "Server backup location: ${BACKUP_DIR}"
echo "Restore command: ssh ${REMOTE_HOST} 'cd ${BACKUP_DIR} && ./restore.sh'"
echo "================================================"