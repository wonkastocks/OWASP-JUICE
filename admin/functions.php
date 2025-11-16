<?php
require_once 'config.php';

// Format date for display
function formatDate($date) {
    return date('M d, Y H:i', strtotime($date));
}

// Get user statistics
function getUserStats() {
    $conn = getDBConnection();
    $stats = [];
    
    // Total users
    $result = $conn->query("SELECT COUNT(*) as total FROM users");
    $stats['total_users'] = $result->fetch_assoc()['total'];
    
    // Verified users
    $result = $conn->query("SELECT COUNT(*) as verified FROM users WHERE email_verified = 1");
    $stats['verified_users'] = $result->fetch_assoc()['verified'];
    
    // Active users (logged in last 7 days)
    $result = $conn->query("SELECT COUNT(*) as active FROM users WHERE last_login > DATE_SUB(NOW(), INTERVAL 7 DAY)");
    $stats['active_users'] = $result->fetch_assoc()['active'];
    
    // Total challenges completed
    $result = $conn->query("SELECT COUNT(*) as completed FROM challenge_progress");
    $stats['challenges_completed'] = $result->fetch_assoc()['completed'];
    
    $conn->close();
    return $stats;
}

// Get container status
function getContainerStatus() {
    $conn = getDBConnection();
    $containers = [];
    
    $sql = "SELECT c.*, u.username, u.email 
            FROM containers c 
            LEFT JOIN users u ON c.user_id = u.id 
            ORDER BY c.port";
    $result = $conn->query($sql);
    
    while ($row = $result->fetch_assoc()) {
        $containers[] = $row;
    }
    
    $conn->close();
    return $containers;
}

// Delete user and all related data
function deleteUser($user_id) {
    $conn = getDBConnection();
    
    // Start transaction
    $conn->begin_transaction();
    
    try {
        // Free up container if assigned
        $stmt = $conn->prepare("UPDATE containers SET user_id = NULL, status = 'available' WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        
        // Delete user (cascade will handle related tables)
        $stmt = $conn->prepare("DELETE FROM users WHERE id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        
        // Commit transaction
        $conn->commit();
        
        logAdminActivity('delete_user', ['user_id' => $user_id]);
        return true;
    } catch (Exception $e) {
        $conn->rollback();
        error_log("Error deleting user: " . $e->getMessage());
        return false;
    } finally {
        $conn->close();
    }
}

// Reset user scoreboard
function resetUserScoreboard($user_id) {
    $conn = getDBConnection();
    
    $conn->begin_transaction();
    
    try {
        // Delete challenge progress
        $stmt = $conn->prepare("DELETE FROM challenge_progress WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        
        // Reset scores
        $stmt = $conn->prepare("UPDATE scores SET total_score = 0, challenges_completed = 0 WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        
        // Get user's container port
        $stmt = $conn->prepare("SELECT c.port FROM containers c WHERE c.user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($row = $result->fetch_assoc()) {
            // Call Juice Shop API to reset (if needed)
            $port = $row['port'];
            resetJuiceShopInstance($port);
        }
        
        $conn->commit();
        logAdminActivity('reset_scoreboard', ['user_id' => $user_id]);
        return true;
    } catch (Exception $e) {
        $conn->rollback();
        error_log("Error resetting scoreboard: " . $e->getMessage());
        return false;
    } finally {
        $conn->close();
    }
}

// Reset Juice Shop instance via API
function resetJuiceShopInstance($port) {
    // This would typically call the Juice Shop admin API to reset
    // For now, we'll just restart the container
    $container_name = "juice-user" . ($port - 3000);
    exec("docker restart $container_name 2>&1", $output, $return_var);
    return $return_var === 0;
}

// Get user progress
function getUserProgress($user_id) {
    $conn = getDBConnection();
    $progress = [];
    
    $stmt = $conn->prepare("
        SELECT cp.*, u.username, u.email 
        FROM challenge_progress cp
        JOIN users u ON cp.user_id = u.id
        WHERE cp.user_id = ?
        ORDER BY cp.completed_at DESC
    ");
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $result = $stmt->get_result();
    
    while ($row = $result->fetch_assoc()) {
        $progress[] = $row;
    }
    
    $conn->close();
    return $progress;
}

// Get all users with their stats
function getAllUsers($search = '', $sort = 'created_at', $order = 'DESC') {
    $conn = getDBConnection();
    $users = [];
    
    $allowed_sorts = ['id', 'username', 'email', 'created_at', 'last_login', 'email_verified'];
    $allowed_orders = ['ASC', 'DESC'];
    
    if (!in_array($sort, $allowed_sorts)) $sort = 'created_at';
    if (!in_array($order, $allowed_orders)) $order = 'DESC';
    
    $sql = "SELECT u.*, 
            c.port as container_port,
            c.status as container_status,
            s.total_score,
            s.challenges_completed
            FROM users u
            LEFT JOIN containers c ON c.user_id = u.id
            LEFT JOIN scores s ON s.user_id = u.id";
    
    if ($search) {
        $sql .= " WHERE u.username LIKE ? OR u.email LIKE ?";
    }
    
    $sql .= " ORDER BY u.$sort $order";
    
    if ($search) {
        $stmt = $conn->prepare($sql);
        $search_param = "%$search%";
        $stmt->bind_param("ss", $search_param, $search_param);
        $stmt->execute();
        $result = $stmt->get_result();
    } else {
        $result = $conn->query($sql);
    }
    
    while ($row = $result->fetch_assoc()) {
        $users[] = $row;
    }
    
    $conn->close();
    return $users;
}

// Assign container to user
function assignContainer($user_id, $port) {
    $conn = getDBConnection();
    
    $conn->begin_transaction();
    
    try {
        // Free any existing container for this user
        $stmt = $conn->prepare("UPDATE containers SET user_id = NULL, status = 'available' WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        $stmt->execute();
        
        // Assign new container
        $stmt = $conn->prepare("UPDATE containers SET user_id = ?, status = 'assigned', assigned_at = NOW() WHERE port = ?");
        $stmt->bind_param("ii", $user_id, $port);
        $stmt->execute();
        
        // Update user's instance URL
        $instance_url = JUICE_BASE_URL . ":$port";
        $stmt = $conn->prepare("UPDATE users SET instance_url = ? WHERE id = ?");
        $stmt->bind_param("si", $instance_url, $user_id);
        $stmt->execute();
        
        $conn->commit();
        logAdminActivity('assign_container', ['user_id' => $user_id, 'port' => $port]);
        return true;
    } catch (Exception $e) {
        $conn->rollback();
        error_log("Error assigning container: " . $e->getMessage());
        return false;
    } finally {
        $conn->close();
    }
}

// Get challenge statistics
function getChallengeStats() {
    $conn = getDBConnection();
    $stats = [];
    
    $sql = "SELECT challenge_name, challenge_category, COUNT(*) as completion_count,
            AVG(points) as avg_points, AVG(time_taken) as avg_time
            FROM challenge_progress
            GROUP BY challenge_name, challenge_category
            ORDER BY completion_count DESC
            LIMIT 10";
    
    $result = $conn->query($sql);
    
    while ($row = $result->fetch_assoc()) {
        $stats[] = $row;
    }
    
    $conn->close();
    return $stats;
}

// Export users to CSV
function exportUsersToCSV() {
    $users = getAllUsers();
    
    $filename = "wonkatech_users_" . date('Y-m-d_H-i-s') . ".csv";
    
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="' . $filename . '"');
    
    $output = fopen('php://output', 'w');
    
    // Header row
    fputcsv($output, ['ID', 'Username', 'Email', 'Verified', 'Created', 'Last Login', 'Container Port', 'Score', 'Challenges']);
    
    // Data rows
    foreach ($users as $user) {
        fputcsv($output, [
            $user['id'],
            $user['username'],
            $user['email'],
            $user['email_verified'] ? 'Yes' : 'No',
            $user['created_at'],
            $user['last_login'] ?? 'Never',
            $user['container_port'] ?? 'None',
            $user['total_score'] ?? 0,
            $user['challenges_completed'] ?? 0
        ]);
    }
    
    fclose($output);
    exit();
}
?>