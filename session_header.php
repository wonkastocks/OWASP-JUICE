<?php
session_start();

// This file should be included at the top of every page
// It provides the navigation bar with login/profile functionality

$isLoggedIn = isset($_SESSION['user_id']);
$username = $isLoggedIn ? $_SESSION['username'] : '';
$isAdmin = isset($_SESSION['is_admin']) ? $_SESSION['is_admin'] : 0;
?>

<style>
.nav-user-section {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-left: auto;
}

.nav-user-section a {
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 5px;
    transition: background 0.3s;
}

.nav-user-section a:hover {
    background: rgba(255,255,255,0.1);
}

.profile-dropdown {
    position: relative;
    display: inline-block;
}

.profile-icon {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    cursor: pointer;
    border: 2px solid white;
}

.dropdown-content {
    display: none;
    position: absolute;
    right: 0;
    background: white;
    min-width: 200px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    z-index: 1000;
    border-radius: 8px;
    margin-top: 10px;
}

.dropdown-content a {
    color: #333 !important;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    transition: background 0.3s;
}

.dropdown-content a:hover {
    background: #f5f5f5;
}

.dropdown-content .user-info {
    padding: 12px 16px;
    border-bottom: 1px solid #e0e0e0;
    font-weight: bold;
    color: #333;
}

.profile-dropdown:hover .dropdown-content {
    display: block;
}

.nav-login-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white !important;
    padding: 8px 20px !important;
    border-radius: 25px !important;
    font-weight: bold;
}

.nav-cart {
    position: relative;
    color: white;
    font-size: 24px;
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
</style>

<script>
// Add to existing navigation bar
document.addEventListener('DOMContentLoaded', function() {
    // Find the main navigation or header
    const header = document.querySelector('header') || document.querySelector('nav') || document.querySelector('.navbar');
    if (header) {
        const userSection = document.createElement('div');
        userSection.className = 'nav-user-section';
        
        <?php if ($isLoggedIn): ?>
            // Show cart icon
            userSection.innerHTML = `
                <div class="nav-cart">
                    🛒
                    <span class="cart-count">0</span>
                </div>
                <div class="profile-dropdown">
                    <div class="profile-icon"><?php echo strtoupper(substr($username, 0, 1)); ?></div>
                    <div class="dropdown-content">
                        <div class="user-info">Hello, <?php echo htmlspecialchars($username); ?></div>
                        <a href="/dashboard.php">My Profile</a>
                        <a href="/orders.php">My Orders</a>
                        <?php if ($isAdmin): ?>
                            <a href="/admin.php" style="color: #667eea !important;">Admin Panel</a>
                        <?php endif; ?>
                        <a href="/logout.php" style="color: #ff4444 !important;">Logout</a>
                    </div>
                </div>
            `;
        <?php else: ?>
            // Show login button
            userSection.innerHTML = `
                <a href="/login.php" class="nav-login-btn">Sign In</a>
            `;
        <?php endif; ?>
        
        // Add to header
        header.appendChild(userSection);
    }
});
</script>