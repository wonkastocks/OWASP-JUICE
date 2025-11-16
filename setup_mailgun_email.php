<?php
// Mailgun Email Setup for WonkaTech CTF Platform
// This updates register.php to use Mailgun API for sending emails

// Mailgun configuration (you'll need to sign up at mailgun.com for free)
define('MAILGUN_API_KEY', 'YOUR_MAILGUN_API_KEY'); // Get from Mailgun dashboard
define('MAILGUN_DOMAIN', 'sandbox_YOUR_DOMAIN.mailgun.org'); // Your sandbox domain from Mailgun
define('MAILGUN_API_URL', 'https://api.mailgun.net/v3/' . MAILGUN_DOMAIN . '/messages');

function sendVerificationEmail($to, $username, $token) {
    $verification_link = "https://wonkatech.org/verify.php?token=" . $token;
    
    $subject = "WonkaTech CTF Platform - Email Verification";
    
    $html = "
    <html>
    <body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
        <div style='max-width: 600px; margin: 0 auto; padding: 20px;'>
            <h2 style='color: #667eea;'>Welcome to WonkaTech CTF Platform!</h2>
            <p>Hello {$username},</p>
            <p>Thank you for registering! Please verify your email address by clicking the button below:</p>
            <div style='text-align: center; margin: 30px 0;'>
                <a href='{$verification_link}' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;'>Verify Email</a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p style='word-break: break-all; color: #667eea;'>{$verification_link}</p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't register for this account, please ignore this email.</p>
            <hr style='border: none; border-top: 1px solid #eee; margin: 30px 0;'>
            <p style='color: #999; font-size: 12px;'>WonkaTech CTF Team</p>
        </div>
    </body>
    </html>
    ";
    
    $text = "Hello {$username},\n\n";
    $text .= "Thank you for registering at WonkaTech CTF Platform!\n\n";
    $text .= "Please verify your email address by visiting:\n\n";
    $text .= "{$verification_link}\n\n";
    $text .= "This link will expire in 24 hours.\n\n";
    $text .= "If you didn't register for this account, please ignore this email.\n\n";
    $text .= "Best regards,\nWonkaTech CTF Team";
    
    // Send via Mailgun API
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, MAILGUN_API_URL);
    curl_setopt($ch, CURLOPT_USERPWD, 'api:' . MAILGUN_API_KEY);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, [
        'from' => 'WonkaTech CTF <noreply@' . MAILGUN_DOMAIN . '>',
        'to' => $to,
        'subject' => $subject,
        'text' => $text,
        'html' => $html
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $result = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    return $httpCode === 200;
}

// Example usage in register.php:
// After creating the user and generating the token:
// if (sendVerificationEmail($email, $username, $verificationToken)) {
//     $success = "Registration successful! Please check your email to verify your account.";
// } else {
//     $success = "Registration successful but email could not be sent. Please contact admin.";
// }
?>