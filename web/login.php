<?php
// EDUCATIONAL PURPOSE ONLY - INTENTIONALLY VULNERABLE CODE
// DO NOT USE IN PRODUCTION

// Check if lab is enabled
$config_file = '/var/www/html/sql-lab-config.json';
$lab_enabled = true; // Default to true if config doesn't exist

if (file_exists($config_file)) {
    $config = json_decode(file_get_contents($config_file), true);
    $lab_enabled = $config['lab_enabled'];
}

// Database connection
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

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    // Check if lab is enabled for SQL injection vulnerability
    if ($lab_enabled) {
        // VULNERABLE CODE - Direct SQL concatenation (DO NOT USE IN PRODUCTION)
        // This is intentionally vulnerable for educational purposes
        $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    } else {
        // SECURE CODE - Using prepared statements when lab is disabled
        $query = "SELECT * FROM users WHERE username = :username AND password = :password";
    }
    
    // Debug mode - shows the actual query being executed (educational purposes)
    if ($lab_enabled) {
        echo "<!-- DEBUG: SQL Query = $query -->\n";
    }
    
    try {
        if ($lab_enabled) {
            // Execute vulnerable query directly
            $result = $conn->query($query);
        } else {
            // Execute secure query with prepared statement
            $stmt = $conn->prepare($query);
            $stmt->bindParam(':username', $username);
            $stmt->bindParam(':password', $password);
            $stmt->execute();
            $result = $stmt;
        }
        
        if ($result && $result->rowCount() > 0) {
            $user = $result->fetch(PDO::FETCH_ASSOC);
            
            // Start session and redirect to dashboard
            session_start();
            $_SESSION['username'] = $user['username'];
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['is_admin'] = $user['is_admin'];
            
            header("Location: dashboard.php");
            exit();
        } else {
            // Login failed
            header("Location: index.php?error=Invalid credentials");
            exit();
        }
    } catch(PDOException $e) {
        // In production, never show detailed errors. This is for educational purposes.
        echo "<div style='background: #fee; padding: 20px; margin: 20px; border: 1px solid #fcc;'>";
        echo "<h2>SQL Error (Educational Mode)</h2>";
        echo "<p><strong>Error:</strong> " . htmlspecialchars($e->getMessage()) . "</p>";
        echo "<p><strong>Query:</strong> <code>" . htmlspecialchars($query) . "</code></p>";
        echo "<p><a href='index.php'>Go back</a></p>";
        echo "</div>";
    }
}
?>