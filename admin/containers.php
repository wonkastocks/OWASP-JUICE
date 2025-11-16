<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

$message = '';
$error = '';

// Handle container assignment
if (isset($_POST['assign_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $user_id = intval($_POST['user_id']);
    $port = intval($_POST['port']);
    
    if (assignContainer($user_id, $port)) {
        $message = "Container assigned successfully";
    } else {
        $error = "Failed to assign container";
    }
}

// Handle container release
if (isset($_POST['release_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $port = intval($_POST['port']);
    
    $conn = getDBConnection();
    $stmt = $conn->prepare("UPDATE containers SET user_id = NULL, status = 'available' WHERE port = ?");
    $stmt->bind_param("i", $port);
    
    if ($stmt->execute()) {
        logAdminActivity('release_container', ['port' => $port]);
        $message = "Container released successfully";
    } else {
        $error = "Failed to release container";
    }
    $conn->close();
}

// Handle container restart
if (isset($_POST['restart_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $port = intval($_POST['port']);
    
    $container_name = "juice-user" . ($port - 3000);
    exec("docker restart $container_name 2>&1", $output, $return_var);
    
    if ($return_var === 0) {
        logAdminActivity('restart_container', ['port' => $port]);
        $message = "Container restarted successfully";
    } else {
        $error = "Failed to restart container: " . implode("\n", $output);
    }
}

// Get container status
$containers = getContainerStatus();

// Get available users (those without containers)
$conn = getDBConnection();
$available_users = [];
$result = $conn->query("SELECT u.* FROM users u 
                        LEFT JOIN containers c ON c.user_id = u.id 
                        WHERE c.user_id IS NULL AND u.email_verified = 1 
                        ORDER BY u.username");
while ($row = $result->fetch_assoc()) {
    $available_users[] = $row;
}
$conn->close();

$csrf_token = generateCSRFToken();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Container Management - WonkaTech CTF</title>
    <link rel="stylesheet" href="style.css">
    <script>
        function confirmRestart(containerName) {
            return confirm('Are you sure you want to restart container "' + containerName + '"?');
        }
        
        function confirmRelease(containerName) {
            return confirm('Are you sure you want to release container "' + containerName + '"? The user will lose access to their instance.');
        }
    </script>
</head>
<body>
    <div class="admin-wrapper">
        <!-- Sidebar -->
        <nav class="sidebar">
            <div class="sidebar-header">
                <h2>🍫 WonkaTech Admin</h2>
            </div>
            <ul class="nav-menu">
                <li><a href="index.php">📊 Dashboard</a></li>
                <li><a href="users.php">👥 Users</a></li>
                <li><a href="progress.php">📈 Progress</a></li>
                <li class="active"><a href="containers.php">🐳 Containers</a></li>
                <li><a href="logout.php">🚪 Logout</a></li>
            </ul>
            <div class="sidebar-footer">
                <p>Logged in as:<br><?php echo htmlspecialchars($_SESSION['admin_email']); ?></p>
            </div>
        </nav>
        
        <!-- Main Content -->
        <main class="main-content">
            <header class="content-header">
                <h1>Container Management</h1>
                <p>Manage Docker containers for Juice Shop instances</p>
            </header>
            
            <?php if ($message): ?>
            <div class="alert alert-success"><?php echo htmlspecialchars($message); ?></div>
            <?php endif; ?>
            
            <?php if ($error): ?>
            <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
            <?php endif; ?>
            
            <!-- Container Status -->
            <div class="panel">
                <div class="panel-header">
                    <h2>Container Status</h2>
                </div>
                <div class="panel-body">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Container</th>
                                <th>Port</th>
                                <th>Status</th>
                                <th>Assigned To</th>
                                <th>Email</th>
                                <th>Assigned At</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($containers as $container): ?>
                            <tr>
                                <td>
                                    <strong><?php echo htmlspecialchars($container['container_name']); ?></strong>
                                </td>
                                <td>
                                    <span class="badge badge-info"><?php echo $container['port']; ?></span>
                                </td>
                                <td>
                                    <?php if ($container['status'] === 'assigned'): ?>
                                    <span class="badge badge-success">Assigned</span>
                                    <?php elseif ($container['status'] === 'available'): ?>
                                    <span class="badge badge-warning">Available</span>
                                    <?php else: ?>
                                    <span class="badge badge-danger">Maintenance</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($container['username']): ?>
                                    <a href="progress.php?user_id=<?php echo $container['user_id']; ?>">
                                        <?php echo htmlspecialchars($container['username']); ?>
                                    </a>
                                    <?php else: ?>
                                    <em>-</em>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php echo $container['email'] ? htmlspecialchars($container['email']) : '-'; ?>
                                </td>
                                <td>
                                    <?php echo $container['assigned_at'] ? formatDate($container['assigned_at']) : '-'; ?>
                                </td>
                                <td>
                                    <div style="display: flex; gap: 5px;">
                                        <!-- Restart Button -->
                                        <form method="POST" style="display: inline;" 
                                              onsubmit="return confirmRestart('<?php echo htmlspecialchars($container['container_name']); ?>')">
                                            <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                            <input type="hidden" name="port" value="<?php echo $container['port']; ?>">
                                            <button type="submit" name="restart_container" 
                                                    class="btn btn-sm btn-warning" title="Restart Container">🔄</button>
                                        </form>
                                        
                                        <?php if ($container['status'] === 'assigned'): ?>
                                        <!-- Release Button -->
                                        <form method="POST" style="display: inline;" 
                                              onsubmit="return confirmRelease('<?php echo htmlspecialchars($container['container_name']); ?>')">
                                            <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                            <input type="hidden" name="port" value="<?php echo $container['port']; ?>">
                                            <button type="submit" name="release_container" 
                                                    class="btn btn-sm btn-danger" title="Release Container">🔓</button>
                                        </form>
                                        <?php endif; ?>
                                        
                                        <!-- View Instance -->
                                        <a href="<?php echo JUICE_BASE_URL . ':' . $container['port']; ?>" 
                                           target="_blank" class="btn btn-sm" title="View Instance">🌐</a>
                                    </div>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Assign Container -->
            <?php 
            $available_containers = array_filter($containers, function($c) { 
                return $c['status'] === 'available'; 
            });
            
            if (!empty($available_containers) && !empty($available_users)): 
            ?>
            <div class="panel">
                <div class="panel-header">
                    <h2>Assign Container</h2>
                </div>
                <div class="panel-body">
                    <form method="POST" action="">
                        <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                        
                        <div class="form-group">
                            <label for="user_id">Select User (verified users without containers):</label>
                            <select name="user_id" id="user_id" class="form-control" required>
                                <option value="">-- Select User --</option>
                                <?php foreach ($available_users as $user): ?>
                                <option value="<?php echo $user['id']; ?>">
                                    <?php echo htmlspecialchars($user['username']); ?> 
                                    (<?php echo htmlspecialchars($user['email']); ?>)
                                </option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="port">Select Container:</label>
                            <select name="port" id="port" class="form-control" required>
                                <option value="">-- Select Container --</option>
                                <?php foreach ($available_containers as $container): ?>
                                <option value="<?php echo $container['port']; ?>">
                                    <?php echo htmlspecialchars($container['container_name']); ?> 
                                    (Port <?php echo $container['port']; ?>)
                                </option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                        
                        <button type="submit" name="assign_container" class="btn btn-success">Assign Container</button>
                    </form>
                </div>
            </div>
            <?php endif; ?>
        </main>
    </div>
</body>
</html>