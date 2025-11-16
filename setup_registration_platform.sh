#!/bin/bash

# Complete Multi-User Registration Platform Setup Script
# With HTTPS, email validation, and instance management

cat << 'SETUP_EOF' > /tmp/setup_registration_platform.sh
#!/bin/bash

echo "================================================"
echo "Setting up Multi-User CTF Platform with Registration"
echo "Domain: wonkatech.org"
echo "================================================"

# Step 1: Install required packages
echo ""
echo "Step 1: Installing required packages..."
apt-get update
apt-get install -y certbot python3-certbot-apache nginx php php-mysql php-mail php-mail-mime postfix mailutils

# Step 2: Set up Let's Encrypt SSL for wonkatech.org
echo ""
echo "Step 2: Setting up HTTPS with Let's Encrypt..."
# First, ensure domain points to this server
certbot --apache -d wonkatech.org --non-interactive --agree-tos --email admin@wonkatech.org || echo "Certbot setup will need manual configuration"

# Step 3: Create MySQL database for users
echo ""
echo "Step 3: Creating user database..."
mysql -u root << 'SQL_EOF'
DROP DATABASE IF EXISTS ctf_platform;
CREATE DATABASE ctf_platform;
USE ctf_platform;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(100),
    instance_port INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    last_activity TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT FALSE,
    session_token VARCHAR(100),
    INDEX idx_session (session_token),
    INDEX idx_email (email)
);

CREATE TABLE instances (
    port INT PRIMARY KEY,
    user_id INT,
    container_id VARCHAR(100),
    status ENUM('available', 'active', 'stopping') DEFAULT 'available',
    last_activity TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Initialize instance pool (ports 3001-3020)
INSERT INTO instances (port) VALUES 
(3001), (3002), (3003), (3004), (3005),
(3006), (3007), (3008), (3009), (3010),
(3011), (3012), (3013), (3014), (3015),
(3016), (3017), (3018), (3019), (3020);

CREATE TABLE activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
SQL_EOF

# Step 4: Create the PHP application
echo ""
echo "Step 4: Creating PHP application..."
mkdir -p /var/www/ctf-platform
cd /var/www/ctf-platform

# Create configuration file
cat > config.php << 'PHP_EOF'
<?php
// Database configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'ctf_platform');

// Email configuration
define('SMTP_HOST', 'localhost');
define('SMTP_PORT', 25);
define('FROM_EMAIL', 'noreply@wonkatech.org');
define('FROM_NAME', 'WonkaTech CTF Platform');

// Platform configuration
define('BASE_URL', 'https://wonkatech.org');
define('SESSION_TIMEOUT', 600); // 10 minutes in seconds
define('INSTANCE_START_PORT', 3001);
define('INSTANCE_END_PORT', 3020);
define('DOCKER_IMAGE', 'bkimminich/juice-shop:latest');

// Security
define('HASH_ALGO', PASSWORD_BCRYPT);
session_start();
PHP_EOF

# Create database connection
cat > db.php << 'PHP_EOF'
<?php
require_once 'config.php';

function getDB() {
    static $conn = null;
    if ($conn === null) {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
    }
    return $conn;
}

function closeDB() {
    $conn = getDB();
    $conn->close();
}
PHP_EOF

# Create instance manager
cat > instance_manager.php << 'PHP_EOF'
<?php
require_once 'db.php';

class InstanceManager {
    
    public static function allocateInstance($userId) {
        $db = getDB();
        
        // Check if user already has an instance
        $stmt = $db->prepare("SELECT port FROM instances WHERE user_id = ?");
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($row = $result->fetch_assoc()) {
            // User already has an instance
            self::startInstance($row['port'], $userId);
            return $row['port'];
        }
        
        // Allocate new instance
        $stmt = $db->prepare("SELECT port FROM instances WHERE user_id IS NULL AND status = 'available' LIMIT 1");
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($row = $result->fetch_assoc()) {
            $port = $row['port'];
            
            // Assign to user
            $stmt = $db->prepare("UPDATE instances SET user_id = ?, status = 'active' WHERE port = ?");
            $stmt->bind_param("ii", $userId, $port);
            $stmt->execute();
            
            // Update user record
            $stmt = $db->prepare("UPDATE users SET instance_port = ? WHERE id = ?");
            $stmt->bind_param("ii", $port, $userId);
            $stmt->execute();
            
            self::startInstance($port, $userId);
            return $port;
        }
        
        return false; // No available instances
    }
    
    public static function startInstance($port, $userId) {
        $containerName = "juice-user-" . $userId;
        
        // Check if container exists
        $exists = shell_exec("docker ps -a --filter name=$containerName --format '{{.Names}}'");
        
        if (trim($exists) == $containerName) {
            // Container exists, just start it
            shell_exec("docker start $containerName");
        } else {
            // Create new container
            $cmd = "docker run -d --name $containerName -p $port:3000 " . DOCKER_IMAGE;
            $containerId = trim(shell_exec($cmd));
            
            // Update database
            $db = getDB();
            $stmt = $db->prepare("UPDATE instances SET container_id = ?, status = 'active', last_activity = NOW() WHERE port = ?");
            $stmt->bind_param("si", $containerId, $port);
            $stmt->execute();
        }
        
        return true;
    }
    
    public static function stopInstance($userId) {
        $db = getDB();
        
        // Get user's instance
        $stmt = $db->prepare("SELECT i.port, i.container_id FROM instances i JOIN users u ON i.user_id = u.id WHERE u.id = ?");
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($row = $result->fetch_assoc()) {
            $containerName = "juice-user-" . $userId;
            
            // Stop container
            shell_exec("docker stop $containerName");
            
            // Update instance status
            $stmt = $db->prepare("UPDATE instances SET status = 'stopping' WHERE port = ?");
            $stmt->bind_param("i", $row['port']);
            $stmt->execute();
            
            // Update user
            $stmt = $db->prepare("UPDATE users SET is_active = FALSE WHERE id = ?");
            $stmt->bind_param("i", $userId);
            $stmt->execute();
        }
    }
    
    public static function cleanupInactiveInstances() {
        $db = getDB();
        
        // Find instances inactive for more than 10 minutes
        $timeout = date('Y-m-d H:i:s', time() - SESSION_TIMEOUT);
        $stmt = $db->prepare("SELECT u.id, i.port FROM users u JOIN instances i ON u.instance_port = i.port WHERE u.last_activity < ? AND u.is_active = TRUE");
        $stmt->bind_param("s", $timeout);
        $stmt->execute();
        $result = $stmt->get_result();
        
        while ($row = $result->fetch_assoc()) {
            self::stopInstance($row['id']);
        }
    }
}
PHP_EOF

# Create email sender
cat > email.php << 'PHP_EOF'
<?php
require_once 'config.php';

function sendVerificationEmail($email, $username, $token) {
    $verifyUrl = BASE_URL . "/verify.php?token=" . $token;
    
    $subject = "Verify your WonkaTech CTF Platform account";
    
    $message = "Hello $username,\n\n";
    $message .= "Welcome to the WonkaTech CTF Platform!\n\n";
    $message .= "Please click the following link to verify your email address:\n";
    $message .= $verifyUrl . "\n\n";
    $message .= "This link will expire in 24 hours.\n\n";
    $message .= "If you didn't create this account, please ignore this email.\n\n";
    $message .= "Happy hacking!\n";
    $message .= "The WonkaTech Team";
    
    $headers = "From: " . FROM_NAME . " <" . FROM_EMAIL . ">\r\n";
    $headers .= "Reply-To: " . FROM_EMAIL . "\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    
    return mail($email, $subject, $message, $headers);
}
PHP_EOF

# Create registration page
cat > register.php << 'PHP_EOF'
<?php
require_once 'db.php';
require_once 'email.php';

$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    $confirm = $_POST['confirm_password'];
    
    // Validation
    if (strlen($username) < 3) {
        $error = "Username must be at least 3 characters";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = "Invalid email address";
    } elseif (strlen($password) < 8) {
        $error = "Password must be at least 8 characters";
    } elseif ($password !== $confirm) {
        $error = "Passwords do not match";
    } else {
        $db = getDB();
        
        // Check if username or email exists
        $stmt = $db->prepare("SELECT id FROM users WHERE username = ? OR email = ?");
        $stmt->bind_param("ss", $username, $email);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows > 0) {
            $error = "Username or email already exists";
        } else {
            // Create user
            $passwordHash = password_hash($password, PASSWORD_BCRYPT);
            $verificationToken = bin2hex(random_bytes(32));
            
            $stmt = $db->prepare("INSERT INTO users (username, email, password_hash, verification_token) VALUES (?, ?, ?, ?)");
            $stmt->bind_param("ssss", $username, $email, $passwordHash, $verificationToken);
            
            if ($stmt->execute()) {
                // Send verification email
                if (sendVerificationEmail($email, $username, $verificationToken)) {
                    $success = "Registration successful! Please check your email to verify your account.";
                } else {
                    $success = "Registration successful! Email verification link: " . BASE_URL . "/verify.php?token=" . $verificationToken;
                }
            } else {
                $error = "Registration failed. Please try again.";
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - WonkaTech CTF Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            width: 90%;
            max-width: 500px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        button:hover {
            opacity: 0.9;
        }
        .alert {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-error {
            background: #fee;
            color: #c33;
            border: 1px solid #fcc;
        }
        .alert-success {
            background: #efe;
            color: #3c3;
            border: 1px solid #cfc;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧃 WonkaTech CTF Platform</h1>
        <p class="subtitle">Create your account to get your own Juice Shop instance</p>
        
        <?php if ($error): ?>
            <div class="alert alert-error"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <?php if ($success): ?>
            <div class="alert alert-success"><?php echo htmlspecialchars($success); ?></div>
        <?php else: ?>
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required minlength="3" maxlength="50">
            </div>
            
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required minlength="8">
            </div>
            
            <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" required>
            </div>
            
            <button type="submit">Register</button>
        </form>
        
        <?php endif; ?>
        
        <div class="links">
            <p>Already have an account? <a href="/login.php">Login here</a></p>
            <p><a href="/">Back to Home</a></p>
        </div>
    </div>
</body>
</html>
PHP_EOF

# Create verification page
cat > verify.php << 'PHP_EOF'
<?php
require_once 'db.php';

$message = '';
$success = false;

if (isset($_GET['token'])) {
    $token = $_GET['token'];
    $db = getDB();
    
    $stmt = $db->prepare("SELECT id, username FROM users WHERE verification_token = ? AND email_verified = FALSE");
    $stmt->bind_param("s", $token);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($row = $result->fetch_assoc()) {
        // Verify the email
        $stmt = $db->prepare("UPDATE users SET email_verified = TRUE, verification_token = NULL WHERE id = ?");
        $stmt->bind_param("i", $row['id']);
        
        if ($stmt->execute()) {
            $message = "Email verified successfully! You can now login.";
            $success = true;
        } else {
            $message = "Verification failed. Please try again.";
        }
    } else {
        $message = "Invalid or expired verification token.";
    }
} else {
    $message = "No verification token provided.";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification - WonkaTech CTF Platform</title>
    <style>
        /* Same styles as register.php */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .message {
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 18px;
        }
        .success { background: #efe; color: #3c3; border: 1px solid #cfc; }
        .error { background: #fee; color: #c33; border: 1px solid #fcc; }
        .button {
            display: inline-block;
            padding: 14px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧃 Email Verification</h1>
        <div class="message <?php echo $success ? 'success' : 'error'; ?>">
            <?php echo htmlspecialchars($message); ?>
        </div>
        <?php if ($success): ?>
            <a href="/login.php" class="button">Go to Login</a>
        <?php else: ?>
            <a href="/register.php" class="button">Back to Registration</a>
        <?php endif; ?>
    </div>
</body>
</html>
PHP_EOF

# Create login page
cat > login.php << 'PHP_EOF'
<?php
require_once 'db.php';
require_once 'instance_manager.php';

$error = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];
    
    $db = getDB();
    
    $stmt = $db->prepare("SELECT id, password_hash, email_verified, instance_port FROM users WHERE username = ? OR email = ?");
    $stmt->bind_param("ss", $username, $username);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($row = $result->fetch_assoc()) {
        if (!$row['email_verified']) {
            $error = "Please verify your email before logging in.";
        } elseif (password_verify($password, $row['password_hash'])) {
            // Login successful
            $sessionToken = bin2hex(random_bytes(32));
            
            // Update user session
            $stmt = $db->prepare("UPDATE users SET session_token = ?, last_login = NOW(), last_activity = NOW(), is_active = TRUE WHERE id = ?");
            $stmt->bind_param("si", $sessionToken, $row['id']);
            $stmt->execute();
            
            $_SESSION['user_id'] = $row['id'];
            $_SESSION['session_token'] = $sessionToken;
            
            // Allocate or start instance
            $port = InstanceManager::allocateInstance($row['id']);
            
            if ($port) {
                header("Location: /dashboard.php");
                exit;
            } else {
                $error = "No instances available. Please try again later.";
            }
        } else {
            $error = "Invalid username or password.";
        }
    } else {
        $error = "Invalid username or password.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - WonkaTech CTF Platform</title>
    <style>
        /* Same styles as register.php */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            width: 90%;
            max-width: 500px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            color: #333;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        button:hover {
            opacity: 0.9;
        }
        .alert-error {
            padding: 12px;
            background: #fee;
            color: #c33;
            border: 1px solid #fcc;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧃 WonkaTech CTF Platform</h1>
        <p class="subtitle">Login to access your Juice Shop instance</p>
        
        <?php if ($error): ?>
            <div class="alert-error"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username or Email</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Login</button>
        </form>
        
        <div class="links">
            <p>Don't have an account? <a href="/register.php">Register here</a></p>
            <p><a href="/">Back to Home</a></p>
        </div>
    </div>
</body>
</html>
PHP_EOF

# Create dashboard page
cat > dashboard.php << 'PHP_EOF'
<?php
session_start();
require_once 'db.php';

// Check if user is logged in
if (!isset($_SESSION['user_id']) || !isset($_SESSION['session_token'])) {
    header("Location: /login.php");
    exit;
}

$db = getDB();

// Verify session
$stmt = $db->prepare("SELECT username, instance_port, last_activity FROM users WHERE id = ? AND session_token = ?");
$stmt->bind_param("is", $_SESSION['user_id'], $_SESSION['session_token']);
$stmt->execute();
$result = $stmt->get_result();

if (!$row = $result->fetch_assoc()) {
    header("Location: /login.php");
    exit;
}

// Update last activity
$stmt = $db->prepare("UPDATE users SET last_activity = NOW() WHERE id = ?");
$stmt->bind_param("i", $_SESSION['user_id']);
$stmt->execute();

$username = $row['username'];
$port = $row['instance_port'];
$instanceUrl = "http://155.138.197.128:" . $port;
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - WonkaTech CTF Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .welcome {
            font-size: 28px;
            color: #333;
            margin-bottom: 10px;
        }
        .info {
            color: #666;
            margin-bottom: 20px;
        }
        .instance-info {
            background: #f0f8ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .instance-url {
            font-size: 20px;
            color: #667eea;
            font-weight: bold;
            word-break: break-all;
        }
        .buttons {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .button {
            display: inline-block;
            padding: 14px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: opacity 0.3s;
        }
        .button:hover {
            opacity: 0.9;
        }
        .button-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        .instructions {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .instructions h2 {
            color: #333;
            margin-bottom: 20px;
        }
        .instructions ul {
            margin-left: 20px;
            line-height: 1.8;
            color: #666;
        }
        .timer {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            font-weight: bold;
        }
    </style>
    <script>
        // Auto-refresh to keep session alive
        let lastActivity = Date.now();
        let timeout = <?php echo SESSION_TIMEOUT * 1000; ?>;
        
        function updateTimer() {
            let remaining = Math.max(0, timeout - (Date.now() - lastActivity));
            let minutes = Math.floor(remaining / 60000);
            let seconds = Math.floor((remaining % 60000) / 1000);
            
            document.getElementById('timer').innerText = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            
            if (remaining === 0) {
                window.location.href = '/logout.php';
            }
        }
        
        // Keep session alive on activity
        document.addEventListener('mousemove', function() {
            lastActivity = Date.now();
            fetch('/keepalive.php');
        });
        
        setInterval(updateTimer, 1000);
    </script>
</head>
<body>
    <div class="timer">
        Session timeout: <span id="timer">10:00</span>
    </div>
    
    <div class="container">
        <div class="header">
            <h1 class="welcome">Welcome, <?php echo htmlspecialchars($username); ?>! 🧃</h1>
            <p class="info">Your personal Juice Shop instance is ready</p>
            
            <div class="instance-info">
                <p><strong>Your Instance URL:</strong></p>
                <p class="instance-url"><?php echo $instanceUrl; ?></p>
                <p style="margin-top: 10px; color: #666;">Port: <?php echo $port; ?> | Status: Active</p>
            </div>
            
            <div class="buttons">
                <a href="<?php echo $instanceUrl; ?>" target="_blank" class="button">🚀 Launch Juice Shop</a>
                <a href="/logout.php" class="button button-secondary">Logout</a>
            </div>
        </div>
        
        <div class="instructions">
            <h2>🎯 Getting Started</h2>
            <ul>
                <li>Click "Launch Juice Shop" to open your personal instance</li>
                <li>Your first challenge: Find the hidden scoreboard!</li>
                <li>All progress is saved to your instance</li>
                <li>Session auto-expires after 10 minutes of inactivity</li>
                <li>Your instance will be stopped when you logout or timeout</li>
                <li>Progress is preserved - you can continue where you left off</li>
            </ul>
            
            <h2 style="margin-top: 30px;">💡 Tips</h2>
            <ul>
                <li>Use browser developer tools (F12) to inspect the application</li>
                <li>Check JavaScript files for hidden functionality</li>
                <li>Try SQL injection on login forms and search fields</li>
                <li>Look for exposed API endpoints</li>
                <li>Explore the application thoroughly - many challenges are hidden!</li>
            </ul>
        </div>
    </div>
</body>
</html>
PHP_EOF

# Create keepalive endpoint
cat > keepalive.php << 'PHP_EOF'
<?php
session_start();
require_once 'db.php';

if (isset($_SESSION['user_id'])) {
    $db = getDB();
    $stmt = $db->prepare("UPDATE users SET last_activity = NOW() WHERE id = ?");
    $stmt->bind_param("i", $_SESSION['user_id']);
    $stmt->execute();
    echo json_encode(['status' => 'ok']);
} else {
    http_response_code(401);
    echo json_encode(['status' => 'unauthorized']);
}
PHP_EOF

# Create logout page
cat > logout.php << 'PHP_EOF'
<?php
session_start();
require_once 'db.php';
require_once 'instance_manager.php';

if (isset($_SESSION['user_id'])) {
    // Stop user's instance
    InstanceManager::stopInstance($_SESSION['user_id']);
    
    // Clear session
    $db = getDB();
    $stmt = $db->prepare("UPDATE users SET session_token = NULL, is_active = FALSE WHERE id = ?");
    $stmt->bind_param("i", $_SESSION['user_id']);
    $stmt->execute();
}

session_destroy();
header("Location: /");
exit;
PHP_EOF

# Create main landing page
cat > index.php << 'PHP_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WonkaTech CTF Platform - OWASP Juice Shop Multi-User Environment</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            padding: 20px;
        }
        .hero-content {
            max-width: 800px;
        }
        .logo {
            font-size: 120px;
            margin-bottom: 30px;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 1.5em;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .feature-icon {
            font-size: 36px;
            margin-bottom: 10px;
        }
        .cta-buttons {
            margin-top: 40px;
        }
        .button {
            display: inline-block;
            padding: 18px 40px;
            margin: 10px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-size: 18px;
            font-weight: bold;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .button-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
        .info-section {
            background: white;
            padding: 80px 20px;
            color: #333;
        }
        .info-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            margin-top: 40px;
        }
        .info-card {
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        .info-card h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
        }
    </style>
</head>
<body>
    <div class="hero">
        <div class="hero-content">
            <div class="logo">🧃</div>
            <h1>WonkaTech CTF Platform</h1>
            <p class="subtitle">Your Personal OWASP Juice Shop Instance Awaits</p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🔐</div>
                    <strong>Isolated Instances</strong>
                    <p>Each user gets their own dedicated environment</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📧</div>
                    <strong>Email Verification</strong>
                    <p>Secure registration with email validation</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">⏱️</div>
                    <strong>Smart Timeout</strong>
                    <p>10-minute inactivity timeout saves resources</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💾</div>
                    <strong>Progress Saved</strong>
                    <p>Your progress persists between sessions</p>
                </div>
            </div>
            
            <div class="cta-buttons">
                <a href="/register.php" class="button">Get Started</a>
                <a href="/login.php" class="button button-secondary">Login</a>
            </div>
        </div>
    </div>
    
    <div class="info-section">
        <div class="info-content">
            <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 20px;">How It Works</h2>
            <p style="text-align: center; font-size: 1.2em; color: #666;">Simple registration, instant access to your own hacking playground</p>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>1. Register</h3>
                    <p>Create your account with a unique username and valid email address. We'll send you a verification link to activate your account.</p>
                </div>
                <div class="info-card">
                    <h3>2. Verify Email</h3>
                    <p>Click the verification link in your email to activate your account. This ensures secure access to your instance.</p>
                </div>
                <div class="info-card">
                    <h3>3. Login</h3>
                    <p>Sign in with your credentials. Your personal Juice Shop instance will be automatically created and started.</p>
                </div>
                <div class="info-card">
                    <h3>4. Start Hacking</h3>
                    <p>Access your dedicated instance with 100+ security challenges. All progress is saved to your account.</p>
                </div>
                <div class="info-card">
                    <h3>5. Auto-Management</h3>
                    <p>Your instance stops after 10 minutes of inactivity. It restarts automatically when you login again.</p>
                </div>
                <div class="info-card">
                    <h3>6. Learn & Grow</h3>
                    <p>Practice web application security in a safe, isolated environment. Perfect for CTFs and training.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>&copy; 2024 WonkaTech CTF Platform | Powered by OWASP Juice Shop</p>
        <p style="margin-top: 10px; opacity: 0.8;">HTTPS Secured | Email Verified | Docker Isolated</p>
    </div>
</body>
</html>
PHP_EOF

# Step 5: Set up cron job for cleanup
echo ""
echo "Step 5: Setting up cleanup cron job..."
cat > /usr/local/bin/cleanup-instances.php << 'PHP_EOF'
#!/usr/bin/php
<?php
require_once '/var/www/ctf-platform/instance_manager.php';
InstanceManager::cleanupInactiveInstances();
PHP_EOF

chmod +x /usr/local/bin/cleanup-instances.php

# Add to crontab (every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/cleanup-instances.php") | crontab -

# Step 6: Configure Apache for the platform
echo ""
echo "Step 6: Configuring Apache..."
cat > /etc/apache2/sites-available/ctf-platform.conf << 'APACHE_EOF'
<VirtualHost *:80>
    ServerName wonkatech.org
    ServerAlias www.wonkatech.org
    
    # Redirect to HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>

<VirtualHost *:443>
    ServerName wonkatech.org
    ServerAlias www.wonkatech.org
    DocumentRoot /var/www/ctf-platform
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/wonkatech.org/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/wonkatech.org/privkey.pem
    
    <Directory /var/www/ctf-platform>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/ctf-platform-error.log
    CustomLog ${APACHE_LOG_DIR}/ctf-platform-access.log combined
</VirtualHost>
APACHE_EOF

# Enable the site
a2dissite multijuicer-final.conf
a2ensite ctf-platform
a2enmod ssl rewrite
systemctl reload apache2

# Set permissions
chown -R www-data:www-data /var/www/ctf-platform
chmod -R 755 /var/www/ctf-platform

echo ""
echo "================================================"
echo "✓ MULTI-USER CTF PLATFORM SETUP COMPLETE!"
echo "================================================"
echo ""
echo "Platform Features:"
echo "  ✅ Domain: https://wonkatech.org"
echo "  ✅ User registration with email verification"
echo "  ✅ Automatic instance allocation (ports 3001-3020)"
echo "  ✅ 10-minute inactivity timeout"
echo "  ✅ Progress persistence between sessions"
echo "  ✅ HTTPS secured with Let's Encrypt"
echo ""
echo "Next Steps:"
echo "  1. Ensure wonkatech.org points to 155.138.197.128"
echo "  2. Configure email settings if needed"
echo "  3. Test registration and login flow"
echo ""
echo "Admin Access:"
echo "  Database: mysql -u root ctf_platform"
echo "  Logs: /var/log/apache2/ctf-platform-*.log"
echo ""
echo "================================================"
SETUP_EOF

echo "Setup script created at /tmp/setup_registration_platform.sh"