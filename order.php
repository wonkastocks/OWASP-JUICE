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
$username = $_SESSION['username'];
$is_admin = $_SESSION['is_admin'];

// Fetch user's full name
$sql = "SELECT full_name FROM users WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
$user = $result->fetch_assoc();
$full_name = $user['full_name'] ?: $username;

// Handle order submission
$orderMessage = '';
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['place_order'])) {
    $cart = json_decode($_POST['cart_data'], true);
    $total = $_POST['total_amount'];
    
    // Generate order number
    $order_number = 'ORD-' . date('Y') . '-' . str_pad(rand(1, 9999), 4, '0', STR_PAD_LEFT);
    
    $orderMessage = '<div class="success-message">✅ Order ' . $order_number . ' placed successfully! Total: $' . number_format($total, 2) . '</div>';
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Place Order - Wally's Monkey Parts</title>
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
            text-decoration: none;
        }

        .logo-icon {
            font-size: 40px;
        }

        .logo h1 {
            font-size: 24px;
            font-weight: bold;
        }

        .user-section {
            display: flex;
            align-items: center;
            gap: 20px;
            color: white;
        }

        .welcome-text {
            font-size: 14px;
            opacity: 0.9;
        }

        .profile-link {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            color: white;
            text-decoration: none;
            transition: background 0.3s;
        }

        .profile-link:hover {
            background: rgba(255,255,255,0.3);
        }

        .logout-btn {
            background: rgba(255,68,68,0.2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            transition: background 0.3s;
            border: 1px solid rgba(255,255,255,0.3);
        }

        .logout-btn:hover {
            background: rgba(255,68,68,0.3);
        }

        .container {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .page-title {
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }

        .page-subtitle {
            color: #666;
            margin-bottom: 30px;
        }

        .order-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
        }

        .products-section {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .section-title {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }

        .product-list {
            display: grid;
            gap: 20px;
        }

        .product-item {
            display: grid;
            grid-template-columns: 60px 1fr auto;
            gap: 20px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            align-items: center;
            transition: box-shadow 0.3s;
        }

        .product-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .product-icon {
            font-size: 40px;
            text-align: center;
        }

        .product-details {
            flex: 1;
        }

        .product-name {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }

        .product-description {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }

        .product-price {
            font-size: 20px;
            color: #667eea;
            font-weight: bold;
        }

        .quantity-controls {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .qty-btn {
            width: 30px;
            height: 30px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
            transition: all 0.3s;
        }

        .qty-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .qty-display {
            min-width: 40px;
            text-align: center;
            font-weight: bold;
        }

        .cart-section {
            position: sticky;
            top: 20px;
        }

        .cart-box {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .cart-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }

        .cart-item:last-child {
            border-bottom: none;
        }

        .cart-total {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
            font-size: 20px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            color: #333;
        }

        .cart-total span:last-child {
            color: #667eea;
        }

        .place-order-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
            transition: transform 0.3s;
        }

        .place-order-btn:hover {
            transform: translateY(-2px);
        }

        .place-order-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .empty-cart {
            text-align: center;
            color: #999;
            padding: 20px;
        }

        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #c3e6cb;
        }

        .categories {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .category-tab {
            padding: 8px 16px;
            background: #f0f0f0;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .category-tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .stock-info {
            font-size: 12px;
            color: #28a745;
            margin-top: 5px;
        }

        .out-of-stock {
            color: #dc3545;
        }
    </style>
</head>
<body>
    <header>
        <a href="/" class="logo">
            <span class="logo-icon">🐵</span>
            <h1>Wally's Monkey Parts</h1>
        </a>
        <div class="user-section">
            <span class="welcome-text">Shopping as: <?php echo htmlspecialchars($full_name); ?></span>
            <a href="dashboard.php" class="profile-link">
                👤 My Profile
            </a>
            <a href="logout.php" class="logout-btn">Logout</a>
        </div>
    </header>

    <div class="container">
        <h1 class="page-title">Place Your Order</h1>
        <p class="page-subtitle">Select the parts you need and we'll ship them fast!</p>

        <?php echo $orderMessage; ?>

        <div class="order-grid">
            <div class="products-section">
                <h2 class="section-title">Available Products</h2>
                
                <div class="categories">
                    <button class="category-tab active" onclick="filterCategory('all')">All Products</button>
                    <button class="category-tab" onclick="filterCategory('brakes')">Brakes</button>
                    <button class="category-tab" onclick="filterCategory('engine')">Engine</button>
                    <button class="category-tab" onclick="filterCategory('electrical')">Electrical</button>
                </div>

                <div class="product-list">
                    <div class="product-item" data-category="brakes">
                        <div class="product-icon">🔧</div>
                        <div class="product-details">
                            <div class="product-name">Premium Brake Pads</div>
                            <div class="product-description">High-performance ceramic brake pads</div>
                            <div class="product-price">$89.99</div>
                            <div class="stock-info">✓ In Stock (15 available)</div>
                        </div>
                        <div class="quantity-controls">
                            <button class="qty-btn" onclick="updateQuantity('brake-pads', -1)">-</button>
                            <span class="qty-display" id="qty-brake-pads">0</span>
                            <button class="qty-btn" onclick="updateQuantity('brake-pads', 1)">+</button>
                        </div>
                    </div>

                    <div class="product-item" data-category="engine">
                        <div class="product-icon">⚙️</div>
                        <div class="product-details">
                            <div class="product-name">Oil Filter Pro</div>
                            <div class="product-description">Premium oil filter for all vehicles</div>
                            <div class="product-price">$24.99</div>
                            <div class="stock-info">✓ In Stock (42 available)</div>
                        </div>
                        <div class="quantity-controls">
                            <button class="qty-btn" onclick="updateQuantity('oil-filter', -1)">-</button>
                            <span class="qty-display" id="qty-oil-filter">0</span>
                            <button class="qty-btn" onclick="updateQuantity('oil-filter', 1)">+</button>
                        </div>
                    </div>

                    <div class="product-item" data-category="electrical">
                        <div class="product-icon">🔋</div>
                        <div class="product-details">
                            <div class="product-name">SuperCharge Battery</div>
                            <div class="product-description">12V automotive battery, 3-year warranty</div>
                            <div class="product-price">$149.99</div>
                            <div class="stock-info">✓ In Stock (8 available)</div>
                        </div>
                        <div class="quantity-controls">
                            <button class="qty-btn" onclick="updateQuantity('battery', -1)">-</button>
                            <span class="qty-display" id="qty-battery">0</span>
                            <button class="qty-btn" onclick="updateQuantity('battery', 1)">+</button>
                        </div>
                    </div>

                    <div class="product-item" data-category="electrical">
                        <div class="product-icon">💡</div>
                        <div class="product-details">
                            <div class="product-name">LED Headlight Kit</div>
                            <div class="product-description">Ultra-bright LED conversion kit</div>
                            <div class="product-price">$79.99</div>
                            <div class="stock-info">✓ In Stock (23 available)</div>
                        </div>
                        <div class="quantity-controls">
                            <button class="qty-btn" onclick="updateQuantity('headlight', -1)">-</button>
                            <span class="qty-display" id="qty-headlight">0</span>
                            <button class="qty-btn" onclick="updateQuantity('headlight', 1)">+</button>
                        </div>
                    </div>

                    <div class="product-item" data-category="engine">
                        <div class="product-icon">🛢️</div>
                        <div class="product-details">
                            <div class="product-name">Synthetic Motor Oil</div>
                            <div class="product-description">5W-30 Full synthetic, 5 quart</div>
                            <div class="product-price">$34.99</div>
                            <div class="stock-info">✓ In Stock (50+ available)</div>
                        </div>
                        <div class="quantity-controls">
                            <button class="qty-btn" onclick="updateQuantity('motor-oil', -1)">-</button>
                            <span class="qty-display" id="qty-motor-oil">0</span>
                            <button class="qty-btn" onclick="updateQuantity('motor-oil', 1)">+</button>
                        </div>
                    </div>

                    <div class="product-item" data-category="brakes">
                        <div class="product-icon">🛑</div>
                        <div class="product-details">
                            <div class="product-name">Brake Rotors (Pair)</div>
                            <div class="product-description">Ventilated disc brake rotors</div>
                            <div class="product-price">$159.99</div>
                            <div class="stock-info">✓ In Stock (6 available)</div>
                        </div>
                        <div class="quantity-controls">
                            <button class="qty-btn" onclick="updateQuantity('rotors', -1)">-</button>
                            <span class="qty-display" id="qty-rotors">0</span>
                            <button class="qty-btn" onclick="updateQuantity('rotors', 1)">+</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="cart-section">
                <div class="cart-box">
                    <h2 class="section-title">Your Cart</h2>
                    <div id="cart-items">
                        <div class="empty-cart">Your cart is empty</div>
                    </div>
                    <div class="cart-total" style="display: none;">
                        <span>Total:</span>
                        <span id="cart-total">$0.00</span>
                    </div>
                    <form method="POST" id="order-form">
                        <input type="hidden" name="cart_data" id="cart-data">
                        <input type="hidden" name="total_amount" id="total-amount">
                        <button type="submit" name="place_order" class="place-order-btn" disabled>
                            Place Order
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script>
    const products = {
        'brake-pads': { name: 'Premium Brake Pads', price: 89.99 },
        'oil-filter': { name: 'Oil Filter Pro', price: 24.99 },
        'battery': { name: 'SuperCharge Battery', price: 149.99 },
        'headlight': { name: 'LED Headlight Kit', price: 79.99 },
        'motor-oil': { name: 'Synthetic Motor Oil', price: 34.99 },
        'rotors': { name: 'Brake Rotors (Pair)', price: 159.99 }
    };

    let cart = {};

    function updateQuantity(productId, change) {
        const currentQty = cart[productId] || 0;
        const newQty = Math.max(0, currentQty + change);
        
        if (newQty === 0) {
            delete cart[productId];
        } else {
            cart[productId] = newQty;
        }
        
        document.getElementById('qty-' + productId).textContent = newQty;
        updateCart();
    }

    function updateCart() {
        const cartItemsDiv = document.getElementById('cart-items');
        const cartTotalDiv = document.querySelector('.cart-total');
        const placeOrderBtn = document.querySelector('.place-order-btn');
        
        if (Object.keys(cart).length === 0) {
            cartItemsDiv.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
            cartTotalDiv.style.display = 'none';
            placeOrderBtn.disabled = true;
        } else {
            let html = '';
            let total = 0;
            
            for (const [productId, qty] of Object.entries(cart)) {
                const product = products[productId];
                const subtotal = product.price * qty;
                total += subtotal;
                html += `
                    <div class="cart-item">
                        <div>
                            <div>${product.name}</div>
                            <small>${qty} × $${product.price.toFixed(2)}</small>
                        </div>
                        <div>$${subtotal.toFixed(2)}</div>
                    </div>
                `;
            }
            
            cartItemsDiv.innerHTML = html;
            document.getElementById('cart-total').textContent = '$' + total.toFixed(2);
            cartTotalDiv.style.display = 'flex';
            placeOrderBtn.disabled = false;
            
            // Update hidden form fields
            document.getElementById('cart-data').value = JSON.stringify(cart);
            document.getElementById('total-amount').value = total.toFixed(2);
        }
    }

    function filterCategory(category) {
        const tabs = document.querySelectorAll('.category-tab');
        tabs.forEach(tab => tab.classList.remove('active'));
        event.target.classList.add('active');
        
        const items = document.querySelectorAll('.product-item');
        items.forEach(item => {
            if (category === 'all' || item.dataset.category === category) {
                item.style.display = 'grid';
            } else {
                item.style.display = 'none';
            }
        });
    }
    </script>
</body>
</html>