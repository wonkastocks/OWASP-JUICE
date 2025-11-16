#!/bin/bash

# Create PHP script to add unverified user
cat > /tmp/create_unverified_user.php << 'PHPEND'
<?php
require_once 'config.php';

// Create an unverified test user
$username = 'unverified_user';
$email = 'unverified@test.com';
$password = password_hash('TestPass123!', PASSWORD_DEFAULT);
$token = bin2hex(random_bytes(32));

// First check if user exists
$check = $pdo->prepare('SELECT id FROM users WHERE username = ? OR email = ?');
$check->execute([$username, $email]);

if ($check->fetch()) {
    // Delete existing user
    $delete = $pdo->prepare('DELETE FROM users WHERE username = ? OR email = ?');
    $delete->execute([$username, $email]);
    echo "Deleted existing test user\n";
}

// Insert new unverified user with email_verified = 0
$stmt = $pdo->prepare('INSERT INTO users (username, email, password, verification_token, email_verified) VALUES (?, ?, ?, ?, 0)');
$stmt->execute([$username, $email, $password, $token]);

echo "Created unverified test user:\n";
echo "Username: " . $username . "\n";
echo "Email: " . $email . "\n";
echo "Password: TestPass123!\n";
echo "Email verified: No\n";
?>
PHPEND

echo "Script created at /tmp/create_unverified_user.php"