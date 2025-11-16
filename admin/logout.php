<?php
session_start();

// Log the logout action
if (isset($_SESSION['admin_email'])) {
    require_once 'config.php';
    require_once 'functions.php';
    logAdminActivity('admin_logout', ['email' => $_SESSION['admin_email']]);
}

// Destroy the session
session_unset();
session_destroy();

// Redirect to login page
header("Location: admin_login.php");
exit();
?>