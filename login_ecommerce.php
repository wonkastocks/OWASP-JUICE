<?php
// Disable error reporting to prevent SQL errors from showing
error_reporting(0);
ini_set('display_errors', 0);
mysqli_report(MYSQLI_REPORT_OFF);

session_start();

// Store where user came from (for redirect after login)
if (!isset($_SESSION['redirect_after_login']) && isset($_SERVER['HTTP_REFERER'])) {
    $_SESSION['redirect_after_login'] = $_SERVER['HTTP_REFERER'];
}

// If already logged in, redirect to homepage or dashboard
if (isset($_SESSION['user_id'])) {
    $redirect = $_SESSION['redirect_after_login'] ?? '/';
    unset($_SESSION['redirect_after_login']);
    header("Location: $redirect");
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
            
            // Redirect to where they came from or homepage
            $redirect = $_SESSION['redirect_after_login'] ?? '/';
            unset($_SESSION['redirect_after_login']);
            header("Location: $redirect");
            exit();
        } else {
            $message = '<span style="color:#ff4444">Invalid username or password</span>';
        }
    } catch (Exception $e) {
        $message = '<span style="color:#ff4444">Invalid username or password</span>';
    } catch (mysqli_sql_exception $e) {
        $message = '<span style="color:#ff4444">Invalid username or password</span>';
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Sign In - Wally's Monkey Parts</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .back-home {
            position: absolute;
            top: 30px;
            left: 30px;
            color: white;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
            opacity: 0.9;
            transition: opacity 0.3s;
        }
        
        .back-home:hover {
            opacity: 1;
        }
        
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            max-width: 450px;
            padding: 20px;
        }
        
        .brand-header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .brand-logo {
            font-size: 60px;
            margin-bottom: 10px;
        }
        
        .brand-name {
            font-size: 28px;
            font-weight: bold;
            margin: 0;
        }
        
        .brand-tagline {
            font-size: 16px;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .login-box { 
            background: white; 
            width: 100%;
            padding: 40px; 
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h2 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 24px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            font-size: 14px;
        }
        
        input { 
            width: 100%; 
            padding: 12px 15px; 
            box-sizing: border-box;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        
        .form-options {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .remember-me {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #666;
            font-size: 14px;
        }
        
        .forgot-password {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }
        
        .forgot-password:hover {
            text-decoration: underline;
        }
        
        button { 
            width: 100%; 
            padding: 14px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            border: none; 
            cursor: pointer;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
            margin-top: 10px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102,126,234,0.3);
        }
        
        .message { 
            padding: 12px; 
            margin: 20px 0; 
            background: #fee;
            border: 1px solid #fcc;
            border-radius: 8px;
            text-align: center;
            color: #c00;
        }
        
        .divider {
            text-align: center;
            margin: 30px 0 20px 0;
            position: relative;
        }
        
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #e0e0e0;
        }
        
        .divider span {
            background: white;
            padding: 0 15px;
            color: #999;
            font-size: 14px;
            position: relative;
        }
        
        .signup-prompt {
            text-align: center;
            margin-top: 25px;
            color: #666;
            font-size: 14px;
        }
        
        .signup-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .signup-link:hover {
            text-decoration: underline;
        }
        
        .benefits {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #f0f0f0;
        }
        
        .benefits h3 {
            font-size: 16px;
            color: #333;
            margin-bottom: 15px;
        }
        
        .benefit-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            color: #666;
            font-size: 14px;
        }
        
        .benefit-icon {
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <a href="/" class="back-home">
        ← Back to Shop
    </a>
    
    <div class="login-container">
        <div class="brand-header">
            <div class="brand-logo">🐵</div>
            <h1 class="brand-name">Wally's Monkey Parts</h1>
            <p class="brand-tagline">Premium Auto Parts Since 1985</p>
        </div>
        
        <div class='login-box'>
            <h2>Welcome Back!</h2>
            <p class="subtitle">Sign in to access your account</p>
            
            <?php if ($message): ?>
                <div class='message'><?= $message ?></div>
            <?php endif; ?>
            
            <form method='POST'>
                <div class="form-group">
                    <label for="username">Username or Email</label>
                    <input type='text' id="username" name='username' placeholder='Enter your username' required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type='password' id="password" name='password' placeholder='Enter your password'>
                </div>
                
                <div class="form-options">
                    <label class="remember-me">
                        <input type="checkbox" name="remember"> Remember me
                    </label>
                    <a href="#" class="forgot-password">Forgot password?</a>
                </div>
                
                <button type='submit'>Sign In</button>
            </form>
            
            <div class="divider">
                <span>New to Wally's?</span>
            </div>
            
            <div class="signup-prompt">
                Don't have an account? <a href="/register.php" class="signup-link">Create one now</a>
            </div>
            
            <div class="benefits">
                <h3>Why create an account?</h3>
                <div class="benefit-item">
                    <span class="benefit-icon">✓</span>
                    <span>Track your orders and shipments</span>
                </div>
                <div class="benefit-item">
                    <span class="benefit-icon">✓</span>
                    <span>Save items to your wishlist</span>
                </div>
                <div class="benefit-item">
                    <span class="benefit-icon">✓</span>
                    <span>Get exclusive member discounts</span>
                </div>
                <div class="benefit-item">
                    <span class="benefit-icon">✓</span>
                    <span>Faster checkout with saved addresses</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>