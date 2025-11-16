<?php
session_start();

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit();
}

// Database connection
$conn = new mysqli('localhost', 'root', '', 'wallys_monkey_parts');

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch user details
$user_id = $_SESSION['user_id'];
$sql = "SELECT * FROM users WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
$user = $result->fetch_assoc();

// Fetch user orders (simulated)
$orders = [
    ['id' => 'ORD-2025-001', 'date' => '2025-08-15', 'status' => 'Delivered', 'total' => 299.99],
    ['id' => 'ORD-2025-002', 'date' => '2025-08-20', 'status' => 'Shipped', 'total' => 149.99],
    ['id' => 'ORD-2025-003', 'date' => '2025-08-28', 'status' => 'Processing', 'total' => 89.99]
];
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Account - Wally's Monkey Parts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f8f9fa;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
            color: white;
            cursor: pointer;
        }

        .logo-icon {
            font-size: 40px;
        }

        .logo h1 {
            font-size: 24px;
            font-weight: bold;
        }

        nav {
            display: flex;
            gap: 30px;
            align-items: center;
        }

        nav a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: opacity 0.3s;
        }

        nav a:hover {
            opacity: 0.8;
        }

        .user-menu {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .cart-icon {
            color: white;
            font-size: 24px;
            position: relative;
            cursor: pointer;
        }

        .cart-count {
            position: absolute;
            top: -8px;
            right: -8px;
            background: #ff4444;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }

        .logout-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            text-decoration: none;
            transition: background 0.3s;
        }

        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
        }

        .breadcrumb {
            padding: 20px 40px;
            color: #666;
            font-size: 14px;
        }

        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 40px;
        }

        .account-header {
            margin-bottom: 40px;
        }

        .account-header h1 {
            font-size: 36px;
            color: #333;
            margin-bottom: 10px;
        }

        .account-header p {
            color: #666;
            font-size: 18px;
        }

        .account-grid {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 40px;
            margin-bottom: 60px;
        }

        .sidebar {
            background: white;
            border-radius: 10px;
            padding: 20px;
            height: fit-content;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .sidebar-menu {
            list-style: none;
        }

        .sidebar-menu li {
            margin-bottom: 5px;
        }

        .sidebar-menu a {
            display: block;
            padding: 12px 15px;
            color: #333;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }

        .sidebar-menu a:hover,
        .sidebar-menu a.active {
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            color: #667eea;
        }

        .content-area {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .section {
            margin-bottom: 40px;
        }

        .section h2 {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .info-item {
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .info-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }

        .info-value {
            font-size: 16px;
            color: #333;
            font-weight: 500;
        }

        .orders-table {
            width: 100%;
            border-collapse: collapse;
        }

        .orders-table th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #666;
        }

        .orders-table td {
            padding: 15px 12px;
            border-bottom: 1px solid #f0f0f0;
        }

        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }

        .status-delivered {
            background: #d4edda;
            color: #155724;
        }

        .status-shipped {
            background: #cce5ff;
            color: #004085;
        }

        .status-processing {
            background: #fff3cd;
            color: #856404;
        }

        .view-order {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }

        .edit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }

        .edit-btn:hover {
            transform: scale(1.05);
        }

        .back-to-shop {
            display: inline-block;
            margin-top: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.3s;
        }

        .back-to-shop:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <header>
        <div class="logo" onclick="window.location.href='/'">
            <span class="logo-icon">🐵</span>
            <h1>Wally's Monkey Parts</h1>
        </div>
        <nav>
            <a href="/">Home</a>
            <a href="/shop.php">Shop</a>
            <a href="/about.php">About</a>
            <a href="/contact.php">Contact</a>
            <div class="user-menu">
                <div class="cart-icon">
                    🛒
                    <span class="cart-count">3</span>
                </div>
                <a href="/logout.php" class="logout-btn">Sign Out</a>
            </div>
        </nav>
    </header>

    <div class="breadcrumb">
        <a href="/">Home</a> / My Account
    </div>

    <div class="container">
        <div class="account-header">
            <h1>My Account</h1>
            <p>Welcome back, <?php echo htmlspecialchars($user['full_name'] ?: $user['username']); ?>!</p>
        </div>

        <div class="account-grid">
            <aside class="sidebar">
                <ul class="sidebar-menu">
                    <li><a href="#profile" class="active">Profile Information</a></li>
                    <li><a href="#orders">Order History</a></li>
                    <li><a href="#addresses">Addresses</a></li>
                    <li><a href="#payment">Payment Methods</a></li>
                    <li><a href="#preferences">Preferences</a></li>
                    <?php if ($user['is_admin']): ?>
                    <li><a href="/admin.php" style="color: #667eea;">Admin Panel</a></li>
                    <?php endif; ?>
                </ul>
            </aside>

            <main class="content-area">
                <section class="section" id="profile">
                    <h2>Profile Information</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Full Name</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['full_name'] ?: 'Not set'); ?></div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Email</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['email'] ?: $user['username'] . '@example.com'); ?></div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Phone</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['phone'] ?: 'Not set'); ?></div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Member Since</div>
                            <div class="info-value"><?php echo date('F Y', strtotime($user['created_at'] ?: '2025-01-01')); ?></div>
                        </div>
                    </div>
                    <button class="edit-btn" style="margin-top: 20px;">Edit Profile</button>
                </section>

                <section class="section" id="addresses">
                    <h2>Shipping Address</h2>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">Street Address</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['address'] ?: 'Not set'); ?></div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">City</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['city'] ?: 'Not set'); ?></div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">State</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['state'] ?: 'Not set'); ?></div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">ZIP Code</div>
                            <div class="info-value"><?php echo htmlspecialchars($user['zip'] ?: 'Not set'); ?></div>
                        </div>
                    </div>
                    <button class="edit-btn" style="margin-top: 20px;">Edit Address</button>
                </section>

                <section class="section" id="orders">
                    <h2>Recent Orders</h2>
                    <table class="orders-table">
                        <thead>
                            <tr>
                                <th>Order ID</th>
                                <th>Date</th>
                                <th>Status</th>
                                <th>Total</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($orders as $order): ?>
                            <tr>
                                <td><?php echo $order['id']; ?></td>
                                <td><?php echo date('M d, Y', strtotime($order['date'])); ?></td>
                                <td>
                                    <span class="status-badge status-<?php echo strtolower($order['status']); ?>">
                                        <?php echo $order['status']; ?>
                                    </span>
                                </td>
                                <td>$<?php echo number_format($order['total'], 2); ?></td>
                                <td><a href="#" class="view-order">View Details</a></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </section>

                <a href="/" class="back-to-shop">Continue Shopping</a>
            </main>
        </div>
    </div>
</body>
</html>