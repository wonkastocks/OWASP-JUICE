# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational CTF (Capture The Flag) platform combining two systems:
1. **WonkaTech CTF Platform** - PHP/Apache registration and user management system
2. **OWASP Juice Shop Instances** - Dockerized Node.js vulnerable web applications

**Production Server**: Vultr VPS at 155.138.197.128 (Ubuntu 22.04.5 LTS)
**Domain**: wonkatech.org (via Cloudflare Tunnel)

## Architecture

### Two-Tier System
- **PHP Platform** (`/var/www/html/`): User registration, authentication, instance assignment, admin dashboard
- **Juice Shop Containers**: 5 Docker instances on ports 3001-3005, each assigned to one user

### Key Directories
- `/var/www/html/` - Main CTF platform (PHP/Apache)
- `/var/www/html/admin/` - Admin panel for monitoring users and containers
- Local `.exp` scripts - Expect scripts for automated remote deployment via SSH/SCP

## Deployment Pattern

**Standard deployment workflow** (matches user preference):
```bash
# Step 1: Copy files to server
scp /path/to/file.php root@155.138.197.128:/var/www/html/

# Step 2: SSH in and apply changes
ssh root@155.138.197.128 "chown www-data:www-data /var/www/html/file.php && chmod 644 /var/www/html/file.php && systemctl restart apache2"
```

**For database changes**:
```bash
scp script.sql root@155.138.197.128:/tmp/ && ssh root@155.138.197.128 "mysql -u root -pWonkaChocolate2024! ctf_platform < /tmp/script.sql"
```

### Expect Script Pattern
Most `.exp` scripts automate the above pattern with password handling:
- Password: `$R00tbeer02` (needs escaping in expect: `\$R00tbeer02`)
- Use expect scripts for automated deployments requiring password entry

## Server Commands

### Docker Container Management
```bash
# Check all Juice Shop containers
docker ps | grep juice

# Restart specific instance
docker restart juice-user1  # (or juice-user2, juice-user3, etc.)

# View logs
docker logs juice-user1

# Restart all instances
for i in {1..5}; do docker restart juice-user$i; done
```

### Database Operations
```bash
# Connect to database
mysql -u root -pWonkaChocolate2024! ctf_platform

# Common queries
mysql -u root -pWonkaChocolate2024! ctf_platform -e "SELECT username, email, instance_url FROM users;"
mysql -u root -pWonkaChocolate2024! ctf_platform -e "SELECT * FROM containers WHERE status='assigned';"
```

### Apache/Web Server
```bash
# Restart Apache
systemctl restart apache2

# Check Apache status
systemctl status apache2

# View error logs
tail -f /var/log/apache2/error.log
```

### Cloudflare Tunnel
```bash
# Check tunnel status
systemctl status cloudflared

# View tunnel logs
journalctl -u cloudflared -f
```

## Development Workflow

### Making Changes to PHP Platform

1. **Edit locally** in this directory
2. **Test syntax** (if possible): `php -l file.php`
3. **Deploy using SCP pattern**:
   ```bash
   scp file.php root@155.138.197.128:/var/www/html/
   ssh root@155.138.197.128 "chown www-data:www-data /var/www/html/file.php && systemctl restart apache2"
   ```
4. **Verify** using firecrawl MCP: `mcp__firecrawl__firecrawl_scrape` on https://wonkatech.org

### Creating Backups

Before making changes, create timestamped backup:
```bash
ssh root@155.138.197.128 "tar -czf /root/backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz /var/www/html/ /etc/apache2/sites-available/"
```

## Challenge Solvers

### Python Automation Scripts
Located in root directory, named by pattern:
- `master_solver.py` - Comprehensive solver for all 110 Juice Shop challenges
- `[challenge]_solver.py` - Specific challenge solvers (e.g., `bonus_payload_solver.py`)
- `juice5_sqli_exploit.py` - SQL injection demonstrations

**Common dependencies**:
```bash
pip3 install requests playwright selenium
```

**Running solvers**:
```bash
python3 master_solver.py  # Solve all challenges
python3 juice5_sqli_exploit.py  # Specific exploit demo
```

## Database Schema

### Primary Tables (ctf_platform database)
- `users` - Registered users with instance assignments
- `containers` - Docker container tracking and status
- `sessions` - User session management
- `challenge_progress` - User challenge completion tracking
- `scores` - Aggregate scoring and leaderboard
- `audit_log` - Admin activity logging

### Instance Assignment Flow
1. User registers → Entry in `users` table
2. System calls stored procedure `assign_container(user_id)`
3. Updates `containers` table status to 'assigned'
4. Sets `users.instance_url` to `http://155.138.197.128:300X`

## Admin Panel

**Access**: https://wonkatech.org/admin/
**Credentials**: admin@wonkatech.org / R00tbeer

**Key Files**:
- `admin/admin_login.php` - Login page (working)
- `admin/dashboard.php` - Main dashboard with statistics (working)
- `admin/index.php` - Redirects to dashboard after auth
- `admin/users.php` - User management (has redirect loop issue)
- `admin/containers.php` - Container monitoring
- `admin/config.php` - Database connection and auth functions

**Current Status**: Admin login and dashboard are functional. Some pages may have issues with redirect loops.

## Security Notes

This is an **educational security lab** with intentionally vulnerable components:
- Basic SQL injection demos in legacy `wallys_login.php` files
- OWASP Juice Shop instances contain 110+ vulnerabilities by design
- Platform itself uses secure coding (prepared statements, password hashing, CSRF tokens)

**Do not**:
- Create new vulnerabilities in the registration/admin platform
- Deploy these demos to public internet without isolation
- Share credentials from this project

**Do**:
- Use prepared statements for all database queries in platform code
- Follow existing security patterns in `/var/www/html/` PHP files
- Test changes on local dev before deploying to production server

## Testing & Verification

### After Deployment
1. **Check web access**: Use firecrawl MCP to scrape https://wonkatech.org
2. **Verify containers**: `ssh root@155.138.197.128 "docker ps"`
3. **Test database**: SSH in and run test queries
4. **Check Apache logs**: `ssh root@155.138.197.128 "tail -20 /var/log/apache2/error.log"`

### Restart All Services
```bash
ssh root@155.138.197.128 "systemctl restart apache2 && systemctl restart mysql && for i in {1..5}; do docker restart juice-user$i; done"
```

## File Naming Conventions

- `*_solver.py` - Python scripts that exploit Juice Shop vulnerabilities
- `deploy_*.exp` - Expect scripts for remote deployment automation
- `fix_*.exp` - Expect scripts for fixing specific issues remotely
- `check_*.exp` - Expect scripts for verifying system state
- `*_documentation.md` - Technical documentation and guides
- `STUDENT_LAB_GUIDE.md` - Educational materials for lab participants