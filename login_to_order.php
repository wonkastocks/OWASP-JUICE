<?php
// Disable error reporting to prevent SQL errors from showing
error_reporting(0);
ini_set('display_errors', 0);
mysqli_report(MYSQLI_REPORT_OFF);

session_start();

// If already logged in, redirect to order page
if (isset($_SESSION['user_id'])) {
    header("Location: order.php");
    exit();
}

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
            
            // Set session variables
            $_SESSION['user_id'] = $row['id'];
            $_SESSION['username'] = $row['username'];
            $_SESSION['is_admin'] = $row['is_admin'];
            
            // Redirect to order page (not dashboard)
            header("Location: order.php");
            exit();
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
    <title>Login - Wally's Monkey Parts</title>
    <style>
        body { 
            font-family: Arial; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 50px; 
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .box { 
            background: white; 
            max-width: 400px; 
            width: 100%;
            padding: 40px; 
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .logo {
            text-align: center;
            font-size: 32px;
            margin-bottom: 10px;
        }
        h2 {
            margin-top: 0;
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        input { 
            width: 100%; 
            padding: 12px; 
            margin: 10px 0; 
            box-sizing: border-box;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
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
            cursor: pointer;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
            margin-top: 10px;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .message { 
            padding: 10px; 
            margin: 10px 0; 
            background: #f0f0f0;
            border-radius: 5px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
    </style>
</head>
<body>
    <div class='box'>
        <div class="logo">🐵</div>
        <h2>Wally's Monkey Parts</h2>
        <p class="subtitle">Sign in to place your order</p>
        <?php if ($message): ?>
            <div class='message'><?= $message ?></div>
        <?php endif; ?>
        <form method='POST'>
            <input type='text' name='username' placeholder='Username' required>
            <input type='password' name='password' placeholder='Password'>
            <button type='submit'>Sign In</button>
        </form>
    </div>
</body>
</html>