# WonkaTech CTF Platform - Complete Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Database Schema](#database-schema)
3. [PHP Configuration](#php-configuration)
4. [Apache Configuration](#apache-configuration)
5. [Docker Configuration](#docker-configuration)
6. [Network Configuration](#network-configuration)
7. [File Structure](#file-structure)
8. [API Endpoints](#api-endpoints)
9. [Security Configuration](#security-configuration)
10. [Deployment Guide](#deployment-guide)

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           WONKATECH CTF PLATFORM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

                                    INTERNET
                                        │
                                        │
                            ┌───────────▼───────────┐
                            │                       │
                            │   CLOUDFLARE TUNNEL   │
                            │   wonkatech.org       │
                            │   (HTTPS/SSL)         │
                            │                       │
                            └───────────┬───────────┘
                                        │
                                        │
                        ┌───────────────▼────────────────┐
                        │                                │
                        │     VULTR VPS SERVER          │
                        │   155.138.197.128             │
                        │   Ubuntu 22.04.5 LTS          │
                        │   75GB Storage / 4GB RAM      │
                        │                                │
                        └───────────────┬────────────────┘
                                        │
            ┌───────────────────────────┴───────────────────────────┐
            │                                                       │
            │                    DOCKER ENGINE                      │
            │                     (Container Host)                  │
            │                                                       │
            └───────────────────────────┬───────────────────────────┘
                                        │
    ┌───────────────────────────────────┴───────────────────────────────────┐
    │                                                                       │
    │                         CONTAINERIZED SERVICES                        │
    │                                                                       │
    ├─────────────┬──────────────┬──────────────┬──────────────┬──────────┤
    │             │              │              │              │          │
┌───▼──────┐ ┌───▼──────┐ ┌────▼─────┐ ┌────▼─────┐ ┌────▼─────┐       │
│ JUICE #1 │ │ JUICE #2 │ │ JUICE #3 │ │ JUICE #4 │ │ JUICE #5 │       │
│ Port:3001│ │ Port:3002│ │ Port:3003│ │ Port:3004│ │ Port:3005│       │
│ User 1   │ │ User 2   │ │ Wonka    │ │ User 4   │ │ User 5   │       │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
```

---

## 2. Database Schema

### Main CTF Platform Database

```sql
-- Database: ctf_platform
CREATE DATABASE IF NOT EXISTS ctf_platform 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE ctf_platform;

-- Users table: Stores registered users
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires DATETIME,
    instance_url VARCHAR(255),
    instance_port INT,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login DATETIME,
    login_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_verification (verification_token),
    INDEX idx_reset (reset_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sessions table: Manage user sessions
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    user_id INT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    payload TEXT,
    last_activity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_last_activity (last_activity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Login attempts table: Track failed login attempts
CREATE TABLE login_attempts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255),
    ip_address VARCHAR(45),
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT FALSE,
    INDEX idx_email_ip (email, ip_address),
    INDEX idx_attempted (attempted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Challenge progress table: Track user progress
CREATE TABLE challenge_progress (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    challenge_name VARCHAR(255) NOT NULL,
    challenge_category VARCHAR(100),
    points INT DEFAULT 0,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_taken INT COMMENT 'Time in seconds',
    hints_used INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_challenge (user_id, challenge_name),
    INDEX idx_user (user_id),
    INDEX idx_challenge (challenge_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Scores table: Aggregate user scores
CREATE TABLE scores (
    user_id INT PRIMARY KEY,
    total_score INT DEFAULT 0,
    challenges_completed INT DEFAULT 0,
    rank INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_score (total_score DESC),
    INDEX idx_rank (rank)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Email queue table: Handle email sending
CREATE TABLE email_queue (
    id INT PRIMARY KEY AUTO_INCREMENT,
    recipient_email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    status ENUM('pending', 'sent', 'failed') DEFAULT 'pending',
    attempts INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at DATETIME,
    error_message TEXT,
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Audit log table: Track important events
CREATE TABLE audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user (user_id),
    INDEX idx_action (action),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Container management table
CREATE TABLE containers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    container_name VARCHAR(100) UNIQUE NOT NULL,
    port INT UNIQUE NOT NULL,
    user_id INT,
    status ENUM('available', 'assigned', 'maintenance') DEFAULT 'available',
    docker_container_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_at DATETIME,
    last_health_check DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_port (port)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default container records
INSERT INTO containers (container_name, port, status) VALUES
('juice-user1', 3001, 'available'),
('juice-user2', 3002, 'available'),
('juice-user3', 3003, 'assigned'),  -- Wonka
('juice-user4', 3004, 'available'),
('juice-user5', 3005, 'available');

-- Create views for easier querying
CREATE VIEW leaderboard AS
SELECT 
    u.username,
    u.email,
    s.total_score,
    s.challenges_completed,
    s.rank,
    u.created_at as member_since
FROM users u
JOIN scores s ON u.id = s.user_id
WHERE u.is_active = TRUE
ORDER BY s.total_score DESC;

CREATE VIEW active_sessions AS
SELECT 
    s.id as session_id,
    u.username,
    u.email,
    s.ip_address,
    FROM_UNIXTIME(s.last_activity) as last_active
FROM sessions s
JOIN users u ON s.user_id = u.id
WHERE s.last_activity > UNIX_TIMESTAMP() - 3600;

-- Stored procedures
DELIMITER $$

CREATE PROCEDURE assign_container(IN p_user_id INT)
BEGIN
    DECLARE v_port INT;
    DECLARE v_container_name VARCHAR(100);
    
    -- Find first available container
    SELECT port, container_name INTO v_port, v_container_name
    FROM containers
    WHERE status = 'available'
    ORDER BY port
    LIMIT 1;
    
    IF v_port IS NOT NULL THEN
        -- Update container status
        UPDATE containers 
        SET status = 'assigned', 
            user_id = p_user_id,
            assigned_at = NOW()
        WHERE port = v_port;
        
        -- Update user with instance URL
        UPDATE users 
        SET instance_url = CONCAT('http://155.138.197.128:', v_port),
            instance_port = v_port
        WHERE id = p_user_id;
        
        SELECT v_port as assigned_port, v_container_name as container_name;
    ELSE
        SELECT 0 as assigned_port, 'No containers available' as message;
    END IF;
END$$

CREATE PROCEDURE cleanup_expired_tokens()
BEGIN
    -- Clean expired reset tokens
    UPDATE users 
    SET reset_token = NULL, 
        reset_token_expires = NULL
    WHERE reset_token_expires < NOW();
    
    -- Clean old sessions
    DELETE FROM sessions 
    WHERE last_activity < UNIX_TIMESTAMP() - 86400;
    
    -- Clean old login attempts
    DELETE FROM login_attempts 
    WHERE attempted_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
END$$

DELIMITER ;

-- Indexes for OWASP Juice Shop SQLite databases (per container)
-- These are within each Juice Shop instance

/* 
SQLite Schema for each Juice Shop instance:
- Users (id, email, password, role, etc.)
- Products (id, name, description, price, etc.)
- Baskets (shopping carts)
- Challenges (CTF challenges)
- Feedbacks (customer feedback)
- And more...
*/
```

---

## 3. PHP Configuration

### PHP.ini Configuration (`/etc/php/8.1/apache2/php.ini`)

```ini
[PHP]
;;;;;;;;;;;;;;;;;;;
; About php.ini   ;
;;;;;;;;;;;;;;;;;;;

; PHP Engine Configuration
engine = On
short_open_tag = Off
precision = 14
output_buffering = 4096
zlib.output_compression = Off
implicit_flush = Off
unserialize_callback_func =
serialize_precision = -1
disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source
disable_classes =
zend.enable_gc = On
zend.exception_ignore_args = On
zend.exception_string_param_max_len = 0

; Error Handling
expose_php = Off
error_reporting = E_ALL & ~E_DEPRECATED & ~E_STRICT
display_errors = Off
display_startup_errors = Off
log_errors = On
log_errors_max_len = 1024
ignore_repeated_errors = Off
ignore_repeated_source = Off
report_memleaks = On
error_log = /var/log/php/error.log

; Data Handling
variables_order = "GPCS"
request_order = "GP"
register_argc_argv = Off
auto_globals_jit = On
post_max_size = 8M
auto_prepend_file =
auto_append_file =
default_mimetype = "text/html"
default_charset = "UTF-8"

; File Uploads
file_uploads = On
upload_tmp_dir = /tmp
upload_max_filesize = 2M
max_file_uploads = 20

; Resource Limits
max_execution_time = 30
max_input_time = 60
max_input_nesting_level = 64
max_input_vars = 1000
memory_limit = 128M

; Paths and Directories
include_path = ".:/usr/share/php"
doc_root =
user_dir =
enable_dl = Off

; Dynamic Extensions
extension_dir = "/usr/lib/php/20210902/"

; Extensions (enabled)
extension=mysqli
extension=pdo
extension=pdo_mysql
extension=mbstring
extension=openssl
extension=json
extension=curl
extension=gd
extension=zip
extension=bcmath
extension=sodium

; Module Settings

[Date]
date.timezone = "America/New_York"

[Session]
session.save_handler = files
session.save_path = "/var/lib/php/sessions"
session.use_strict_mode = 1
session.use_cookies = 1
session.use_only_cookies = 1
session.name = PHPSESSID
session.auto_start = 0
session.cookie_lifetime = 0
session.cookie_path = /
session.cookie_domain =
session.cookie_httponly = 1
session.cookie_samesite = "Lax"
session.serialize_handler = php
session.gc_probability = 1
session.gc_divisor = 1000
session.gc_maxlifetime = 1440
session.referer_check =
session.cache_limiter = nocache
session.cache_expire = 180
session.use_trans_sid = 0
session.sid_length = 26
session.trans_sid_tags = "a=href,area=href,frame=src,form="
session.sid_bits_per_character = 5

[MySQLi]
mysqli.max_persistent = -1
mysqli.allow_persistent = On
mysqli.max_links = -1
mysqli.default_port = 3306
mysqli.default_socket =
mysqli.default_host =
mysqli.default_user =
mysqli.default_pw =
mysqli.reconnect = Off

[mysqlnd]
mysqlnd.collect_statistics = On
mysqlnd.collect_memory_statistics = Off

[Mail Function]
SMTP = localhost
smtp_port = 25
mail.add_x_header = Off
mail.log = "/var/log/mail.log"

[ODBC]
odbc.allow_persistent = On
odbc.check_persistent = On
odbc.max_persistent = -1
odbc.max_links = -1
odbc.defaultlrl = 4096
odbc.defaultbinmode = 1

[PDO]
pdo_mysql.default_socket=

[opcache]
opcache.enable=1
opcache.enable_cli=0
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=10000
opcache.max_wasted_percentage=5
opcache.validate_timestamps=1
opcache.revalidate_freq=2
opcache.fast_shutdown=1
```

### PHP Application Configuration (`/var/www/html/config.php`)

```php
<?php
// Database Configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'ctf_platform');
define('DB_USER', 'ctf_user');
define('DB_PASS', 'your_secure_password_here');
define('DB_CHARSET', 'utf8mb4');

// Application Settings
define('APP_NAME', 'WonkaTech CTF Platform');
define('APP_URL', 'https://wonkatech.org');
define('APP_ENV', 'production'); // development, staging, production
define('APP_DEBUG', false);
define('APP_KEY', 'your_32_character_random_string_here');

// Session Configuration
define('SESSION_LIFETIME', 120); // minutes
define('SESSION_SECURE', true);
define('SESSION_HTTPONLY', true);
define('SESSION_SAMESITE', 'Lax');

// Email Configuration (Gmail SMTP)
define('MAIL_DRIVER', 'smtp');
define('MAIL_HOST', 'smtp.gmail.com');
define('MAIL_PORT', 587);
define('MAIL_USERNAME', 'your_email@gmail.com');
define('MAIL_PASSWORD', 'your_app_specific_password');
define('MAIL_ENCRYPTION', 'tls');
define('MAIL_FROM_ADDRESS', 'noreply@wonkatech.org');
define('MAIL_FROM_NAME', 'WonkaTech CTF');

// Security Settings
define('BCRYPT_ROUNDS', 12);
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOCKOUT_TIME', 900); // 15 minutes in seconds
define('TOKEN_EXPIRY', 3600); // 1 hour for password reset tokens
define('CSRF_TOKEN_NAME', '_token');
define('ALLOWED_ORIGINS', ['https://wonkatech.org', 'http://155.138.197.128']);

// Juice Shop Configuration
define('JUICE_SHOP_BASE_URL', 'http://155.138.197.128');
define('JUICE_SHOP_PORTS', [3001, 3002, 3003, 3004, 3005]);
define('MAX_USERS_PER_INSTANCE', 1);

// File Upload Settings
define('UPLOAD_DIR', '/var/www/uploads/');
define('MAX_UPLOAD_SIZE', 2097152); // 2MB in bytes
define('ALLOWED_EXTENSIONS', ['jpg', 'jpeg', 'png', 'gif', 'pdf']);

// Rate Limiting
define('RATE_LIMIT_REQUESTS', 60);
define('RATE_LIMIT_WINDOW', 60); // seconds

// Logging
define('LOG_LEVEL', 'error'); // debug, info, warning, error, critical
define('LOG_FILE', '/var/log/ctf_platform/app.log');

// Timezone
date_default_timezone_set('America/New_York');

// Error Reporting
if (APP_DEBUG) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Autoloader
spl_autoload_register(function ($class) {
    $file = __DIR__ . '/classes/' . str_replace('\\', '/', $class) . '.php';
    if (file_exists($file)) {
        require_once $file;
    }
});

// Database Connection Function
function getDB() {
    static $db = null;
    if ($db === null) {
        try {
            $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=' . DB_CHARSET;
            $db = new PDO($dsn, DB_USER, DB_PASS);
            $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
            $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
        } catch (PDOException $e) {
            if (APP_DEBUG) {
                die('Database connection failed: ' . $e->getMessage());
            } else {
                die('Database connection failed. Please try again later.');
            }
        }
    }
    return $db;
}

// CSRF Token Generation
function generateCSRFToken() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

// CSRF Token Validation
function validateCSRFToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

// Sanitization Functions
function sanitizeInput($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

// Password Hashing
function hashPassword($password) {
    return password_hash($password, PASSWORD_BCRYPT, ['cost' => BCRYPT_ROUNDS]);
}

// Password Verification
function verifyPassword($password, $hash) {
    return password_verify($password, $hash);
}

// Session Security
function secureSession() {
    if (!isset($_SESSION['initiated'])) {
        session_regenerate_id(true);
        $_SESSION['initiated'] = true;
    }
    
    // Session timeout
    if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity'] > SESSION_LIFETIME * 60)) {
        session_unset();
        session_destroy();
        header('Location: /login.php?timeout=1');
        exit();
    }
    $_SESSION['last_activity'] = time();
    
    // Regenerate session ID periodically
    if (!isset($_SESSION['created'])) {
        $_SESSION['created'] = time();
    } else if (time() - $_SESSION['created'] > 1800) { // 30 minutes
        session_regenerate_id(true);
        $_SESSION['created'] = time();
    }
}

// Rate Limiting
function checkRateLimit($identifier) {
    $db = getDB();
    $window_start = time() - RATE_LIMIT_WINDOW;
    
    $stmt = $db->prepare("SELECT COUNT(*) as count FROM rate_limits WHERE identifier = ? AND created_at > ?");
    $stmt->execute([$identifier, $window_start]);
    $result = $stmt->fetch();
    
    if ($result['count'] >= RATE_LIMIT_REQUESTS) {
        return false;
    }
    
    $stmt = $db->prepare("INSERT INTO rate_limits (identifier, created_at) VALUES (?, ?)");
    $stmt->execute([$identifier, time()]);
    
    return true;
}

// Logging Function
function logActivity($action, $details = null, $user_id = null) {
    $db = getDB();
    $ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
    
    $stmt = $db->prepare("INSERT INTO audit_log (user_id, action, details, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)");
    $stmt->execute([$user_id, $action, json_encode($details), $ip, $user_agent]);
}
?>
```

---

## 4. Apache Configuration

### Virtual Host Configuration (`/etc/apache2/sites-available/000-default.conf`)

```apache
<VirtualHost *:80>
    ServerName wonkatech.org
    ServerAlias www.wonkatech.org
    ServerAdmin admin@wonkatech.org
    
    DocumentRoot /var/www/html
    
    # Directory Configuration
    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
        
        # Security Headers
        Header always set X-Frame-Options "SAMEORIGIN"
        Header always set X-Content-Type-Options "nosniff"
        Header always set X-XSS-Protection "1; mode=block"
        Header always set Referrer-Policy "strict-origin-when-cross-origin"
        Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
    </Directory>
    
    # PHP Configuration
    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>
    
    # Error Documents
    ErrorDocument 404 /error/404.php
    ErrorDocument 403 /error/403.php
    ErrorDocument 500 /error/500.php
    
    # Logging
    ErrorLog ${APACHE_LOG_DIR}/ctf_error.log
    CustomLog ${APACHE_LOG_DIR}/ctf_access.log combined
    
    # ProxyPass for Juice Shop instances
    ProxyPreserveHost On
    ProxyPass /juice1 http://localhost:3001/
    ProxyPassReverse /juice1 http://localhost:3001/
    
    ProxyPass /juice2 http://localhost:3002/
    ProxyPassReverse /juice2 http://localhost:3002/
    
    ProxyPass /juice3 http://localhost:3003/
    ProxyPassReverse /juice3 http://localhost:3003/
    
    ProxyPass /juice4 http://localhost:3004/
    ProxyPassReverse /juice4 http://localhost:3004/
    
    ProxyPass /juice5 http://localhost:3005/
    ProxyPassReverse /juice5 http://localhost:3005/
    
    # Security Configurations
    <Location /admin>
        Require ip 127.0.0.1
    </Location>
    
    # Deny access to sensitive files
    <FilesMatch "^\.ht|\.env|composer\.(json|lock)|package\.(json|lock)">
        Require all denied
    </FilesMatch>
    
    # Enable compression
    <IfModule mod_deflate.c>
        AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
    </IfModule>
    
    # Cache static assets
    <IfModule mod_expires.c>
        ExpiresActive On
        ExpiresByType image/jpg "access 1 year"
        ExpiresByType image/jpeg "access 1 year"
        ExpiresByType image/gif "access 1 year"
        ExpiresByType image/png "access 1 year"
        ExpiresByType text/css "access 1 month"
        ExpiresByType application/javascript "access 1 month"
    </IfModule>
</VirtualHost>
```

### .htaccess Configuration (`/var/www/html/.htaccess`)

```apache
# Enable Rewrite Engine
RewriteEngine On

# Force HTTPS (when not using Cloudflare)
# RewriteCond %{HTTPS} !=on
# RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]

# Remove trailing slash
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.+)/$ /$1 [L,R=301]

# Remove .php extension
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}.php -f
RewriteRule ^(.+)$ $1.php [L]

# Prevent directory listing
Options -Indexes

# Deny access to hidden files
<FilesMatch "^\.">
    Order allow,deny
    Deny from all
</FilesMatch>

# Protect config files
<FilesMatch "(config|database)\.php">
    Order allow,deny
    Deny from all
</FilesMatch>

# Set default charset
AddDefaultCharset UTF-8

# Enable GZIP compression
<IfModule mod_deflate.c>
    SetOutputFilter DEFLATE
    SetEnvIfNoCase Request_URI \.(?:gif|jpe?g|png)$ no-gzip dont-vary
    SetEnvIfNoCase Request_URI \.(?:exe|t?gz|zip|bz2|sit|rar)$ no-gzip dont-vary
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-Content-Type-Options "nosniff"
    Header set X-XSS-Protection "1; mode=block"
</IfModule>

# Error pages
ErrorDocument 400 /error/400.php
ErrorDocument 401 /error/401.php
ErrorDocument 403 /error/403.php
ErrorDocument 404 /error/404.php
ErrorDocument 500 /error/500.php

# Limit file upload size
LimitRequestBody 2097152

# Block bad bots
SetEnvIfNoCase User-Agent "^$" bad_bot
SetEnvIfNoCase User-Agent "^Java" bad_bot
SetEnvIfNoCase User-Agent "^JDatabaseDriver" bad_bot
SetEnvIfNoCase User-Agent "^Microsoft URL Control" bad_bot
SetEnvIfNoCase User-Agent "^PostmanRuntime" bad_bot
SetEnvIfNoCase User-Agent "^python" bad_bot

<RequireAll>
    Require all granted
    Require not env bad_bot
</RequireAll>
```

---

## 5. Docker Configuration

### Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  juice-user1:
    image: bkimminich/juice-shop:latest
    container_name: juice-user1
    ports:
      - "3001:3000"
    environment:
      - NODE_ENV=ctf
      - CTF_KEY=your_ctf_key_here
    restart: unless-stopped
    networks:
      - ctf_network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  juice-user2:
    image: bkimminich/juice-shop:latest
    container_name: juice-user2
    ports:
      - "3002:3000"
    environment:
      - NODE_ENV=ctf
      - CTF_KEY=your_ctf_key_here
    restart: unless-stopped
    networks:
      - ctf_network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  juice-user3:
    image: bkimminich/juice-shop:latest
    container_name: juice-user3
    ports:
      - "3003:3000"
    environment:
      - NODE_ENV=ctf
      - CTF_KEY=your_ctf_key_here
    restart: unless-stopped
    networks:
      - ctf_network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  juice-user4:
    image: bkimminich/juice-shop:latest
    container_name: juice-user4
    ports:
      - "3004:3000"
    environment:
      - NODE_ENV=ctf
      - CTF_KEY=your_ctf_key_here
    restart: unless-stopped
    networks:
      - ctf_network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  juice-user5:
    image: bkimminich/juice-shop:latest
    container_name: juice-user5
    ports:
      - "3005:3000"
    environment:
      - NODE_ENV=ctf
      - CTF_KEY=your_ctf_key_here
    restart: unless-stopped
    networks:
      - ctf_network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

networks:
  ctf_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Docker Daemon Configuration (`/etc/docker/daemon.json`)

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "iptables": true,
  "live-restore": true,
  "userland-proxy": false,
  "default-address-pools": [
    {
      "base": "172.20.0.0/16",
      "size": 24
    }
  ],
  "metrics-addr": "127.0.0.1:9323",
  "experimental": false
}
```

---

## 6. Network Configuration

### UFW Firewall Rules

```bash
# UFW Configuration
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (restricted)
ufw allow from YOUR_IP_ADDRESS to any port 22

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow Juice Shop ports
ufw allow 3001:3005/tcp

# Allow MySQL (local only)
ufw allow from 127.0.0.1 to any port 3306

# Enable UFW
ufw enable
```

### Cloudflare Tunnel Configuration (`~/.cloudflared/config.yml`)

```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /root/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: wonkatech.org
    service: http://localhost:80
  - hostname: www.wonkatech.org
    service: http://localhost:80
  - service: http_status:404
```

---

## 7. File Structure

```
/var/www/html/
├── index.php           # Landing page
├── login.php           # User login
├── register.php        # User registration
├── dashboard.php       # User dashboard
├── logout.php          # Logout handler
├── verify.php          # Email verification
├── forgot-password.php # Password reset request
├── reset-password.php  # Password reset form
├── config.php          # Configuration file
├── .htaccess          # Apache configuration
│
├── assets/
│   ├── css/
│   │   ├── style.css
│   │   └── bootstrap.min.css
│   ├── js/
│   │   ├── main.js
│   │   └── jquery.min.js
│   └── images/
│       └── logo.png
│
├── includes/
│   ├── header.php
│   ├── footer.php
│   ├── db.php          # Database connection
│   └── functions.php   # Helper functions
│
├── classes/
│   ├── User.php        # User class
│   ├── Auth.php        # Authentication class
│   ├── Mailer.php      # Email handler
│   └── Container.php   # Docker container manager
│
├── error/
│   ├── 403.php
│   ├── 404.php
│   └── 500.php
│
└── admin/
    ├── index.php       # Admin dashboard
    ├── users.php       # User management
    ├── containers.php  # Container management
    └── logs.php        # View logs
```

---

## 8. API Endpoints

### Authentication Endpoints

```php
// POST /api/auth/login
// Request: { email, password }
// Response: { success, token, user }

// POST /api/auth/register
// Request: { username, email, password }
// Response: { success, message }

// POST /api/auth/logout
// Response: { success, message }

// POST /api/auth/verify
// Request: { token }
// Response: { success, message }

// POST /api/auth/forgot-password
// Request: { email }
// Response: { success, message }

// POST /api/auth/reset-password
// Request: { token, password }
// Response: { success, message }
```

### User Endpoints

```php
// GET /api/user/profile
// Response: { user_data }

// PUT /api/user/profile
// Request: { field: value }
// Response: { success, user }

// GET /api/user/scores
// Response: { scores, rank }

// GET /api/user/challenges
// Response: { completed_challenges }
```

### Challenge Endpoints

```php
// GET /api/challenges
// Response: { challenges[] }

// POST /api/challenges/complete
// Request: { challenge_id }
// Response: { success, points }

// GET /api/leaderboard
// Response: { leaderboard[] }
```

---

## 9. Security Configuration

### Security Headers (PHP)

```php
// Set security headers
header('X-Frame-Options: SAMEORIGIN');
header('X-Content-Type-Options: nosniff');
header('X-XSS-Protection: 1; mode=block');
header('Referrer-Policy: strict-origin-when-cross-origin');
header('Content-Security-Policy: default-src \'self\';');
header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
header('Permissions-Policy: geolocation=(), microphone=(), camera=()');
```

### Input Validation Functions

```php
// Email validation
function validateEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
}

// Username validation
function validateUsername($username) {
    return preg_match('/^[a-zA-Z0-9_]{3,20}$/', $username);
}

// Password strength check
function validatePassword($password) {
    return strlen($password) >= 8 &&
           preg_match('/[A-Z]/', $password) &&
           preg_match('/[a-z]/', $password) &&
           preg_match('/[0-9]/', $password);
}

// SQL Injection prevention (using PDO)
function safeQuery($sql, $params = []) {
    $db = getDB();
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    return $stmt;
}

// XSS Prevention
function escape($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}
```

---

## 10. Deployment Guide

### Initial Setup Commands

```bash
# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y apache2 php8.1 php8.1-mysql php8.1-curl php8.1-gd \
    php8.1-mbstring php8.1-xml php8.1-zip mysql-server docker.io \
    docker-compose git ufw fail2ban

# Configure MySQL
mysql_secure_installation

# Create database and user
mysql -u root -p << EOF
CREATE DATABASE ctf_platform;
CREATE USER 'ctf_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON ctf_platform.* TO 'ctf_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# Import database schema
mysql -u root -p ctf_platform < schema.sql

# Set up Apache
a2enmod rewrite proxy proxy_http headers expires deflate
systemctl restart apache2

# Deploy Juice Shop containers
for i in {1..5}; do
    docker run -d \
        --name juice-user$i \
        --restart unless-stopped \
        -p 300$i:3000 \
        -e NODE_ENV=ctf \
        bkimminich/juice-shop:latest
done

# Set up Cloudflare Tunnel
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared
cloudflared tunnel login
cloudflared tunnel create wonkatech
cloudflared tunnel route dns wonkatech wonkatech.org

# Configure firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3001:3005/tcp
ufw enable

# Set permissions
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html
chmod -R 770 /var/www/html/uploads

# Create log directory
mkdir -p /var/log/ctf_platform
chown www-data:www-data /var/log/ctf_platform

# Set up cron jobs
crontab -e
# Add:
# */5 * * * * php /var/www/html/cron/cleanup.php
# 0 * * * * docker system prune -f
# 0 2 * * * mysqldump -u root -p ctf_platform > /backup/ctf_$(date +\%Y\%m\%d).sql
```

### Monitoring Commands

```bash
# Check container status
docker ps

# View container logs
docker logs juice-user1

# Monitor system resources
htop

# Check Apache logs
tail -f /var/log/apache2/access.log
tail -f /var/log/apache2/error.log

# Check PHP logs
tail -f /var/log/php/error.log

# MySQL status
systemctl status mysql

# Check disk usage
df -h

# Network connections
netstat -tulpn
```

---

This complete documentation provides everything needed to understand, configure, and maintain the WonkaTech CTF platform!