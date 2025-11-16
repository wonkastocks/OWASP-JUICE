<?php
session_start();

// Check if user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: wallys_login.php");
    exit();
}

// Database connection
$host = 'localhost';
$dbname = 'wallys_monkey_parts';
$db_user = 'wallys_web';
$db_pass = 'MonkeyWeb123!';

try {
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $db_user, $db_pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

// Check if SQL injection lab is enabled
$config_file = '/var/www/html/sql-lab-config.json';
$lab_enabled = true;

if (file_exists($config_file)) {
    $config = json_decode(file_get_contents($config_file), true);
    $lab_enabled = $config['lab_enabled'] ?? true;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Wally's Monkey Parts - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #8B4513, #A0522D);
            color: white;
            padding: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
        }
        .user-info {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 8px;
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .welcome-box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .admin-panel {
            background: #fff8e1;
            border: 2px solid #ffc107;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .admin-panel h2 {
            color: #f57c00;
            margin-bottom: 20px;
        }
        .credentials-box {
            background: #ffebcd;
            border: 2px solid #D2691E;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .credentials-box h3 {
            color: #8B4513;
            margin-bottom: 15px;
        }
        .code-block {
            background: #263238;
            color: #aed581;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
            overflow-x: auto;
        }
        .search-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .search-form {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .search-input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .search-btn {
            padding: 12px 30px;
            background: #8B4513;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background: #8B4513;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background: #f9f9f9;
        }
        .sql-hint {
            background: #e3f2fd;
            border: 1px solid #2196F3;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .logout-btn {
            background: #dc3545;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 8px;
            display: inline-block;
            margin-top: 20px;
        }
        .flag-box {
            background: linear-gradient(135deg, #4caf50, #8bc34a);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            margin: 20px 0;
            font-weight: bold;
        }
        .hash-display {
            background: #fff3e0;
            border: 2px solid #ff9800;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .hash-display h3 {
            color: #e65100;
            margin-bottom: 15px;
        }
        .hash-table {
            width: 100%;
            margin-top: 10px;
        }
        .hash-table td {
            font-family: 'Courier New', monospace;
            background: #263238;
            color: #aed581;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                🐵 Wally's Monkey Parts
            </div>
            <div class="user-info">
                Logged in as: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong>
                <?php if ($_SESSION['is_admin']): ?>
                    <span style="color: #ffeb3b;"> [ADMIN]</span>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="welcome-box">
            <h1>Welcome, <?php echo htmlspecialchars($_SESSION['full_name']); ?>!</h1>
            <p>You have successfully logged into Wally's Monkey Parts inventory system.</p>
            <p><strong>Your Details:</strong></p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>Username: <?php echo htmlspecialchars($_SESSION['username']); ?></li>
                <li>Email: <?php echo htmlspecialchars($_SESSION['email']); ?></li>
                <li>Role: <?php echo htmlspecialchars($_SESSION['role']); ?></li>
                <li>SSH Access: <?php echo $_SESSION['ssh_access'] ? 'Enabled' : 'Disabled'; ?></li>
            </ul>
        </div>

        <?php if ($_SESSION['is_admin']): ?>
        <div class="admin-panel">
            <h2>🔐 Admin Panel - System Access</h2>
            
            <div class="credentials-box">
                <h3>Database Credentials:</h3>
                <div class="code-block">
Host: localhost
Database: wallys_monkey_parts
Admin User: wallys_web
Admin Password: MonkeyWeb123!
Root Password: MySQLRoot123!
                </div>
            </div>

            <div class="credentials-box">
                <h3>SSH Access Information:</h3>
                <div class="code-block">
SSH Host: 155.138.197.128
SSH Port: 22
SSH User: root
SSH Password: MonkeyRoot2024!
Alternative: wally / WallyParts2024!
                </div>
            </div>

            <div class="hash-display">
                <h3>🔓 User Password Hashes (MD5):</h3>
                <p>These MD5 hashes can be cracked using online tools:</p>
                <?php
                // Fetch all user hashes for admin
                $hash_query = "SELECT username, password, role FROM users";
                $hash_result = $conn->query($hash_query);
                ?>
                <table class="hash-table">
                    <tr>
                        <th style="background: #e65100;">Username</th>
                        <th style="background: #e65100;">MD5 Hash</th>
                        <th style="background: #e65100;">Role</th>
                    </tr>
                    <?php while ($hash_row = $hash_result->fetch(PDO::FETCH_ASSOC)): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($hash_row['username']); ?></td>
                        <td><?php echo htmlspecialchars($hash_row['password']); ?></td>
                        <td><?php echo htmlspecialchars($hash_row['role']); ?></td>
                    </tr>
                    <?php endwhile; ?>
                </table>
            </div>

            <div class="flag-box">
                🚩 FLAG{W4llys_M0nk3y_SQL_Inj3ct10n} 🚩
            </div>
        </div>
        <?php endif; ?>

        <div class="search-section">
            <h2>🔍 Search Monkey Parts Inventory</h2>
            
            <?php if ($lab_enabled): ?>
            <div class="sql-hint">
                <strong>💡 SQL Injection Practice:</strong><br>
                This search is vulnerable to UNION attacks. Try:<br>
                • <code>' UNION SELECT 1,2,3,4,5,6,7 --</code><br>
                • <code>' UNION SELECT id,username,password,email,role,null,null FROM users --</code><br>
                • <code>' UNION SELECT 1,data_type,data_value,'SECRET',null,null,null FROM sensitive_data --</code>
            </div>
            <?php endif; ?>
            
            <?php
            $search = $_GET['search'] ?? '';
            $search_error = false;
            
            if ($search) {
                if ($lab_enabled) {
                    // VULNERABLE: Direct concatenation allows UNION attacks
                    $query = "SELECT * FROM products WHERE product_name LIKE '%$search%' OR description LIKE '%$search%'";
                    
                    echo "<!-- DEBUG: Search Query = $query -->\n";
                } else {
                    // SECURE: Using prepared statements
                    $query = "SELECT * FROM products WHERE product_name LIKE :search OR description LIKE :search";
                }
                
                try {
                    if ($lab_enabled) {
                        $result = $conn->query($query);
                    } else {
                        $stmt = $conn->prepare($query);
                        $search_param = "%$search%";
                        $stmt->bindParam(':search', $search_param);
                        $stmt->execute();
                        $result = $stmt;
                    }
                } catch(PDOException $e) {
                    $search_error = true;
                    $error_msg = $e->getMessage();
                }
            } else {
                // Default: show all products
                $query = "SELECT * FROM products";
                $result = $conn->query($query);
            }
            ?>
            
            <form method="GET" action="" class="search-form">
                <input type="text" name="search" class="search-input" 
                       placeholder="Search for monkey parts..." 
                       value="<?php echo htmlspecialchars($search); ?>">
                <button type="submit" class="search-btn">Search</button>
            </form>
            
            <?php if ($search_error && $lab_enabled): ?>
            <div style="background: #fee; border: 2px solid #f44336; color: #c62828; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <strong>SQL Error:</strong> <?php echo htmlspecialchars($error_msg); ?><br>
                <strong>Query:</strong> <code><?php echo htmlspecialchars($query); ?></code>
            </div>
            <?php endif; ?>
            
            <?php if (!$search_error && isset($result)): ?>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Part Number</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Stock</th>
                    <th>Category</th>
                </tr>
                <?php while ($row = $result->fetch(PDO::FETCH_ASSOC)): ?>
                <tr>
                    <td><?php echo htmlspecialchars($row['id'] ?? ''); ?></td>
                    <td><?php echo htmlspecialchars($row['product_name'] ?? ''); ?></td>
                    <td><?php echo htmlspecialchars($row['part_number'] ?? ''); ?></td>
                    <td><?php echo htmlspecialchars($row['description'] ?? ''); ?></td>
                    <td>$<?php echo htmlspecialchars($row['price'] ?? ''); ?></td>
                    <td><?php echo htmlspecialchars($row['stock_quantity'] ?? ''); ?></td>
                    <td><?php echo htmlspecialchars($row['category'] ?? ''); ?></td>
                </tr>
                <?php endwhile; ?>
            </table>
            <?php endif; ?>
        </div>

        <a href="wallys_logout.php" class="logout-btn">Logout</a>
    </div>
</body>
</html>