<?php
session_start();

// Database connection settings
$host = 'localhost';
$dbname = 'vulnerable_db';
$username = 'web_user';
$password = 'web_pass123';

// Handle login form submission
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $email = $_POST['email'] ?? '';
    $pass = $_POST['password'] ?? '';
    
    // Connect to database
    $conn = mysqli_connect($host, $username, $password, $dbname);
    
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }
    
    // VULNERABLE QUERY (for educational purposes)
    $query = "SELECT * FROM users WHERE email = '$email' AND password = '$pass'";
    
    $result = mysqli_query($conn, $query);
    
    if ($result && mysqli_num_rows($result) > 0) {
        $user = mysqli_fetch_assoc($result);
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'] ?? $user['email'];
        $_SESSION['is_admin'] = $user['is_admin'] ?? false;
        header("Location: dashboard.php");
        exit();
    } else {
        $error = "Invalid credentials";
    }
    
    mysqli_close($conn);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Wonkatech</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        .login-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            width: 400px;
            max-width: 90%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
            font-weight: 600;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        input[type="email"],
        input[type="password"],
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input[type="email"]:focus,
        input[type="password"]:focus,
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: #ff7043;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        button:hover {
            background: #ff5722;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255, 87, 34, 0.3);
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            border: 1px solid #ef5350;
        }
        
        .logo {
            text-align: center;
            margin-bottom: 20px;
            font-size: 40px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🔐</div>
        <h1>Sign In</h1>
        
        <?php if (isset($error)): ?>
            <div class="error"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        
        <form method="POST" action="">
            <div class="form-group">
                <input type="email" name="email" placeholder="Email" required>
            </div>
            
            <div class="form-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>