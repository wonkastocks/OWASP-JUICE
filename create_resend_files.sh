#!/bin/bash

# Create resend_verification.php
cat > /tmp/resend_verification.php << 'PHPEND'
<?php
session_start();
require_once 'config.php';

$message = '';
$error = '';

// Handle resend request
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['email'])) {
    $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);
    
    if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Check if user exists and is not verified
        $stmt = $pdo->prepare("SELECT id, username, email_verified, verification_token FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch();
        
        if ($user) {
            if ($user['email_verified'] == 1) {
                $error = "This email is already verified. You can login.";
            } else {
                // Generate new verification token
                $newToken = bin2hex(random_bytes(32));
                
                // Update token in database
                $updateStmt = $pdo->prepare("UPDATE users SET verification_token = ? WHERE id = ?");
                $updateStmt->execute([$newToken, $user['id']]);
                
                // Send verification email
                $to = $email;
                $subject = "WonkaTech CTF - Email Verification (Resent)";
                $verificationLink = BASE_URL . "/verify.php?token=" . $newToken;
                
                $emailMessage = "Hello " . $user['username'] . ",\n\n";
                $emailMessage .= "You requested to resend your verification email.\n\n";
                $emailMessage .= "Please click the link below to verify your email:\n\n";
                $emailMessage .= $verificationLink . "\n\n";
                $emailMessage .= "This link will expire in 24 hours.\n\n";
                $emailMessage .= "If you did not request this, please ignore this email.\n\n";
                $emailMessage .= "Best regards,\n";
                $emailMessage .= "WonkaTech CTF Team";
                
                $headers = "From: noreply@wonkatech.org\r\n";
                $headers .= "Reply-To: noreply@wonkatech.org\r\n";
                $headers .= "X-Mailer: PHP/" . phpversion();
                
                if (@mail($to, $subject, $emailMessage, $headers)) {
                    $message = "Verification email has been resent to " . $email . ". Please check your inbox.";
                } else {
                    $error = "Failed to send email. Please try again later.";
                }
            }
        } else {
            $error = "No account found with this email address.";
        }
    } else {
        $error = "Please enter a valid email address.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resend Verification - WonkaTech CTF</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="container">
        <div class="auth-box">
            <h1>🔄 Resend Verification Email</h1>
            <p>Enter your email address to receive a new verification link</p>
            
            <?php if ($message): ?>
                <div class="success-message"><?php echo htmlspecialchars($message); ?></div>
            <?php endif; ?>
            
            <?php if ($error): ?>
                <div class="error-message"><?php echo htmlspecialchars($error); ?></div>
            <?php endif; ?>
            
            <form method="POST" action="resend_verification.php">
                <div class="form-group">
                    <label for="email">Email Address</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="Enter your email address"
                           value="<?php echo isset($_POST['email']) ? htmlspecialchars($_POST['email']) : ''; ?>">
                </div>
                
                <button type="submit" class="btn btn-primary">Resend Verification Email</button>
            </form>
            
            <div class="auth-links">
                <a href="login.php">Back to Login</a>
                <a href="register.php">Create New Account</a>
            </div>
        </div>
    </div>
</body>
</html>
PHPEND

# Create PHP script to update login.php
cat > /tmp/update_login_resend.php << 'PHPSCRIPT'
<?php
// Read login.php
$content = file_get_contents('login.php');

// Check if already has resend link
if (strpos($content, 'resend_verification.php') !== false) {
    echo "login.php already has resend verification link\n";
    exit;
}

// Find where to add the unverified check
$search = '$error = "Invalid username or password.";';

// Add check for unverified email with resend link
$replace = '// Check if email is verified
                $checkStmt = $pdo->prepare("SELECT email_verified FROM users WHERE username = ? OR email = ?");
                $checkStmt->execute([$username, $username]);
                $userCheck = $checkStmt->fetch();
                
                if ($userCheck && $userCheck["email_verified"] == 0) {
                    $error = "Your email is not verified. <a href=\"resend_verification.php\" style=\"color: #667eea; text-decoration: underline;\">Click here to resend verification email</a>";
                } else {
                    $error = "Invalid username or password.";
                }';

// Replace in file
$content = str_replace($search, $replace, $content);

// Also add a general resend link in the form area
$formSearch = '<div class="auth-links">';
$formReplace = '<div class="auth-links">
                <a href="resend_verification.php">Resend Verification Email</a> |';

$content = str_replace($formSearch, $formReplace, $content);

// Save the updated file
file_put_contents('login.php', $content);
echo "login.php updated with resend verification links\n";
?>
PHPSCRIPT

echo "Files created in /tmp/"