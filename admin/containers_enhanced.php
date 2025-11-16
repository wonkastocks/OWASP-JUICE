<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

$message = '';
$error = '';

// Handle container creation
if (isset($_POST['create_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $port = intval($_POST['port']);
    $container_name = "juice-user" . ($port - 3000);
    
    $conn = getDBConnection();
    
    // Check if port is already in use
    $stmt = $conn->prepare("SELECT id FROM containers WHERE port = ?");
    $stmt->bind_param("i", $port);
    $stmt->execute();
    
    if ($stmt->get_result()->num_rows > 0) {
        $error = "Port $port is already in use";
    } else {
        // Create Docker container
        $cmd = "docker run -d --name $container_name --restart unless-stopped -p $port:3000 -e NODE_ENV=ctf bkimminich/juice-shop:latest 2>&1";
        exec($cmd, $output, $return_var);
        
        if ($return_var === 0) {
            // Get container ID
            exec("docker ps -q -f name=$container_name", $container_id);
            $docker_id = trim($container_id[0] ?? '');
            
            // Add to database
            $stmt = $conn->prepare("INSERT INTO containers (container_name, port, status, docker_container_id, created_at) VALUES (?, ?, 'available', ?, NOW())");
            $stmt->bind_param("sis", $container_name, $port, $docker_id);
            
            if ($stmt->execute()) {
                logAdminActivity('create_container', ['port' => $port, 'name' => $container_name]);
                $message = "Container created successfully on port $port";
            } else {
                $error = "Container created but failed to add to database";
            }
        } else {
            $error = "Failed to create container: " . implode(" ", $output);
        }
    }
    $conn->close();
}

// Handle container deletion
if (isset($_POST['delete_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $container_id = intval($_POST['container_id']);
    
    $conn = getDBConnection();
    
    // Get container details
    $stmt = $conn->prepare("SELECT container_name, port, user_id FROM containers WHERE id = ?");
    $stmt->bind_param("i", $container_id);
    $stmt->execute();
    $result = $stmt->get_result()->fetch_assoc();
    
    if ($result) {
        $container_name = $result['container_name'];
        $port = $result['port'];
        
        // Stop and remove Docker container
        exec("docker stop $container_name 2>&1", $output, $return_var);
        exec("docker rm $container_name 2>&1", $output, $return_var);
        
        // Remove from database
        $stmt = $conn->prepare("DELETE FROM containers WHERE id = ?");
        $stmt->bind_param("i", $container_id);
        
        if ($stmt->execute()) {
            // Clear user assignment if any
            if ($result['user_id']) {
                $stmt = $conn->prepare("UPDATE users SET instance_url = NULL WHERE id = ?");
                $stmt->bind_param("i", $result['user_id']);
                $stmt->execute();
            }
            
            logAdminActivity('delete_container', ['port' => $port, 'name' => $container_name]);
            $message = "Container deleted successfully";
        } else {
            $error = "Failed to delete container from database";
        }
    }
    $conn->close();
}

// Handle container restart
if (isset($_POST['restart_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $container_name = $_POST['container_name'];
    
    exec("docker restart $container_name 2>&1", $output, $return_var);
    
    if ($return_var === 0) {
        logAdminActivity('restart_container', ['name' => $container_name]);
        $message = "Container restarted successfully";
    } else {
        $error = "Failed to restart container: " . implode(" ", $output);
    }
}

// Handle container start
if (isset($_POST['start_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $container_name = $_POST['container_name'];
    
    exec("docker start $container_name 2>&1", $output, $return_var);
    
    if ($return_var === 0) {
        // Update status in database
        $conn = getDBConnection();
        $stmt = $conn->prepare("UPDATE containers SET status = 'available' WHERE container_name = ?");
        $stmt->bind_param("s", $container_name);
        $stmt->execute();
        $conn->close();
        
        logAdminActivity('start_container', ['name' => $container_name]);
        $message = "Container started successfully";
    } else {
        $error = "Failed to start container: " . implode(" ", $output);
    }
}

// Handle container stop
if (isset($_POST['stop_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $container_name = $_POST['container_name'];
    
    exec("docker stop $container_name 2>&1", $output, $return_var);
    
    if ($return_var === 0) {
        // Update status in database
        $conn = getDBConnection();
        $stmt = $conn->prepare("UPDATE containers SET status = 'maintenance' WHERE container_name = ?");
        $stmt->bind_param("s", $container_name);
        $stmt->execute();
        $conn->close();
        
        logAdminActivity('stop_container', ['name' => $container_name]);
        $message = "Container stopped successfully";
    } else {
        $error = "Failed to stop container: " . implode(" ", $output);
    }
}

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

// Get all containers
$containers = getContainerStatus();

// Get Docker container status
exec("docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'", $docker_output);

// Parse Docker status
$docker_status = [];
foreach ($docker_output as $line) {
    if (strpos($line, 'juice-user') !== false) {
        $parts = preg_split('/\s+/', $line, 3);
        if (count($parts) >= 2) {
            $docker_status[$parts[0]] = $parts[1];
        }
    }
}

// Get available users for assignment
$conn = getDBConnection();
$available_users = [];
$result = $conn->query("SELECT u.* FROM users u 
                        LEFT JOIN containers c ON c.user_id = u.id 
                        WHERE c.user_id IS NULL AND u.email_verified = 1 
                        ORDER BY u.username");
while ($row = $result->fetch_assoc()) {
    $available_users[] = $row;
}

// Get port usage
$used_ports = [];
$result = $conn->query("SELECT port FROM containers ORDER BY port");
while ($row = $result->fetch_assoc()) {
    $used_ports[] = $row['port'];
}
$conn->close();

// Find available ports (3001-3020)
$available_ports = [];
for ($p = 3001; $p <= 3020; $p++) {
    if (!in_array($p, $used_ports)) {
        $available_ports[] = $p;
    }
}

$csrf_token = generateCSRFToken();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Container Management - WonkaTech CTF</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .container-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .container-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .container-card h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-running { background: #27ae60; }
        .status-stopped { background: #e74c3c; }
        .status-assigned { background: #3498db; }
        .status-available { background: #f39c12; }
        .container-actions {
            margin-top: 15px;
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        .port-selector {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin: 20px 0;
        }
        .port-box {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            text-align: center;
            cursor: pointer;
        }
        .port-box.used {
            background: #e74c3c;
            color: white;
            cursor: not-allowed;
        }
        .port-box.available {
            background: #27ae60;
            color: white;
        }
        .port-box.available:hover {
            background: #229954;
        }
    </style>
    <script>
        function confirmDelete(containerName) {
            return confirm('Are you sure you want to delete container "' + containerName + '"? This will stop and remove the Docker container.');
        }
        
        function confirmStop(containerName) {
            return confirm('Are you sure you want to stop container "' + containerName + '"?');
        }
        
        function selectPort(port) {
            document.getElementById('new_port').value = port;
            document.querySelectorAll('.port-box').forEach(box => {
                box.style.border = '2px solid #ddd';
            });
            event.target.style.border = '2px solid #2c3e50';
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
                <p>Manage Docker containers for Juice Shop instances (Max: 20 containers)</p>
            </header>
            
            <?php if ($message): ?>
            <div class="alert alert-success"><?php echo htmlspecialchars($message); ?></div>
            <?php endif; ?>
            
            <?php if ($error): ?>
            <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
            <?php endif; ?>
            
            <!-- Container Statistics -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">🐳</div>
                    <div class="stat-details">
                        <h3><?php echo count($containers); ?>/20</h3>
                        <p>Total Containers</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">✅</div>
                    <div class="stat-details">
                        <h3><?php echo count(array_filter($containers, function($c) { return $c['status'] === 'available'; })); ?></h3>
                        <p>Available</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-details">
                        <h3><?php echo count(array_filter($containers, function($c) { return $c['status'] === 'assigned'; })); ?></h3>
                        <p>Assigned</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🔧</div>
                    <div class="stat-details">
                        <h3><?php echo count(array_filter($containers, function($c) { return $c['status'] === 'maintenance'; })); ?></h3>
                        <p>Maintenance</p>
                    </div>
                </div>
            </div>
            
            <!-- Create New Container -->
            <?php if (count($containers) < 20): ?>
            <div class="panel">
                <div class="panel-header">
                    <h2>Create New Container</h2>
                </div>
                <div class="panel-body">
                    <form method="POST" action="">
                        <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                        
                        <div class="form-group">
                            <label>Select Port (Available: <?php echo count($available_ports); ?>)</label>
                            <div class="port-selector">
                                <?php for ($p = 3001; $p <= 3020; $p++): ?>
                                <div class="port-box <?php echo in_array($p, $used_ports) ? 'used' : 'available'; ?>" 
                                     <?php if (!in_array($p, $used_ports)): ?>onclick="selectPort(<?php echo $p; ?>)"<?php endif; ?>>
                                    <?php echo $p; ?>
                                    <?php if (in_array($p, $used_ports)): ?>
                                    <br><small>In Use</small>
                                    <?php endif; ?>
                                </div>
                                <?php endfor; ?>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label for="new_port">Port Number</label>
                            <input type="number" name="port" id="new_port" class="form-control" 
                                   min="3001" max="3020" required placeholder="Select a port above or enter manually">
                        </div>
                        
                        <button type="submit" name="create_container" class="btn btn-success">
                            🚀 Create Container
                        </button>
                    </form>
                </div>
            </div>
            <?php else: ?>
            <div class="alert alert-info">
                Maximum number of containers (20) reached. Delete existing containers to create new ones.
            </div>
            <?php endif; ?>
            
            <!-- Existing Containers -->
            <div class="panel">
                <div class="panel-header">
                    <h2>Container List</h2>
                </div>
                <div class="panel-body">
                    <div class="container-grid">
                        <?php foreach ($containers as $container): ?>
                        <div class="container-card">
                            <h3>
                                <?php 
                                $docker_running = isset($docker_status[$container['container_name']]) && 
                                                 strpos($docker_status[$container['container_name']], 'Up') !== false;
                                ?>
                                <span class="status-indicator status-<?php echo $docker_running ? 'running' : 'stopped'; ?>"></span>
                                <?php echo htmlspecialchars($container['container_name']); ?>
                            </h3>
                            
                            <div style="margin: 10px 0;">
                                <strong>Port:</strong> <?php echo $container['port']; ?><br>
                                <strong>Status:</strong> 
                                <span class="badge badge-<?php 
                                    echo $container['status'] === 'assigned' ? 'success' : 
                                        ($container['status'] === 'available' ? 'warning' : 'danger'); 
                                ?>">
                                    <?php echo ucfirst($container['status']); ?>
                                </span><br>
                                
                                <?php if ($container['username']): ?>
                                <strong>User:</strong> <?php echo htmlspecialchars($container['username']); ?><br>
                                <strong>Email:</strong> <?php echo htmlspecialchars($container['email']); ?><br>
                                <?php endif; ?>
                                
                                <strong>Docker:</strong> 
                                <?php echo $docker_running ? '🟢 Running' : '🔴 Stopped'; ?>
                            </div>
                            
                            <div class="container-actions">
                                <!-- View Instance -->
                                <a href="http://155.138.197.128:<?php echo $container['port']; ?>" 
                                   target="_blank" class="btn btn-sm" title="View Instance">🌐</a>
                                
                                <!-- Start/Stop -->
                                <?php if ($docker_running): ?>
                                <form method="POST" style="display: inline;" 
                                      onsubmit="return confirmStop('<?php echo htmlspecialchars($container['container_name']); ?>')">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="container_name" value="<?php echo $container['container_name']; ?>">
                                    <button type="submit" name="stop_container" class="btn btn-sm btn-warning" title="Stop">⏹️</button>
                                </form>
                                <?php else: ?>
                                <form method="POST" style="display: inline;">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="container_name" value="<?php echo $container['container_name']; ?>">
                                    <button type="submit" name="start_container" class="btn btn-sm btn-success" title="Start">▶️</button>
                                </form>
                                <?php endif; ?>
                                
                                <!-- Restart -->
                                <form method="POST" style="display: inline;">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="container_name" value="<?php echo $container['container_name']; ?>">
                                    <button type="submit" name="restart_container" class="btn btn-sm" title="Restart">🔄</button>
                                </form>
                                
                                <!-- Release if assigned -->
                                <?php if ($container['status'] === 'assigned'): ?>
                                <form method="POST" style="display: inline;">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="port" value="<?php echo $container['port']; ?>">
                                    <button type="submit" name="release_container" class="btn btn-sm btn-warning" title="Release">🔓</button>
                                </form>
                                <?php endif; ?>
                                
                                <!-- Delete -->
                                <form method="POST" style="display: inline;" 
                                      onsubmit="return confirmDelete('<?php echo htmlspecialchars($container['container_name']); ?>')">
                                    <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                    <input type="hidden" name="container_id" value="<?php echo $container['id']; ?>">
                                    <button type="submit" name="delete_container" class="btn btn-sm btn-danger" title="Delete">🗑️</button>
                                </form>
                            </div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                    
                    <?php if (empty($containers)): ?>
                    <p style="text-align: center; padding: 40px; color: #7f8c8d;">
                        No containers exist yet. Create your first container above.
                    </p>
                    <?php endif; ?>
                </div>
            </div>
            
            <!-- Quick Assignment -->
            <?php if (!empty($available_users) && !empty(array_filter($containers, function($c) { return $c['status'] === 'available'; }))): ?>
            <div class="panel">
                <div class="panel-header">
                    <h2>Quick Assignment</h2>
                </div>
                <div class="panel-body">
                    <form method="POST" action="">
                        <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                        
                        <div class="form-group">
                            <label for="user_id">Select User</label>
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
                            <label for="port">Select Container</label>
                            <select name="port" id="port" class="form-control" required>
                                <option value="">-- Select Container --</option>
                                <?php foreach ($containers as $container): ?>
                                    <?php if ($container['status'] === 'available'): ?>
                                    <option value="<?php echo $container['port']; ?>">
                                        <?php echo htmlspecialchars($container['container_name']); ?> 
                                        (Port <?php echo $container['port']; ?>)
                                    </option>
                                    <?php endif; ?>
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