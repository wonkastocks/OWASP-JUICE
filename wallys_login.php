<?php
// Wally's Monkey Parts - Vulnerable Login System
// EDUCATIONAL PURPOSE ONLY - SQL INJECTION DEMO

session_start();

// Check if SQL injection lab is enabled
$config_file = '/var/www/html/sql-lab-config.json';
$lab_enabled = true; // Default to true for demo

if (file_exists($config_file)) {
    $config = json_decode(file_get_contents($config_file), true);
    $lab_enabled = $config['lab_enabled'] ?? true;
}

// Database connection
$host = 'localhost';
$dbname = 'wallys_monkey_parts';
$db_user = 'wallys_web';
$db_pass = 'MonkeyWeb123!';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $db_user, $db_pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("<div style='background: #fee; padding: 20px; margin: 20px; border: 1px solid #fcc;'>
         <h2>Database Connection Failed</h2>
         <p>Unable to connect to Wally's database.</p>
         </div>");
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if ($lab_enabled) {
        // VULNERABLE CODE - Direct SQL concatenation with MD5
        // This allows SQL injection attacks
        $md5_password = md5($password);
        $query = "SELECT * FROM users WHERE username = '$username' AND password = '$md5_password'";
        
        // Educational debug mode - shows the query
        if (isset($_GET['debug'])) {
            echo "<!-- SQL Query: $query -->\n";
        }
    } else {
        // SECURE CODE - Using prepared statements
        $query = "SELECT * FROM users WHERE username = :username AND password = :password";
    }
    
    try {
        if ($lab_enabled) {
            // Execute vulnerable query
            $result = $conn->query($query);
        } else {
            // Execute secure query with prepared statement
            $stmt = $conn->prepare($query);
            $stmt->bindParam(':username', $username);
            $md5_password = md5($password);
            $stmt->bindParam(':password', $md5_password);
            $stmt->execute();
            $result = $stmt;
        }
        
        if ($result && $result->rowCount() > 0) {
            $user = $result->fetch(PDO::FETCH_ASSOC);
            
            // Log successful login
            $log_query = "INSERT INTO access_logs (user_id, action, ip_address, user_agent) 
                         VALUES (?, 'Login successful', ?, ?)";
            $log_stmt = $conn->prepare($log_query);
            $log_stmt->execute([$user['id'], $_SERVER['REMOTE_ADDR'], $_SERVER['HTTP_USER_AGENT']]);
            
            // Set session variables
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            $_SESSION['full_name'] = $user['full_name'];
            $_SESSION['role'] = $user['role'];
            $_SESSION['is_admin'] = $user['is_admin'];
            $_SESSION['ssh_access'] = $user['ssh_access'];
            $_SESSION['email'] = $user['email'];
            
            // Redirect to dashboard
            header("Location: wallys_dashboard.php");
            exit();
        } else {
            $error = "Invalid username or password";
        }
    } catch(PDOException $e) {
        if ($lab_enabled) {
            // Educational error display - shows SQL errors
            $error_display = true;
            $sql_error = $e->getMessage();
            $sql_query = $query;
        } else {
            $error = "Login failed. Please try again.";
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Wally's Monkey Parts - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .login-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 450px;
            overflow: hidden;
        }
        .login-header {
            background: linear-gradient(135deg, #8B4513, #A0522D);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .login-header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        .login-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        .monkey-emoji {
            font-size: 48px;
            margin-bottom: 10px;
        }
        .login-form {
            padding: 40px;
        }
        .form-group {
            margin-bottom: 25px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #8B4513;
        }
        .login-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #8B4513, #A0522D);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .login-btn:hover {
            transform: translateY(-2px);
        }
        .lab-status {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
        }
        .lab-enabled {
            background: #ffebcd;
            color: #8B4513;
            border: 2px solid #D2691E;
        }
        .lab-disabled {
            background: #e8f5e9;
            color: #2e7d32;
            border: 2px solid #4caf50;
        }
        .error-box {
            background: #fee;
            border: 2px solid #f44336;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .sql-error {
            background: #fff3e0;
            border: 2px solid #ff9800;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .sql-error h3 {
            color: #e65100;
            margin-bottom: 10px;
        }
        .sql-error pre {
            background: #263238;
            color: #aed581;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin-top: 10px;
        }
        .hint-box {
            background: #fff8e1;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
        }
        .hint-box strong {
            color: #f57c00;
        }
        .hint-box code {
            background: #263238;
            color: #aed581;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="monkey-emoji">🐵</div>
            <h1>Wally's Monkey Parts</h1>
            <p>Premium Monkey-Themed Hardware Supplies</p>
        </div>
        
        <div class="login-form">
            <?php if ($lab_enabled): ?>
                <div class="lab-status lab-enabled">
                    ⚠️ SQL Injection Lab Mode ENABLED
                </div>
            <?php else: ?>
                <div class="lab-status lab-disabled">
                    🔒 Secure Mode Active
                </div>
            <?php endif; ?>
            
            <?php if (isset($error)): ?>
                <div class="error-box">
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php endif; ?>
            
            <?php if (isset($error_display) && $lab_enabled): ?>
                <div class="sql-error">
                    <h3>SQL Error (Educational Mode)</h3>
                    <p><strong>Error:</strong> <?php echo htmlspecialchars($sql_error); ?></p>
                    <p><strong>Query Executed:</strong></p>
                    <pre><?php echo htmlspecialchars($sql_query); ?></pre>
                </div>
            <?php endif; ?>
            
            <form method="POST" action="">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" 
                           placeholder="Enter your username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" 
                           placeholder="Enter your password" required>
                </div>
                
                <button type="submit" class="login-btn">
                    🔑 Login to Monkey Parts
                </button>
            </form>
            
            <?php if ($lab_enabled): ?>
                <div class="hint-box">
                    <strong>💡 SQL Injection Hints:</strong><br>
                    • Try: <code>admin' --</code><br>
                    • Or: <code>' OR '1'='1</code><br>
                    • Password field uses MD5 hashing<br>
                    • Add <code>?debug=1</code> to URL for query display
                </div>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>