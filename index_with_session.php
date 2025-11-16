<?php include 'session_header.php'; ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wally's Monkey Parts - Premium Automobile Parts</title>
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

        .hero {
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            padding: 80px 40px;
            text-align: center;
        }

        .hero h2 {
            font-size: 48px;
            color: #333;
            margin-bottom: 20px;
        }

        .hero p {
            font-size: 20px;
            color: #666;
            margin-bottom: 30px;
        }

        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
            transition: transform 0.3s;
        }

        .cta-button:hover {
            transform: translateY(-2px);
        }

        .products {
            padding: 60px 40px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .products h2 {
            font-size: 36px;
            color: #333;
            margin-bottom: 40px;
            text-align: center;
        }

        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
        }

        .product-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            text-align: center;
        }

        .product-card:hover {
            transform: translateY(-5px);
        }

        .product-icon {
            font-size: 60px;
            margin-bottom: 15px;
        }

        .product-name {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }

        .product-price {
            font-size: 24px;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .add-to-cart {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }

        .add-to-cart:hover {
            transform: scale(1.05);
        }

        .features {
            background: #fff;
            padding: 60px 40px;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .feature {
            text-align: center;
        }

        .feature-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }

        .feature h3 {
            font-size: 24px;
            color: #333;
            margin-bottom: 10px;
        }

        .feature p {
            color: #666;
            line-height: 1.6;
        }

        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 60px;
        }

        .user-greeting {
            background: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <?php if ($isLoggedIn): ?>
    <div class="user-greeting">
        Welcome back, <?php echo htmlspecialchars($username); ?>! Enjoy shopping at Wally's Monkey Parts 🐵
    </div>
    <?php endif; ?>

    <header>
        <div class="logo">
            <span class="logo-icon">🐵</span>
            <h1>Wally's Monkey Parts</h1>
        </div>
        <nav>
            <a href="/">Home</a>
            <a href="/shop.php">Shop</a>
            <a href="/about.php">About</a>
            <a href="/contact.php">Contact</a>
        </nav>
    </header>

    <section class="hero">
        <h2>Premium Auto Parts for Every Vehicle</h2>
        <p>Quality parts, unbeatable prices, and fast shipping!</p>
        <a href="/shop.php" class="cta-button">Shop Now</a>
    </section>

    <section class="products">
        <h2>Featured Products</h2>
        <div class="product-grid">
            <div class="product-card">
                <div class="product-icon">🔧</div>
                <div class="product-name">Premium Brake Pads</div>
                <div class="product-price">$89.99</div>
                <button class="add-to-cart" onclick="addToCart('Premium Brake Pads', 89.99)">Add to Cart</button>
            </div>
            <div class="product-card">
                <div class="product-icon">⚙️</div>
                <div class="product-name">Oil Filter Pro</div>
                <div class="product-price">$24.99</div>
                <button class="add-to-cart" onclick="addToCart('Oil Filter Pro', 24.99)">Add to Cart</button>
            </div>
            <div class="product-card">
                <div class="product-icon">🔋</div>
                <div class="product-name">SuperCharge Battery</div>
                <div class="product-price">$149.99</div>
                <button class="add-to-cart" onclick="addToCart('SuperCharge Battery', 149.99)">Add to Cart</button>
            </div>
            <div class="product-card">
                <div class="product-icon">💡</div>
                <div class="product-name">LED Headlight Kit</div>
                <div class="product-price">$79.99</div>
                <button class="add-to-cart" onclick="addToCart('LED Headlight Kit', 79.99)">Add to Cart</button>
            </div>
        </div>
    </section>

    <section class="features">
        <div class="features-grid">
            <div class="feature">
                <div class="feature-icon">🚚</div>
                <h3>Fast Shipping</h3>
                <p>Free shipping on orders over $50. Most items ship same day!</p>
            </div>
            <div class="feature">
                <div class="feature-icon">✅</div>
                <h3>Quality Guaranteed</h3>
                <p>All parts come with manufacturer warranty and our satisfaction guarantee.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">💬</div>
                <h3>Expert Support</h3>
                <p>Our team of experts is here to help you find the right parts for your vehicle.</p>
            </div>
        </div>
    </section>

    <footer>
        <p>&copy; 2025 Wally's Monkey Parts. All rights reserved.</p>
    </footer>

    <script>
    function addToCart(productName, price) {
        <?php if ($isLoggedIn): ?>
            // Add to cart logic for logged in users
            alert(`Added ${productName} to your cart!`);
            
            // Update cart count
            const cartCount = document.querySelector('.cart-count');
            if (cartCount) {
                cartCount.textContent = parseInt(cartCount.textContent) + 1;
            }
        <?php else: ?>
            // Redirect to login if not logged in
            if (confirm(`Please sign in to add items to your cart. Would you like to sign in now?`)) {
                window.location.href = '/login.php';
            }
        <?php endif; ?>
    }
    </script>
</body>
</html>