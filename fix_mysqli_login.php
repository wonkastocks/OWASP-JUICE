<?php
// EDUCATIONAL PURPOSE ONLY - INTENTIONALLY VULNERABLE CODE
// DO NOT USE IN PRODUCTION

session_start();

// Database connection using mysqli
$host = 'localhost';
$dbname = 'vulnerable_db';
$db_user = 'web_user';
$db_pass = 'web_pass123';

// Create MySQLi connection
$conn = new mysqli($host, $db_user, $db_pass, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    // VULNERABLE CODE - Direct SQL concatenation (DO NOT USE IN PRODUCTION)
    // This is intentionally vulnerable for educational purposes
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    
    // Debug mode - shows the actual query being executed (educational purposes)
    echo "<!-- DEBUG: SQL Query = $query -->\n";
    
    // Execute query
    $result = $conn->query($query);
    
    if ($result === false) {
        // SQL error occurred - show it for educational purposes
        echo "<div style='background: #fee; padding: 20px; margin: 20px; border: 1px solid #fcc;'>";
        echo "<h2>SQL Error (Educational Mode)</h2>";
        echo "<p><strong>Error:</strong> " . htmlspecialchars($conn->error) . "</p>";
        echo "<p><strong>Query:</strong> <code>" . htmlspecialchars($query) . "</code></p>";
        echo "<p><a href='index.php'>Go back</a></p>";
        echo "</div>";
    } else if ($result->num_rows > 0) {
        // Login successful
        $user = $result->fetch_assoc();
        
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
} else {
    header("Location: index.php");
    exit();
}

$conn->close();
?>