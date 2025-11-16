<?php
session_start();

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    header("Location: logintest.php");
    exit();
}

// Database connection
$conn = new mysqli('localhost', 'root', '', 'wallys_monkey_parts');

// Get user information
$user_id = $_SESSION['user_id'];
$username = $_SESSION['username'];
$is_admin = $_SESSION['is_admin'];

// Get full user details
$user_query = "SELECT * FROM users WHERE id = $user_id";
$user_result = $conn->query($user_query);
$user = $user_result->fetch_assoc();

// Get user's orders (create orders table if needed)
$orders_query = "SELECT * FROM orders WHERE user_id = $user_id ORDER BY order_date DESC LIMIT 10";
$orders_result = @$conn->query($orders_query);

// Get some products for display
$products_query = "SELECT * FROM products LIMIT 6";
$products_result = @$conn->query($products_query);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Wally's Monkey Parts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            font-size: 24px;
            font-weight: bold;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .admin-badge {
            background: #ff6b6b;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .logout-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .logout-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .welcome-section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .welcome-section h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .account-info {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .info-item {
            display: flex;
            flex-direction: column;
        }
        .info-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 16px;
            color: #333;
            font-weight: 500;
        }
        .section {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .section h2 {
            margin-bottom: 20px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .orders-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .orders-table th {
            background: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #666;
            border-bottom: 2px solid #ddd;
        }
        .orders-table td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        .orders-table tr:hover {
            background: #f9f9f9;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .status-completed {
            background: #d4edda;
            color: #155724;
        }
        .status-pending {
            background: #fff3cd;
            color: #856404;
        }
        .status-shipped {
            background: #cce5ff;
            color: #004085;
        }
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .product-card {
            background: #f9f9f9;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            transition: transform 0.3s;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .product-price {
            color: #667eea;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .quick-links {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        .quick-link {
            flex: 1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
            transition: transform 0.3s;
        }
        .quick-link:hover {
            transform: translateY(-3px);
        }
        .no-data {
            text-align: center;
            color: #999;
            padding: 40px;
            background: #f9f9f9;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">🐵 Wally's Monkey Parts</div>
            <div class="user-info">
                <span>Welcome, <?php echo htmlspecialchars($username); ?></span>
                <?php if ($is_admin): ?>
                    <span class="admin-badge">ADMIN</span>
                <?php endif; ?>
                <a href="logout.php" class="logout-btn">Logout</a>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="welcome-section">
            <h1>Welcome back, <?php echo htmlspecialchars($user['full_name'] ?? $username); ?>!</h1>
            <p>Manage your account, view orders, and explore our latest monkey parts.</p>
            
            <div class="account-info">
                <h3>Account Information</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">Username</span>
                        <span class="info-value"><?php echo htmlspecialchars($username); ?></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Email</span>
                        <span class="info-value"><?php echo htmlspecialchars($user['email']); ?></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Full Name</span>
                        <span class="info-value"><?php echo htmlspecialchars($user['full_name'] ?? 'Not provided'); ?></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Member Since</span>
                        <span class="info-value"><?php echo date('F j, Y', strtotime($user['created_at'] ?? '2024-01-01')); ?></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Account Type</span>
                        <span class="info-value"><?php echo $is_admin ? 'Administrator' : 'Customer'; ?></span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Phone</span>
                        <span class="info-value"><?php echo htmlspecialchars($user['phone'] ?? 'Not provided'); ?></span>
                    </div>
                </div>
            </div>
        </div>

        <?php if ($is_admin): ?>
        <div class="section">
            <h2>🔧 Admin Panel</h2>
            <div class="quick-links">
                <a href="admin/users.php" class="quick-link">Manage Users</a>
                <a href="admin/products.php" class="quick-link">Manage Products</a>
                <a href="admin/orders.php" class="quick-link">View All Orders</a>
                <a href="admin/reports.php" class="quick-link">Sales Reports</a>
            </div>
        </div>
        <?php endif; ?>

        <div class="section">
            <h2>📦 Recent Orders</h2>
            <?php if ($orders_result && $orders_result->num_rows > 0): ?>
                <table class="orders-table">
                    <thead>
                        <tr>
                            <th>Order #</th>
                            <th>Date</th>
                            <th>Items</th>
                            <th>Total</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while($order = $orders_result->fetch_assoc()): ?>
                        <tr>
                            <td>#<?php echo $order['id']; ?></td>
                            <td><?php echo date('M j, Y', strtotime($order['order_date'])); ?></td>
                            <td><?php echo $order['item_count'] ?? rand(1, 5); ?> items</td>
                            <td>$<?php echo number_format($order['total'] ?? rand(50, 500), 2); ?></td>
                            <td>
                                <?php 
                                $statuses = ['completed', 'shipped', 'pending'];
                                $status = $order['status'] ?? $statuses[array_rand($statuses)];
                                ?>
                                <span class="status-badge status-<?php echo $status; ?>">
                                    <?php echo ucfirst($status); ?>
                                </span>
                            </td>
                        </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <div class="no-data">
                    <p>No orders yet. Start shopping to see your order history!</p>
                </div>
            <?php endif; ?>
        </div>

        <div class="section">
            <h2>🛍️ Featured Products</h2>
            <div class="products-grid">
                <?php 
                $mock_products = [
                    ['name' => 'Rubber Chicken', 'price' => 12.99],
                    ['name' => 'Whoopee Cushion Pro', 'price' => 8.99],
                    ['name' => 'Fake Dog Poop', 'price' => 6.99],
                    ['name' => 'Joy Buzzer 2000', 'price' => 15.99],
                    ['name' => 'Invisible Ink Pen', 'price' => 9.99],
                    ['name' => 'Squirting Flower', 'price' => 11.99]
                ];
                
                foreach ($mock_products as $product): ?>
                <div class="product-card">
                    <h4><?php echo $product['name']; ?></h4>
                    <div class="product-price">$<?php echo $product['price']; ?></div>
                    <button style="background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Add to Cart</button>
                </div>
                <?php endforeach; ?>
            </div>
        </div>

        <div class="section">
            <h2>🔗 Quick Links</h2>
            <div class="quick-links">
                <a href="profile.php" class="quick-link">Edit Profile</a>
                <a href="orders.php" class="quick-link">Order History</a>
                <a href="wishlist.php" class="quick-link">Wishlist</a>
                <a href="support.php" class="quick-link">Support</a>
            </div>
        </div>
    </div>
</body>
</html>