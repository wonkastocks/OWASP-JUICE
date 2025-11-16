#!/bin/bash

# Setup email system for WonkaTech CTF Platform
# This script configures msmtp (a simple SMTP client) to send emails

echo "Setting up email system..."

# Install msmtp and mail utilities
apt-get update
apt-get install -y msmtp msmtp-mta mailutils

# Create msmtp configuration
cat > /etc/msmtprc << 'EOF'
# Default settings
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        /var/log/msmtp.log

# Gmail account (you can change this to any SMTP provider)
account        gmail
host           smtp.gmail.com
port           587
from           noreply@wonkatech.org
user           wonkastocks@gmail.com
# You need to use an App Password for Gmail, not your regular password
# Go to: https://myaccount.google.com/apppasswords to generate one
password       YOUR_APP_PASSWORD_HERE

# Set default account
account default : gmail
EOF

# Set proper permissions
chmod 600 /etc/msmtprc
touch /var/log/msmtp.log
chmod 666 /var/log/msmtp.log

# Configure PHP to use msmtp
echo "sendmail_path = /usr/bin/msmtp -t" >> /etc/php/8.1/apache2/php.ini

# Update register.php to properly send emails
cd /var/www/ctf-platform/

cat > update_register_email.php << 'PHPSCRIPT'
<?php
// Read the current register.php
$content = file_get_contents('register.php');

// Find the success message line and add email sending code after it
$search = '$success = "Registration successful! Please check your email to verify your account.";';
$replace = '$success = "Registration successful! Please check your email to verify your account.";
                    
                    // Send verification email
                    $to = $email;
                    $subject = "WonkaTech CTF Platform - Email Verification";
                    $verification_link = BASE_URL . "/verify.php?token=" . $verificationToken;
                    
                    $message = "Hello " . $username . ",\n\n";
                    $message .= "Thank you for registering at WonkaTech CTF Platform!\n\n";
                    $message .= "Please click the following link to verify your email address:\n\n";
                    $message .= $verification_link . "\n\n";
                    $message .= "This link will expire in 24 hours.\n\n";
                    $message .= "If you did not register for this account, please ignore this email.\n\n";
                    $message .= "Best regards,\n";
                    $message .= "WonkaTech CTF Team";
                    
                    $headers = "From: WonkaTech CTF <noreply@wonkatech.org>\r\n";
                    $headers .= "Reply-To: noreply@wonkatech.org\r\n";
                    $headers .= "X-Mailer: PHP/" . phpversion();
                    
                    // Send the email
                    if (!mail($to, $subject, $message, $headers)) {
                        error_log("Failed to send verification email to: " . $email);
                    }';

$content = str_replace($search, $replace, $content);
file_put_contents('register.php', $content);
echo "register.php updated with email sending code\n";
?>
PHPSCRIPT

php update_register_email.php
rm update_register_email.php

# Restart Apache to apply PHP changes
systemctl restart apache2

echo ""
echo "Email system setup complete!"
echo ""
echo "IMPORTANT: You need to configure the SMTP settings in /etc/msmtprc"
echo "For Gmail:"
echo "1. Go to https://myaccount.google.com/apppasswords"
echo "2. Generate an app password"
echo "3. Edit /etc/msmtprc and replace YOUR_APP_PASSWORD_HERE with the generated password"
echo ""
echo "For testing without real email, you can use a service like:"
echo "- Mailtrap.io (free tier available)"
echo "- MailHog (local testing)"
echo ""