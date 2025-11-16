<?php
// Container Restart Helper - Ensures users get their assigned container running
require_once 'config.php';

function restartUserContainer($userId) {
    $conn = getDBConnection();
    
    // Find user's assigned container
    $sql = "SELECT c.*, u.username 
            FROM containers c 
            JOIN users u ON c.assigned_to = u.id 
            WHERE c.assigned_to = ?";
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $userId);
    $stmt->execute();
    $result = $stmt->get_result();
    
    if ($container = $result->fetch_assoc()) {
        $containerName = $container['container_name'];
        $port = $container['port'];
        $status = $container['status'];
        
        // Check if container exists in Docker
        $dockerCheck = shell_exec("docker ps -a --format '{{.Names}}' | grep -w $containerName");
        
        if (trim($dockerCheck) == $containerName) {
            // Container exists, just start it if stopped
            if ($status == 'stopped') {
                $startCmd = "docker start $containerName 2>&1";
                $startResult = shell_exec($startCmd);
                
                if (strpos($startResult, 'Error') === false) {
                    // Update status and activity
                    $updateSql = "UPDATE containers SET status = 'assigned', last_activity = NOW() WHERE id = ?";
                    $updateStmt = $conn->prepare($updateSql);
                    $updateStmt->bind_param("i", $container['id']);
                    $updateStmt->execute();
                    
                    return ['success' => true, 'port' => $port, 'message' => 'Container restarted'];
                }
            } else {
                // Container already running, just update activity
                $updateSql = "UPDATE containers SET last_activity = NOW() WHERE id = ?";
                $updateStmt = $conn->prepare($updateSql);
                $updateStmt->bind_param("i", $container['id']);
                $updateStmt->execute();
                
                return ['success' => true, 'port' => $port, 'message' => 'Container already running'];
            }
        } else {
            // Container doesn't exist, recreate it
            $createCmd = "docker run -d --name $containerName --restart unless-stopped -p $port:3000 -e NODE_ENV=ctf bkimminich/juice-shop:latest 2>&1";
            $createResult = shell_exec($createCmd);
            
            if (strpos($createResult, 'Error') === false) {
                // Update status and activity
                $updateSql = "UPDATE containers SET status = 'assigned', last_activity = NOW() WHERE id = ?";
                $updateStmt = $conn->prepare($updateSql);
                $updateStmt->bind_param("i", $container['id']);
                $updateStmt->execute();
                
                return ['success' => true, 'port' => $port, 'message' => 'Container recreated'];
            }
        }
    } else {
        // No container assigned, try to assign one
        $assignSql = "SELECT * FROM containers WHERE status = 'available' ORDER BY port LIMIT 1";
        $assignResult = $conn->query($assignSql);
        
        if ($availableContainer = $assignResult->fetch_assoc()) {
            // Assign container to user
            $updateSql = "UPDATE containers SET assigned_to = ?, status = 'assigned', last_activity = NOW() WHERE id = ?";
            $updateStmt = $conn->prepare($updateSql);
            $updateStmt->bind_param("ii", $userId, $availableContainer['id']);
            $updateStmt->execute();
            
            // Start the container
            $containerName = $availableContainer['container_name'];
            $port = $availableContainer['port'];
            
            $startCmd = "docker start $containerName 2>&1";
            $startResult = shell_exec($startCmd);
            
            if (strpos($startResult, 'Error') !== false) {
                // Container doesn't exist, create it
                $createCmd = "docker run -d --name $containerName --restart unless-stopped -p $port:3000 -e NODE_ENV=ctf bkimminich/juice-shop:latest 2>&1";
                shell_exec($createCmd);
            }
            
            return ['success' => true, 'port' => $port, 'message' => 'New container assigned'];
        }
    }
    
    $conn->close();
    return ['success' => false, 'message' => 'No containers available'];
}

// If called directly with user_id parameter
if (isset($_GET['user_id']) || isset($_POST['user_id'])) {
    $userId = $_GET['user_id'] ?? $_POST['user_id'];
    $result = restartUserContainer($userId);
    
    header('Content-Type: application/json');
    echo json_encode($result);
}
?>