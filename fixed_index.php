<!DOCTYPE html>
<html>
<head>
    <title>SecureCorp Login Portal - Educational SQL Injection Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 400px;
        }
        .warning {
            background: #ff6b6b;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        input[type="submit"]:hover {
            background: #5a67d8;
        }
        .error {
            background: #fee;
            color: #c00;
            border: 1px solid #fcc;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">⚠️ EDUCATIONAL LAB - INTENTIONALLY VULNERABLE ⚠️</div>
        <h1>SecureCorp Login</h1>
        
        <?php if (isset($_GET['error'])): ?>
            <div class="error"><?php echo htmlspecialchars($_GET['error']); ?></div>
        <?php endif; ?>
        
        <form method="POST" action="login.php">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
            
            <input type="submit" value="Login">
        </form>
    </div>
</body>
</html>