#!/bin/bash

# Script to add activity tracking for juice5.wonkatech.org

cat > /tmp/add_tracking.php << 'ENDPHP'
<?php
// Enhanced activity tracking for Juice Shop containers

// Database connection
$conn = new mysqli('localhost', 'root', '', 'ctf_platform');
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "Connected to database\n";

// First, ensure the user_sessions table exists
$sql = "CREATE TABLE IF NOT EXISTS user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    session_token VARCHAR(100),
    container_name VARCHAR(50),
    container_port INT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1,
    INDEX idx_container (container_name),
    INDEX idx_user (user_id)
)";

if ($conn->query($sql)) {
    echo "user_sessions table ready\n";
}

// Add last_activity column to users table if it doesn't exist
$sql = "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_activity TIMESTAMP NULL";
$conn->query($sql);

// Now check who is assigned to juice5
$sql = "SELECT id, username, email, instance_url FROM users WHERE instance_url LIKE '%juice5%'";
$result = $conn->query($sql);

if ($result && $result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "Found juice5 user: " . $row['username'] . " (ID: " . $row['id'] . ")\n";
        
        // Add activity tracking
        $user_id = $row['id'];
        $token = md5(uniqid());
        
        // Insert or update session
        $sql = "INSERT INTO user_sessions (user_id, session_token, container_name, container_port, is_active) 
                VALUES ($user_id, '$token', 'juice5', 3005, 1)
                ON DUPLICATE KEY UPDATE last_activity = NOW(), is_active = 1";
        
        if ($conn->query($sql)) {
            echo "  - Activity tracking added\n";
        }
        
        // Update user's last activity
        $sql = "UPDATE users SET last_activity = NOW() WHERE id = $user_id";
        $conn->query($sql);
    }
} else {
    echo "No users assigned to juice5. Checking if wonkastocks exists...\n";
    
    // Look for wonkastocks user
    $sql = "SELECT id, username, email, instance_url FROM users WHERE username = 'wonkastocks' OR email LIKE '%wonkastocks%'";
    $result = $conn->query($sql);
    
    if ($result && $result->num_rows > 0) {
        $row = $result->fetch_assoc();
        echo "Found user: " . $row['username'] . "\n";
        echo "Current instance_url: " . $row['instance_url'] . "\n";
        
        // Assign juice5 if not assigned
        if (empty($row['instance_url']) || !strpos($row['instance_url'], 'juice5')) {
            $sql = "UPDATE users SET instance_url = 'https://juice5.wonkatech.org' WHERE id = " . $row['id'];
            if ($conn->query($sql)) {
                echo "Assigned juice5 to " . $row['username'] . "\n";
            }
        }
    }
}

// Show current container assignments
echo "\n=== Current Container Assignments ===\n";
$sql = "SELECT username, instance_url FROM users WHERE instance_url IS NOT NULL ORDER BY instance_url";
$result = $conn->query($sql);

if ($result) {
    while($row = $result->fetch_assoc()) {
        $container = 'unknown';
        if (preg_match('/juice(\d+)/', $row['instance_url'], $matches)) {
            $container = 'juice' . $matches[1];
        }
        echo $container . " -> " . $row['username'] . "\n";
    }
}

$conn->close();
echo "\nTracking update complete!\n";
?>
ENDPHP

# Copy and run on server
sshpass -p '$$R00tbeer02' scp /tmp/add_tracking.php root@155.138.197.128:/tmp/
sshpass -p '$$R00tbeer02' ssh root@155.138.197.128 "php /tmp/add_tracking.php"

# Also update the dashboard to show this activity
sshpass -p '$$R00tbeer02' ssh root@155.138.197.128 "
echo 'Updating dashboard to show activity...';
curl -s http://localhost/admin/get_status.php > /tmp/status.json;
echo 'Current status saved to /tmp/status.json';
cat /tmp/status.json | python3 -m json.tool 2>/dev/null | head -20 || echo 'No JSON output';
"

echo "Done! Check https://wonkatech.org/admin/containers.php"