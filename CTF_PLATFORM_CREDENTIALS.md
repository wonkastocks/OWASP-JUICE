# WonkaTech CTF Platform Credentials

## 🔐 Admin Account
**URL**: https://wonkatech.org/login.php  
**Email**: admin@wonkatech.org  
**Password**: WonkaAdmin2024!

## 🌐 Platform Access Points

### Main CTF Platform
- **URL**: https://wonkatech.org
- **Purpose**: User registration and instance management
- **Features**:
  - User registration/login
  - Automatic Juice Shop instance assignment
  - Challenge tracking per user

### Admin Panel
- **URL**: https://wonkatech.org/admin/
- **Access**: Requires admin credentials above
- **Features**:
  - View all registered users
  - Monitor active Juice Shop instances
  - Track challenge completion statistics
  - Manage Docker containers
  - View user activity and last login times

### Individual Juice Shop Instances
- **Instance 1**: https://juice1.wonkatech.org (Port 3001)
- **Instance 2**: https://juice2.wonkatech.org (Port 3002)
- **Instance 3**: https://juice3.wonkatech.org (Port 3003)
- **Instance 4**: https://juice4.wonkatech.org (Port 3004)
- **Instance 5**: https://juice5.wonkatech.org (Port 3005)

### Standalone Instance (Direct IP Access)
- **URL**: http://155.138.197.128:5000
- **Purpose**: Direct challenge solving without Cloudflare
- **Features**: All 110 challenges enabled (NODE_ENV=unsafe)

## 🖥️ Server Access

### SSH Access
- **Host**: 155.138.197.128
- **Username**: root
- **Password**: $R00tbeer02
- **Port**: 22

### MySQL Database
- **Database**: ctf_platform
- **Username**: root
- **Password**: Wonka2024!
- **Tables**:
  - users (registered users)
  - password_resets (reset tokens)

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  instance_url VARCHAR(255),
  container_id VARCHAR(64),
  is_verified BOOLEAN DEFAULT FALSE,
  verification_token VARCHAR(255),
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP,
  challenges_solved INT DEFAULT 0,
  rank INT DEFAULT 0,
  last_activity TIMESTAMP
);
```

## 🔧 Common Administrative Tasks

### Check User Count
```bash
mysql -u root -pWonka2024! ctf_platform -e "SELECT COUNT(*) FROM users;"
```

### View Admin Users
```bash
mysql -u root -pWonka2024! ctf_platform -e "SELECT email FROM users WHERE is_admin = 1;"
```

### Check Active Containers
```bash
docker ps | grep juice-shop
```

### Restart a User's Instance
```bash
docker restart juice-user-[1-5]
```

### View Cloudflare Tunnel Status
```bash
systemctl status cloudflared
```

## 📝 Notes

- The platform supports 5 concurrent users with isolated Juice Shop instances
- Each user gets their own Docker container automatically assigned on registration
- Cloudflare tunnels provide HTTPS access to all instances
- The standalone instance on port 5000 is for direct challenge solving/testing
- All 110 challenges are enabled on the standalone instance (including dangerous ones)
- Email verification is disabled for easier testing
- The admin panel shows real-time statistics and user activity

## 🚨 Important Security Notes

- Change default passwords in production environment
- Enable email verification for production use
- Consider implementing rate limiting
- Add SSL certificates if not using Cloudflare
- Regular backup of the database is recommended
- Monitor Docker container resource usage

---

**Last Updated**: January 2025  
**Platform Version**: 1.0  
**Juice Shop Version**: v17.1.1