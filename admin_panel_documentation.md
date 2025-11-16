# WonkaTech CTF Admin Panel Documentation

## 🎯 Overview
A comprehensive admin panel has been created for managing the WonkaTech CTF platform with OWASP Juice Shop instances.

## 📌 Access Information

**Admin Panel URL:** http://155.138.197.128/admin/admin_login.php

**Admin Credentials:**
- Email: `admin@wonkatech.com`
- Password: `WonkaAdmin2024!`

## 🚀 Features

### 1. Dashboard (`/admin/index.php`)
- **Statistics Overview**
  - Total registered users
  - Verified users count
  - Active users (last 7 days)
  - Total challenges completed
- **Container Status**
  - View all 5 Docker containers (ports 3001-3005)
  - See current assignments
  - Quick management links
- **Popular Challenges**
  - Most completed challenges
  - Average completion time
  - Points distribution

### 2. User Management (`/admin/users.php`)
- **View All Users**
  - Username, email, registration date
  - Verification status
  - Assigned container/instance
  - Score and challenge progress
- **User Actions**
  - Delete users (with confirmation)
  - Reset scoreboards
  - View detailed progress
- **Search & Filter**
  - Search by username or email
  - Sort by various columns
- **Export**
  - Download user list as CSV

### 3. Progress Tracking (`/admin/progress.php`)
- **Individual User Progress**
  - Select any user from dropdown
  - View completed challenges by category
  - See completion times and points
  - Track hints used
- **User Statistics**
  - Total score
  - Challenge count
  - Container assignment

### 4. Container Management (`/admin/containers.php`)
- **Container Overview**
  - All 5 Juice Shop instances
  - Current status (available/assigned/maintenance)
  - User assignments
- **Container Actions**
  - Restart containers
  - Release/unassign containers
  - Assign containers to users
  - View instance directly (opens Juice Shop)

## 🔒 Security Features

1. **Authentication**
   - Separate admin login system
   - Session management with timeout (1 hour)
   - Activity logging

2. **CSRF Protection**
   - All forms include CSRF tokens
   - Token validation on every action

3. **Audit Logging**
   - All admin actions logged to database
   - Includes IP address and user agent
   - Timestamp for every action

4. **Access Control**
   - Admin-only access
   - Automatic logout on inactivity
   - Secure password hashing

## 📂 File Structure

```
/var/www/ctf-platform/admin/
├── admin_login.php    # Admin authentication
├── index.php          # Dashboard
├── users.php          # User management
├── progress.php       # Progress tracking
├── containers.php     # Container management
├── config.php         # Configuration & database
├── functions.php      # Shared functions
├── style.css          # Admin panel styling
└── logout.php         # Logout handler
```

## 🛠️ Technical Details

### Database Tables Used
- `users` - User accounts and authentication
- `challenge_progress` - Individual challenge completions
- `scores` - Aggregated user scores
- `containers` - Docker container assignments
- `audit_log` - Admin activity tracking
- `sessions` - User session management

### Key Functions
- `deleteUser()` - Remove user and cascade delete related data
- `resetUserScoreboard()` - Clear user's challenge progress
- `assignContainer()` - Assign Docker container to user
- `getUserProgress()` - Get detailed challenge completion data
- `exportUsersToCSV()` - Export user list to CSV file
- `logAdminActivity()` - Track all admin actions

## 🔧 Administration Tasks

### Common Operations

1. **Remove a User**
   - Go to Users page
   - Find the user
   - Click delete button (🗑️)
   - Confirm deletion

2. **Reset User Progress**
   - Go to Users page
   - Find the user
   - Click reset button (🔄)
   - Confirm reset

3. **Assign Container**
   - Go to Containers page
   - Select user from dropdown
   - Select available container
   - Click "Assign Container"

4. **View User Progress**
   - Go to Progress page
   - Select user from dropdown
   - View completed challenges by category

5. **Export User Data**
   - Go to Users page
   - Click "Export CSV" button
   - File downloads automatically

## 🚨 Important Notes

1. **Password Security**
   - Change the default admin password in `config.php`
   - Use a strong, unique password

2. **Container Management**
   - Containers restart automatically when reassigned
   - Each user can only have one container
   - Unassigned containers remain available

3. **Data Integrity**
   - User deletion cascades to all related data
   - Scoreboard reset only affects challenge progress
   - Container release makes it available for others

## 📊 Monitoring

The admin panel provides real-time monitoring of:
- User registration trends
- Challenge completion rates
- Container utilization
- System activity

## 🔄 Maintenance

Regular maintenance tasks:
1. Monitor container health
2. Review audit logs
3. Export user data for backup
4. Check for inactive users
5. Restart containers if needed

## 📝 Deployment

To redeploy or update the admin panel:
```bash
/Users/walterbarr_1/sql-injection-lab/deploy_admin_panel_fixed.exp
```

## 🆘 Troubleshooting

**Can't access admin panel:**
- Verify Apache is running: `systemctl status apache2`
- Check DocumentRoot: `/var/www/ctf-platform`
- Ensure admin directory exists with correct permissions

**Login not working:**
- Check credentials in `config.php`
- Verify session directory exists: `/var/lib/php/sessions`
- Check PHP error logs

**Container operations failing:**
- Ensure Docker is running
- Check container names match pattern: `juice-user[1-5]`
- Verify port assignments (3001-3005)

---

*Admin panel successfully deployed and operational!*