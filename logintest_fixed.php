<?php
// Disable error reporting to prevent SQL errors from showing
error_reporting(0);
ini_set('display_errors', 0);
mysqli_report(MYSQLI_REPORT_OFF);

session_start();

// Database connection
$conn = @new mysqli('localhost', 'root', '', 'wallys_monkey_parts');

if ($conn->connect_error) {
    die('Database connection failed');
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $user = $_POST['username'] ?? '';
    $pass = $_POST['password'] ?? '';
    
    // Vulnerable query - intentional for SQL injection demo
    $sql = "SELECT * FROM users WHERE username = '$user' AND password = MD5('$pass')";
    
    // Suppress ALL errors including exceptions
    try {
        $result = @$conn->query($sql);
        
        if ($result && $result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $message = '<span style="color:green">SUCCESS: Logged in as ' . htmlspecialchars($row['username']) . ' (Admin: ' . ($row['is_admin'] ? 'YES' : 'NO') . ')</span>';
        } else {
            $message = '<span style="color:red">Login failed</span>';
        }
    } catch (Exception $e) {
        // Catch any exceptions and show generic error
        $message = '<span style="color:red">Login failed</span>';
    } catch (mysqli_sql_exception $e) {
        // Catch SQL exceptions specifically
        $message = '<span style="color:red">Login failed</span>';
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login Test</title>
    <style>
        body { 
            font-family: Arial; 
            background: #eee; 
            padding: 50px; 
            margin: 0;
        }
        .box { 
            background: white; 
            max-width: 400px; 
            margin: 0 auto; 
            padding: 30px; 
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
            color: #333;
        }
        input { 
            width: 100%; 
            padding: 10px; 
            margin: 10px 0; 
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        button { 
            width: 100%; 
            padding: 10px; 
            background: #4CAF50; 
            color: white; 
            border: none; 
            cursor: pointer;
            border-radius: 3px;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .message { 
            padding: 10px; 
            margin: 10px 0; 
            background: #f0f0f0;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class='box'>
        <h2>Login</h2>
        <?php if ($message): ?>
            <div class='message'><?= $message ?></div>
        <?php endif; ?>
        <form method='POST'>
            <input type='text' name='username' placeholder='Username' required>
            <input type='password' name='password' placeholder='Password'>
            <button type='submit'>Login</button>
        </form>
    </div>
</body>
</html>