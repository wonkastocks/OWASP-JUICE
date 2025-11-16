<?php
session_start();

// Check if user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

// Database connection for additional queries
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
?>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - SecureCorp</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 {
            color: #333;
            margin: 0;
        }
        .user-info {
            background: #f0f0f0;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .admin-panel {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .data-section {
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
        }
        tr:hover {
            background: #f5f5f5;
        }
        .logout-btn {
            background: #dc3545;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
        }
        .secret-data {
            background: #e8f5e9;
            border: 2px solid #4caf50;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .code {
            background: #f4f4f4;
            padding: 10px;
            border-left: 4px solid #667eea;
            font-family: monospace;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SecureCorp Dashboard</h1>
            <div class="user-info">
                Logged in as: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong>
                <?php if ($_SESSION['is_admin'] == 1): ?>
                    <span style="color: red; font-weight: bold;"> [ADMIN]</span>
                <?php endif; ?>
            </div>
        </div>

        <div class="success-box">
            <h2>🎉 Congratulations!</h2>
            <p>You successfully logged into the system! This demonstrates a successful SQL injection attack.</p>
            <p><strong>Your session details:</strong></p>
            <ul>
                <li>Username: <?php echo htmlspecialchars($_SESSION['username']); ?></li>
                <li>User ID: <?php echo $_SESSION['user_id']; ?></li>
                <li>Admin Status: <?php echo $_SESSION['is_admin'] ? 'Yes' : 'No'; ?></li>
            </ul>
        </div>

        <?php if ($_SESSION['is_admin'] == 1): ?>
        <div class="admin-panel">
            <h2>🔐 Admin Panel - System Credentials</h2>
            <div style="text-align: right; margin-bottom: 20px;">
                <a href="admin_control.php" style="background: #ff6b6b; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    ⚙️ Lab Control Panel
                </a>
            </div>
            <p>As an admin, you have access to sensitive system information:</p>
            
            <div class="secret-data">
                <h3>Database Credentials:</h3>
                <div class="code">
                    Host: localhost<br>
                    Database: vulnerable_db<br>
                    Root User: root<br>
                    Root Password: rootpass123!<br>
                </div>
                
                <h3>System SSH Credentials:</h3>
                <div class="code">
                    SSH User: sysadmin<br>
                    SSH Password: Sysadmin123!@#<br>
                    SSH Port: 22<br>
                </div>
                
                <h3>Additional Services:</h3>
                <div class="code">
                    MySQL Port: 3306<br>
                    Apache Config: /etc/apache2/sites-available/vulnerable-site.conf<br>
                    Web Root: /var/www/vulnerable-site<br>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <div class="data-section">
            <h2>User Directory</h2>
            <?php
            // Fetch all users (another potentially vulnerable query for students to explore)
            $search = isset($_GET['search']) ? $_GET['search'] : '';
            if ($search) {
                // Another vulnerable query for students to practice
                $query = "SELECT id, username, email, is_admin FROM users WHERE username LIKE '%$search%'";
            } else {
                $query = "SELECT id, username, email, is_admin FROM users";
            }
            
            $result = $conn->query($query);
            ?>
            
            <form method="GET" action="">
                <input type="text" name="search" placeholder="Search users..." value="<?php echo htmlspecialchars($search); ?>">
                <input type="submit" value="Search">
            </form>
            
            <table>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                </tr>
                <?php while ($row = $result->fetch(PDO::FETCH_ASSOC)): ?>
                <tr>
                    <td><?php echo $row['id']; ?></td>
                    <td><?php echo htmlspecialchars($row['username']); ?></td>
                    <td><?php echo htmlspecialchars($row['email']); ?></td>
                    <td><?php echo $row['is_admin'] ? 'Admin' : 'User'; ?></td>
                </tr>
                <?php endwhile; ?>
            </table>
        </div>

        <div style="margin-top: 30px;">
            <a href="logout.php" class="logout-btn">Logout</a>
        </div>
    </div>
</body>
</html>