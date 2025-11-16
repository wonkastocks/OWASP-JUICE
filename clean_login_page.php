<!-- This would be the clean login page for Wally's site -->
<!-- Remove the yellow hint box completely -->
<?php
// Check if there's an existing login page showing hints
// This script will help identify and remove them
?>
<!DOCTYPE html>
<html>
<head>
    <title>Wally's Monkey Parts - Login</title>
    <style>
        /* Clean login page without any hints */
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 400px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        input[type="email"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #ff7f50;
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #ff6347;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Wally's Monkey Parts</h1>
        <form method="POST" action="login_process.php">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>