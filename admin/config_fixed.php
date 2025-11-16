<?php
// Admin Panel Configuration
session_start();

// Database configuration - NO PASSWORD NEEDED for root
define('DB_HOST', 'localhost');
define('DB_NAME', 'ctf_platform');
define('DB_USER', 'root');
define('DB_PASS', ''); // No password for root user

// Admin credentials - Updated to wonkatech.org
define('ADMIN_EMAIL', 'admin@wonkatech.org');
define('ADMIN_PASSWORD_HASH', password_hash('WonkaAdmin2024!', PASSWORD_DEFAULT));

// Juice Shop configuration - Use HTTPS
define('JUICE_BASE_URL', 'https://wonkatech.org');
define('JUICE_PORTS', [3001, 3002, 3003, 3004, 3005]);

// Session configuration
define('SESSION_TIMEOUT', 3600); // 1 hour
define('ADMIN_SESSION_NAME', 'wonka_admin_session');

// Security settings
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOCKOUT_TIME', 900); // 15 minutes

// Force HTTPS
if (!isset($_SERVER['HTTPS']) || $_SERVER['HTTPS'] !== 'on') {
    if (!isset($_SERVER['HTTP_X_FORWARDED_PROTO']) || $_SERVER['HTTP_X_FORWARDED_PROTO'] !== 'https') {
        // Only redirect if not already on HTTPS (check for Cloudflare)
        if (php_sapi_name() !== 'cli') {
            // Don't redirect for localhost/direct IP access
            if ($_SERVER['HTTP_HOST'] === 'wonkatech.org' || $_SERVER['HTTP_HOST'] === 'www.wonkatech.org') {
                header("Location: https://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
                exit();
            }
        }
    }
}

// Create database connection
function getDBConnection() {
    try {
        $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
        if ($conn->connect_error) {
            throw new Exception("Connection failed: " . $conn->connect_error);
        }
        $conn->set_charset("utf8mb4");
        return $conn;
    } catch (Exception $e) {
        error_log("Database connection error: " . $e->getMessage());
        die("Database connection failed. Please contact administrator.");
    }
}

// Check if user is admin
function checkAdminAuth() {
    if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
        header("Location: admin_login.php");
        exit();
    }
    
    // Check session timeout
    if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity'] > SESSION_TIMEOUT)) {
        session_unset();
        session_destroy();
        header("Location: admin_login.php?timeout=1");
        exit();
    }
    $_SESSION['last_activity'] = time();
}

// Log admin activity
function logAdminActivity($action, $details = null, $user_id = null) {
    $conn = getDBConnection();
    $admin_email = $_SESSION['admin_email'] ?? 'system';
    $ip_address = $_SERVER['REMOTE_ADDR'] ?? '';
    $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? '';
    
    $stmt = $conn->prepare("INSERT INTO audit_log (user_id, action, details, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)");
    $details_json = json_encode($details);
    $stmt->bind_param("issss", $user_id, $action, $details_json, $ip_address, $user_agent);
    $stmt->execute();
    $stmt->close();
    $conn->close();
}

// CSRF token functions
function generateCSRFToken() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function verifyCSRFToken($token) {
    if (!isset($_SESSION['csrf_token']) || $token !== $_SESSION['csrf_token']) {
        die("CSRF token validation failed");
    }
}
?>