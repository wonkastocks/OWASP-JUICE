#!/bin/bash

# Create backup on server with timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/root/backups/wallys_monkey_parts_${TIMESTAMP}"

cat << 'EOF' > /tmp/backup_commands.sh
#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/root/backups/wallys_monkey_parts_${TIMESTAMP}"

echo "================================================"
echo "Creating backup at: ${BACKUP_DIR}"
echo "================================================"

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Backup website files
echo "Backing up website files..."
cd /var/www/html && tar -czf ${BACKUP_DIR}/website_files.tar.gz .
echo "✓ Website files backed up"

# Backup database
echo "Backing up database..."
mysqldump -u root wallysdb > ${BACKUP_DIR}/wallysdb_backup.sql
gzip ${BACKUP_DIR}/wallysdb_backup.sql
echo "✓ Database backed up"

# Create restore script
cat > ${BACKUP_DIR}/restore.sh << 'RESTORE_EOF'
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
RESTORE_EOF

chmod +x ${BACKUP_DIR}/restore.sh

# Create manifest
cat > ${BACKUP_DIR}/MANIFEST.txt << MANIFEST_EOF
Wally's Monkey Parts - Backup Manifest
=======================================
Backup Date: $(date)
Backup Location: ${BACKUP_DIR}

Contents:
- website_files.tar.gz : Complete /var/www/html directory
- wallysdb_backup.sql.gz : MySQL database dump
- restore.sh : Automated restore script
- MANIFEST.txt : This file

To restore:
1. cd ${BACKUP_DIR}
2. sudo ./restore.sh
MANIFEST_EOF

echo ""
echo "================================================"
echo "✓ BACKUP COMPLETE!"
echo "================================================"
echo "Backup location: ${BACKUP_DIR}"
echo "================================================"

# List backup contents
ls -la ${BACKUP_DIR}/
EOF

echo "Backup script created at /tmp/backup_commands.sh"