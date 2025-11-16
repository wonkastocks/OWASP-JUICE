<?php
// Container Activity Monitor - Shuts down containers after 10 minutes of inactivity
require_once 'config.php';

function logActivity($message) {
    $timestamp = date('Y-m-d H:i:s');
    echo "[$timestamp] $message\n";
}

$conn = getDBConnection();

// Update last_activity for active containers by checking Docker logs
$activeContainers = shell_exec("docker ps --format '{{.Names}}' | grep juice-user");
$activeList = array_filter(explode("\n", trim($activeContainers)));

foreach ($activeList as $containerName) {
    // Check last log entry time to determine activity
    $lastLog = shell_exec("docker logs $containerName --tail 1 --timestamps 2>&1 | head -1");
    
    if ($lastLog) {
        // Parse timestamp from log (format: 2024-01-20T10:30:45.123456789Z)
        if (preg_match('/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})/', $lastLog, $matches)) {
            $logTime = strtotime(str_replace('T', ' ', $matches[1]));
            $minutesAgo = (time() - $logTime) / 60;
            
            // Update database with activity status
            $stmt = $conn->prepare("UPDATE containers SET last_activity = NOW() WHERE container_name = ? AND status = 'assigned'");
            $stmt->bind_param("s", $containerName);
            $stmt->execute();
            
            logActivity("Container $containerName - Last activity: " . round($minutesAgo, 1) . " minutes ago");
        }
    }
}

// Find containers inactive for more than 10 minutes
$inactiveThreshold = 10; // minutes
$sql = "SELECT c.id, c.container_name, c.port, c.status, c.assigned_to, c.last_activity, u.username 
        FROM containers c 
        LEFT JOIN users u ON c.assigned_to = u.id 
        WHERE c.status = 'assigned' 
        AND c.last_activity < DATE_SUB(NOW(), INTERVAL ? MINUTE)";

$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $inactiveThreshold);
$stmt->execute();
$result = $stmt->get_result();

$shutdownCount = 0;
while ($container = $result->fetch_assoc()) {
    $containerName = $container['container_name'];
    $username = $container['username'] ?? 'Unknown';
    $lastActivity = $container['last_activity'];
    
    logActivity("Shutting down inactive container: $containerName (User: $username, Last activity: $lastActivity)");
    
    // Stop the Docker container
    $stopCmd = "docker stop $containerName 2>&1";
    $stopResult = shell_exec($stopCmd);
    
    if (strpos($stopResult, 'Error') === false) {
        // Update database - mark as available but keep assignment
        // This ensures user gets same container when they return
        $updateSql = "UPDATE containers SET status = 'stopped', last_activity = NOW() WHERE id = ?";
        $updateStmt = $conn->prepare($updateSql);
        $updateStmt->bind_param("i", $container['id']);
        $updateStmt->execute();
        
        // Log the shutdown
        $auditSql = "INSERT INTO audit_log (admin_id, action, details) VALUES (0, 'auto_shutdown', ?)";
        $auditStmt = $conn->prepare($auditSql);
        $details = "Auto-shutdown container $containerName for user $username after $inactiveThreshold minutes of inactivity";
        $auditStmt->bind_param("s", $details);
        $auditStmt->execute();
        
        $shutdownCount++;
        logActivity("Successfully stopped container: $containerName");
    } else {
        logActivity("Error stopping container $containerName: $stopResult");
    }
}

if ($shutdownCount > 0) {
    logActivity("Shutdown $shutdownCount inactive container(s)");
} else {
    logActivity("No inactive containers found");
}

// Clean up any orphaned Docker containers (not in database)
$allDockerContainers = shell_exec("docker ps -a --format '{{.Names}}' | grep juice-user");
$dockerList = array_filter(explode("\n", trim($allDockerContainers)));

foreach ($dockerList as $dockerContainer) {
    $checkSql = "SELECT id FROM containers WHERE container_name = ?";
    $checkStmt = $conn->prepare($checkSql);
    $checkStmt->bind_param("s", $dockerContainer);
    $checkStmt->execute();
    
    if ($checkStmt->get_result()->num_rows == 0) {
        logActivity("Found orphaned container: $dockerContainer - removing");
        shell_exec("docker stop $dockerContainer 2>&1");
        shell_exec("docker rm $dockerContainer 2>&1");
    }
}

$conn->close();

logActivity("Container monitoring cycle completed");
?>