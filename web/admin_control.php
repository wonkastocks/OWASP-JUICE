<?php
session_start();

// Check if user is admin
if (!isset($_SESSION['is_admin']) || $_SESSION['is_admin'] != 1) {
    header("Location: index.php");
    exit();
}

// Configuration file path
$config_file = '/var/www/html/sql-lab-config.json';

// Handle toggle action
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['toggle_lab'])) {
    $current_state = json_decode(file_get_contents($config_file), true);
    $new_state = !$current_state['lab_enabled'];
    
    $config = [
        'lab_enabled' => $new_state,
        'last_modified' => date('Y-m-d H:i:s'),
        'modified_by' => $_SESSION['username']
    ];
    
    file_put_contents($config_file, json_encode($config, JSON_PRETTY_PRINT));
    $message = $new_state ? "SQL Injection Lab is now ENABLED" : "SQL Injection Lab is now DISABLED";
}

// Get current state
if (!file_exists($config_file)) {
    // Create default config
    $default_config = [
        'lab_enabled' => false,
        'last_modified' => date('Y-m-d H:i:s'),
        'modified_by' => 'system'
    ];
    file_put_contents($config_file, json_encode($default_config, JSON_PRETTY_PRINT));
}

$config = json_decode(file_get_contents($config_file), true);
$lab_enabled = $config['lab_enabled'];
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Control Panel - SQL Injection Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 600px;
            max-width: 100%;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .status-box {
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        .status-enabled {
            background: #d4edda;
            border: 2px solid #28a745;
            color: #155724;
        }
        .status-disabled {
            background: #f8d7da;
            border: 2px solid #dc3545;
            color: #721c24;
        }
        .toggle-switch {
            position: relative;
            width: 120px;
            height: 60px;
            margin: 30px auto;
            display: block;
        }
        .toggle-switch input {
            display: none;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 52px;
            width: 52px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #28a745;
        }
        input:checked + .slider:before {
            transform: translateX(60px);
        }
        .toggle-text {
            text-align: center;
            margin: 20px 0;
            font-size: 24px;
            font-weight: bold;
        }
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .info-box {
            background: #e7f3ff;
            border: 1px solid #2196F3;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            display: block;
            margin: 20px auto;
        }
        .button:hover {
            background: #5a67d8;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .back-link:hover {
            background: #5a6268;
        }
        .message {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: center;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        .status-indicator.active {
            background: #28a745;
        }
        .status-indicator.inactive {
            background: #dc3545;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ SQL Injection Lab Control Panel</h1>
        
        <?php if (isset($message)): ?>
        <div class="message">
            <?php echo $message; ?>
        </div>
        <?php endif; ?>
        
        <div class="status-box <?php echo $lab_enabled ? 'status-enabled' : 'status-disabled'; ?>">
            <h2>
                <span class="status-indicator <?php echo $lab_enabled ? 'active' : 'inactive'; ?>"></span>
                Lab Status: <?php echo $lab_enabled ? 'ENABLED' : 'DISABLED'; ?>
            </h2>
            <p>Last modified: <?php echo $config['last_modified']; ?> by <?php echo $config['modified_by']; ?></p>
        </div>
        
        <form method="POST" action="">
            <label class="toggle-switch">
                <input type="checkbox" name="lab_state" <?php echo $lab_enabled ? 'checked' : ''; ?> onchange="this.form.submit()">
                <span class="slider"></span>
                <input type="hidden" name="toggle_lab" value="1">
            </label>
        </form>
        
        <div class="toggle-text">
            <?php if ($lab_enabled): ?>
                🟢 Lab is Active
            <?php else: ?>
                🔴 Lab is Inactive
            <?php endif; ?>
        </div>
        
        <div class="warning">
            <strong>⚠️ Security Warning:</strong><br>
            When enabled, the SQL injection lab makes your site intentionally vulnerable for educational purposes. 
            Only enable this in a controlled environment with proper network isolation.
        </div>
        
        <div class="info-box">
            <strong>ℹ️ Information:</strong><br>
            • When disabled, the vulnerable login system will not accept any SQL injection attempts<br>
            • Regular authentication will still work with valid credentials<br>
            • The dashboard and other features remain accessible to logged-in users<br>
            • Student progress and data are preserved when toggling the lab state
        </div>
        
        <div style="text-align: center;">
            <a href="dashboard.php" class="back-link">← Back to Dashboard</a>
        </div>
    </div>
</body>
</html>