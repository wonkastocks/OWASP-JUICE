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
        .message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
        }
        .error {
            background: #fee;
            color: #c00;
            border: 1px solid #fcc;
        }
        .success {
            background: #efe;
            color: #060;
            border: 1px solid #cfc;
        }
        .hint {
            background: #fff3cd;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <?php
        // Check if lab is enabled
        $config_file = '/var/www/html/sql-lab-config.json';
        $lab_enabled = true; // Default to true if config doesn't exist
        
        if (file_exists($config_file)) {
            $config = json_decode(file_get_contents($config_file), true);
            $lab_enabled = $config['lab_enabled'];
        }
        
        if ($lab_enabled): ?>
            <div class="warning">⚠️ EDUCATIONAL LAB - INTENTIONALLY VULNERABLE ⚠️</div>
        <?php else: ?>
            <div style="background: #28a745; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; font-weight: bold;">
                🔒 SECURE MODE - SQL Injection Protection Active
            </div>
        <?php endif; ?>
        <h1>SecureCorp Login</h1>
        
        <form method="POST" action="login.php">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>
            
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>
            
            <input type="submit" value="Login">
        </form>
        
        <?php if ($lab_enabled): ?>
        <div class="hint">
            💡 <strong>Student Hint:</strong> This application is vulnerable to SQL injection. 
            Try different inputs to understand how the backend processes your data.
            Common test: admin' --
        </div>
        <?php else: ?>
        <div style="background: #e3f2fd; color: #1565c0; padding: 10px; border-radius: 5px; margin-top: 20px; font-size: 14px;">
            ℹ️ <strong>Note:</strong> The SQL injection lab is currently disabled. 
            The application is using secure prepared statements. Contact your instructor to enable the vulnerable mode for practice.
        </div>
        <?php endif; ?>
    </div>
</body>
</html>