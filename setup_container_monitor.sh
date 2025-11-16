#!/bin/bash

# Setup container monitoring cron job

echo "Setting up container activity monitoring..."

# Create the cron script
cat > /tmp/container_monitor_cron.sh << 'EOF'
#!/bin/bash
# Container monitor cron script
/usr/bin/php /var/www/ctf-platform/admin/container_monitor.php >> /var/log/container_monitor.log 2>&1
EOF

chmod +x /tmp/container_monitor_cron.sh

# Add to crontab (runs every minute)
echo "Adding cron job to run every minute..."
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/php /var/www/ctf-platform/admin/container_monitor.php >> /var/log/container_monitor.log 2>&1") | crontab -

echo "Container monitoring setup complete!"
echo "Containers will be checked every minute and shut down after 10 minutes of inactivity."
echo "Log file: /var/log/container_monitor.log"