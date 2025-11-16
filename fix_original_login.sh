#!/bin/bash

# Fix script for the original vulnerable login.php
# This fixes the SQL error while keeping the vulnerability for educational purposes

cat > /tmp/fixed_login.php << 'EOF'
<?php
// EDUCATIONAL PURPOSE ONLY - INTENTIONALLY VULNERABLE CODE
// DO NOT USE IN PRODUCTION

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
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    // VULNERABLE CODE - Direct SQL concatenation (DO NOT USE IN PRODUCTION)
    // This is intentionally vulnerable for educational purposes
    // Fixed the query to handle special characters properly
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    
    // Debug mode - shows the actual query being executed (educational purposes)
    echo "<!-- DEBUG: SQL Query = $query -->\n";
    
    try {
        $stmt = $conn->prepare($query);
        $stmt->execute();
        $result = $stmt;
        
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
} else {
    header("Location: index.php");
}
?>
EOF

echo "Deploying fixed login.php to server..."
scp /tmp/fixed_login.php root@155.138.197.128:/var/www/html/login.php && \
ssh root@155.138.197.128 "chown www-data:www-data /var/www/html/login.php && chmod 644 /var/www/html/login.php && systemctl restart apache2"

echo "Fix complete!"