<?php
// EDUCATIONAL PURPOSE ONLY - INTENTIONALLY VULNERABLE CODE
// DO NOT USE IN PRODUCTION

session_start();

// Database connection
$host = 'localhost';
$dbname = 'vulnerable_db';
$db_user = 'web_user';
$db_pass = 'web_pass123';

// Create connection using mysqli
$conn = mysqli_connect($host, $db_user, $db_pass, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = isset($_POST['username']) ? $_POST['username'] : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';
    
    // VULNERABLE CODE - Direct SQL concatenation (DO NOT USE IN PRODUCTION)
    // This is intentionally vulnerable for educational purposes
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    
    // Debug mode - shows the actual query being executed (educational purposes)
    if (isset($_GET['debug'])) {
        echo "<!-- DEBUG: SQL Query = $query -->\n";
    }
    
    // Execute query - suppress errors to handle them properly
    $result = @mysqli_query($conn, $query);
    
    if (!$result) {
        // SQL error occurred - show it for educational purposes
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
                
                <div class='query-box'>
                    <h3>Error Message:</h3>
                    <p>" . htmlspecialchars(mysqli_error($conn)) . "</p>
                    <h3>Executed Query:</h3>
                    <code>" . htmlspecialchars($query) . "</code>
                </div>
                
                <a href='index.php' class='back-link'>← Back to Login</a>
            </div>
        </body>
        </html>";
        exit();
    }
    
    if (mysqli_num_rows($result) > 0) {
        // Login successful
        $user = mysqli_fetch_assoc($result);
        
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
}

mysqli_close($conn);
header("Location: index.php");
exit();
?>