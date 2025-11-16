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

// Parse name for first and last
$full_name = $user['full_name'] ?? $username;
$name_parts = explode(' ', $full_name);
$first_name = $name_parts[0] ?? $username;

// Get user's orders
$orders_query = "SELECT * FROM orders WHERE user_id = $user_id ORDER BY order_date DESC LIMIT 10";
$orders_result = @$conn->query($orders_query);

// Get some products for display
$products_query = "SELECT * FROM products LIMIT 6";
$products_result = @$conn->query($products_query);
?>
<!DOCTYPE html>
<html>
<head>
    <title>My Account - Wally's Monkey Parts</title>
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
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .user-menu {
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
        .welcome-banner {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .welcome-banner h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .welcome-banner p {
            font-size: 18px;
            opacity: 0.95;
        }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        .profile-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .profile-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .profile-avatar {
            width: 100px;
            height: 100px;
            background: white;
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
        }
        .profile-body {
            padding: 25px;
        }
        .profile-info {
            margin-bottom: 20px;
        }
        .profile-info h3 {
            color: #667eea;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f5f5f5;
        }
        .info-label {
            color: #666;
            font-size: 14px;
        }
        .info-value {
            color: #333;
            font-weight: 500;
            font-size: 14px;
            text-align: right;
        }
        .account-details {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .account-details h2 {
            margin-bottom: 25px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .details-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }
        .detail-group {
            border-left: 3px solid #667eea;
            padding-left: 15px;
        }
        .detail-group h4 {
            color: #667eea;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .detail-group p {
            color: #333;
            font-size: 15px;
            line-height: 1.5;
        }
        .section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section h2 {
            margin-bottom: 25px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
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
            font-size: 13px;
            text-transform: uppercase;
            border-bottom: 2px solid #dee2e6;
        }
        .orders-table td {
            padding: 15px 12px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }
        .orders-table tr:hover {
            background: #f8f9fa;
        }
        .status-badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
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
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        .product-emoji {
            font-size: 48px;
            margin-bottom: 10px;
        }
        .product-name {
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        .product-price {
            color: #667eea;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .add-to-cart {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s;
        }
        .add-to-cart:hover {
            transform: scale(1.05);
        }
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .action-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-decoration: none;
            text-align: center;
            transition: transform 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        .action-card:hover {
            transform: translateY(-3px);
        }
        .action-icon {
            font-size: 32px;
        }
        .action-text {
            font-weight: 600;
            font-size: 14px;
        }
        .no-data {
            text-align: center;
            color: #999;
            padding: 60px 20px;
            background: #f9f9f9;
            border-radius: 10px;
        }
        .no-data-icon {
            font-size: 48px;
            margin-bottom: 15px;
            opacity: 0.5;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <span style="font-size: 32px;">🐵</span>
                <span>Wally's Monkey Parts</span>
            </div>
            <div class="user-menu">
                <span>👤 <?php echo htmlspecialchars($username); ?></span>
                <?php if ($is_admin): ?>
                    <span class="admin-badge">ADMIN ACCESS</span>
                <?php endif; ?>
                <a href="logout.php" class="logout-btn">Sign Out</a>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="welcome-banner">
            <h1>Welcome back, <?php echo htmlspecialchars($first_name); ?>! 👋</h1>
            <p>Your one-stop shop for premium monkey parts and prank supplies</p>
        </div>

        <div class="main-grid">
            <div class="profile-card">
                <div class="profile-header">
                    <div class="profile-avatar">👤</div>
                    <h2><?php echo htmlspecialchars($full_name); ?></h2>
                    <p><?php echo $is_admin ? 'Administrator' : 'Valued Customer'; ?></p>
                </div>
                <div class="profile-body">
                    <div class="profile-info">
                        <h3>Contact Information</h3>
                        <div class="info-row">
                            <span class="info-label">Email:</span>
                            <span class="info-value"><?php echo htmlspecialchars($user['email']); ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Phone:</span>
                            <span class="info-value"><?php echo htmlspecialchars($user['phone'] ?? '(555) 000-0000'); ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Username:</span>
                            <span class="info-value"><?php echo htmlspecialchars($username); ?></span>
                        </div>
                    </div>
                    
                    <div class="profile-info">
                        <h3>Shipping Address</h3>
                        <div class="info-row">
                            <span class="info-label">Street:</span>
                            <span class="info-value"><?php echo htmlspecialchars($user['address'] ?? '123 Main St'); ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">City:</span>
                            <span class="info-value"><?php echo htmlspecialchars($user['city'] ?? 'Springfield'); ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">State:</span>
                            <span class="info-value"><?php echo htmlspecialchars($user['state'] ?? 'CA'); ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">ZIP:</span>
                            <span class="info-value"><?php echo htmlspecialchars($user['zip'] ?? '90210'); ?></span>
                        </div>
                    </div>
                    
                    <div class="profile-info">
                        <h3>Account Status</h3>
                        <div class="info-row">
                            <span class="info-label">Member Since:</span>
                            <span class="info-value"><?php echo date('M Y', strtotime($user['created_at'] ?? '2024-01-01')); ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Account Type:</span>
                            <span class="info-value"><?php echo $is_admin ? 'Admin' : 'Customer'; ?></span>
                        </div>
                        <div class="info-row">
                            <span class="info-label">Status:</span>
                            <span class="info-value" style="color: #28a745;">Active</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="account-details">
                <h2>📋 Account Overview</h2>
                <div class="details-grid">
                    <div class="detail-group">
                        <h4>Personal Information</h4>
                        <p><strong>Full Name:</strong> <?php echo htmlspecialchars($user['full_name'] ?? $username); ?></p>
                        <p><strong>Email:</strong> <?php echo htmlspecialchars($user['email']); ?></p>
                        <p><strong>Phone:</strong> <?php echo htmlspecialchars($user['phone'] ?? 'Not provided'); ?></p>
                    </div>
                    
                    <div class="detail-group">
                        <h4>Billing Address</h4>
                        <p><?php echo htmlspecialchars($user['full_name'] ?? $username); ?></p>
                        <p><?php echo htmlspecialchars($user['address'] ?? '123 Main Street'); ?></p>
                        <p><?php echo htmlspecialchars($user['city'] ?? 'Springfield'); ?>, <?php echo htmlspecialchars($user['state'] ?? 'CA'); ?> <?php echo htmlspecialchars($user['zip'] ?? '90210'); ?></p>
                    </div>
                    
                    <div class="detail-group">
                        <h4>Shipping Address</h4>
                        <p><?php echo htmlspecialchars($user['full_name'] ?? $username); ?></p>
                        <p><?php echo htmlspecialchars($user['address'] ?? '123 Main Street'); ?></p>
                        <p><?php echo htmlspecialchars($user['city'] ?? 'Springfield'); ?>, <?php echo htmlspecialchars($user['state'] ?? 'CA'); ?> <?php echo htmlspecialchars($user['zip'] ?? '90210'); ?></p>
                    </div>
                    
                    <div class="detail-group">
                        <h4>Account Security</h4>
                        <p><strong>User ID:</strong> #<?php echo str_pad($user_id, 6, '0', STR_PAD_LEFT); ?></p>
                        <p><strong>Last Login:</strong> <?php echo date('M j, Y g:i A'); ?></p>
                        <p><strong>2FA Status:</strong> <span style="color: #dc3545;">Disabled</span></p>
                    </div>
                </div>
                
                <?php if ($is_admin): ?>
                <div style="margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%); border-radius: 10px; color: white;">
                    <h3 style="margin-bottom: 15px;">🔧 Administrator Controls</h3>
                    <div class="quick-actions" style="margin-top: 15px;">
                        <a href="admin/users.php" class="action-card" style="background: rgba(255,255,255,0.2);">
                            <span class="action-icon">👥</span>
                            <span class="action-text">Manage Users</span>
                        </a>
                        <a href="admin/products.php" class="action-card" style="background: rgba(255,255,255,0.2);">
                            <span class="action-icon">📦</span>
                            <span class="action-text">Products</span>
                        </a>
                        <a href="admin/orders.php" class="action-card" style="background: rgba(255,255,255,0.2);">
                            <span class="action-icon">📊</span>
                            <span class="action-text">Orders</span>
                        </a>
                        <a href="admin/reports.php" class="action-card" style="background: rgba(255,255,255,0.2);">
                            <span class="action-icon">📈</span>
                            <span class="action-text">Reports</span>
                        </a>
                    </div>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <div class="section">
            <h2>📦 Order History</h2>
            <?php if ($orders_result && $orders_result->num_rows > 0): ?>
                <table class="orders-table">
                    <thead>
                        <tr>
                            <th>Order #</th>
                            <th>Date</th>
                            <th>Ship To</th>
                            <th>Items</th>
                            <th>Total</th>
                            <th>Status</th>
                            <th>Tracking</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php while($order = $orders_result->fetch_assoc()): ?>
                        <tr>
                            <td><strong>#<?php echo str_pad($order['id'], 8, '0', STR_PAD_LEFT); ?></strong></td>
                            <td><?php echo date('M j, Y', strtotime($order['order_date'])); ?></td>
                            <td><?php echo htmlspecialchars($user['city'] ?? 'Springfield'); ?>, <?php echo htmlspecialchars($user['state'] ?? 'CA'); ?></td>
                            <td><?php echo $order['item_count'] ?? rand(1, 5); ?> items</td>
                            <td><strong>$<?php echo number_format($order['total'] ?? rand(50, 500), 2); ?></strong></td>
                            <td>
                                <?php 
                                $statuses = ['completed', 'shipped', 'pending'];
                                $status = $order['status'] ?? $statuses[array_rand($statuses)];
                                ?>
                                <span class="status-badge status-<?php echo $status; ?>">
                                    <?php echo ucfirst($status); ?>
                                </span>
                            </td>
                            <td>
                                <?php if ($status == 'shipped'): ?>
                                    <a href="#" style="color: #667eea;">Track</a>
                                <?php else: ?>
                                    -
                                <?php endif; ?>
                            </td>
                        </tr>
                        <?php endwhile; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <div class="no-data">
                    <div class="no-data-icon">📦</div>
                    <h3>No orders yet</h3>
                    <p>When you place your first order, it will appear here.</p>
                </div>
            <?php endif; ?>
        </div>

        <div class="section">
            <h2>🎪 Featured Products</h2>
            <div class="products-grid">
                <?php 
                $mock_products = [
                    ['emoji' => '🐔', 'name' => 'Rubber Chicken Deluxe', 'price' => 14.99],
                    ['emoji' => '💨', 'name' => 'Whoopee Cushion Pro Max', 'price' => 9.99],
                    ['emoji' => '💩', 'name' => 'Ultra-Realistic Fake Poop', 'price' => 7.99],
                    ['emoji' => '⚡', 'name' => 'Joy Buzzer 3000', 'price' => 16.99],
                    ['emoji' => '✒️', 'name' => 'Disappearing Ink Set', 'price' => 11.99],
                    ['emoji' => '🌸', 'name' => 'Squirting Flower Classic', 'price' => 13.99],
                    ['emoji' => '🎭', 'name' => 'Fake Mustache Collection', 'price' => 8.99],
                    ['emoji' => '🕷️', 'name' => 'Remote Control Spider', 'price' => 24.99]
                ];
                
                foreach ($mock_products as $product): ?>
                <div class="product-card">
                    <div class="product-emoji"><?php echo $product['emoji']; ?></div>
                    <div class="product-name"><?php echo $product['name']; ?></div>
                    <div class="product-price">$<?php echo $product['price']; ?></div>
                    <button class="add-to-cart">Add to Cart</button>
                </div>
                <?php endforeach; ?>
            </div>
        </div>

        <div class="section">
            <h2>🚀 Quick Actions</h2>
            <div class="quick-actions">
                <a href="profile.php" class="action-card">
                    <span class="action-icon">✏️</span>
                    <span class="action-text">Edit Profile</span>
                </a>
                <a href="addresses.php" class="action-card">
                    <span class="action-icon">📍</span>
                    <span class="action-text">Manage Addresses</span>
                </a>
                <a href="payment.php" class="action-card">
                    <span class="action-icon">💳</span>
                    <span class="action-text">Payment Methods</span>
                </a>
                <a href="wishlist.php" class="action-card">
                    <span class="action-icon">❤️</span>
                    <span class="action-text">My Wishlist</span>
                </a>
                <a href="rewards.php" class="action-card">
                    <span class="action-icon">🎁</span>
                    <span class="action-text">Rewards Points</span>
                </a>
                <a href="support.php" class="action-card">
                    <span class="action-icon">💬</span>
                    <span class="action-text">Get Support</span>
                </a>
            </div>
        </div>
    </div>
</body>
</html>