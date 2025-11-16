# Deploy Clean Login Page - Manual Instructions

## Files Created
- `/Users/walterbarr_1/sql-injection-lab/clean_login.php` - The clean login page with only header banner and login form

## Manual Deployment Steps

### Step 1: Copy the file to server
```bash
scp /Users/walterbarr_1/sql-injection-lab/clean_login.php root@155.138.197.128:/root/clean_login.php
```
Password: `$R00tbeer02`

### Step 2: SSH into server
```bash
ssh root@155.138.197.128
```
Password: `$R00tbeer02`

### Step 3: Deploy the clean login page
Once logged in, run these commands:
```bash
# Backup current login page
cp /var/www/html/login.php /var/www/html/login.php.backup.$(date +%Y%m%d_%H%M%S)

# Replace with clean version
cp /root/clean_login.php /var/www/html/login.php

# Set proper permissions
chown www-data:www-data /var/www/html/login.php
chmod 644 /var/www/html/login.php

# Restart Apache
systemctl restart apache2

# Verify
echo "Clean login page deployed!"
exit
```

## What the Clean Login Page Contains
- ✅ Header banner with shipping promotion
- ✅ Clean "Login" title (no emoji, no "Demo")
- ✅ Username and Password fields
- ✅ Sign In button
- ✅ Modern purple gradient styling
- ✅ SQL injection vulnerability preserved for demo

## What Was Removed
- ❌ All navigation menus
- ❌ Product categories bar
- ❌ Shop sections
- ❌ Footer with copyright text
- ❌ "For entertainment purposes" disclaimer
- ❌ Contact information
- ❌ Quick links
- ❌ All extra content except header and login form

## Verification
After deployment, visit https://wonkatech.org/login.php to verify the changes.