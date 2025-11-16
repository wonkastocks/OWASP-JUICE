<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

$message = '';
$error = '';

// Handle user creation
if (isset($_POST['create_user'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    
    $username = trim($_POST['username']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    
    $conn = getDBConnection();
    
    // Check if email already exists
    $stmt = $conn->prepare("SELECT id FROM users WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    if ($stmt->get_result()->num_rows > 0) {
        $error = "Email already exists";
    } else {
        // Create new user
        $password_hash = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $conn->prepare("INSERT INTO users (username, email, password_hash, email_verified, created_at) VALUES (?, ?, ?, 1, NOW())");
        $stmt->bind_param("sss", $username, $email, $password_hash);
        
        if ($stmt->execute()) {
            $user_id = $conn->insert_id;
            
            // Initialize score record
            $stmt = $conn->prepare("INSERT INTO scores (user_id, total_score, challenges_completed) VALUES (?, 0, 0)");
            $stmt->bind_param("i", $user_id);
            $stmt->execute();
            
            logAdminActivity('create_user', ['username' => $username, 'email' => $email]);
            $message = "User created successfully";
        } else {
            $error = "Failed to create user";
        }
    }
    $conn->close();
}

// Handle user editing
if (isset($_POST['edit_user'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    
    $user_id = intval($_POST['user_id']);
    $username = trim($_POST['username']);
    $email = trim($_POST['email']);
    $email_verified = isset($_POST['email_verified']) ? 1 : 0;
    
    $conn = getDBConnection();
    $stmt = $conn->prepare("UPDATE users SET username = ?, email = ?, email_verified = ? WHERE id = ?");
    $stmt->bind_param("ssii", $username, $email, $email_verified, $user_id);
    
    if ($stmt->execute()) {
        logAdminActivity('edit_user', ['user_id' => $user_id, 'username' => $username]);
        $message = "User updated successfully";
    } else {
        $error = "Failed to update user";
    }
    $conn->close();
}

// Handle password reset
if (isset($_POST['reset_password'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    
    $user_id = intval($_POST['user_id']);
    $new_password = $_POST['new_password'];
    
    $conn = getDBConnection();
    $password_hash = password_hash($new_password, PASSWORD_DEFAULT);
    $stmt = $conn->prepare("UPDATE users SET password_hash = ? WHERE id = ?");
    $stmt->bind_param("si", $password_hash, $user_id);
    
    if ($stmt->execute()) {
        logAdminActivity('reset_password', ['user_id' => $user_id]);
        $message = "Password reset successfully";
    } else {
        $error = "Failed to reset password";
    }
    $conn->close();
}

// Handle user deletion
if (isset($_POST['delete_user'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $user_id = intval($_POST['user_id']);
    
    if (deleteUser($user_id)) {
        $message = "User deleted successfully";
    } else {
        $error = "Failed to delete user";
    }
}

// Handle scoreboard reset
if (isset($_POST['reset_scoreboard'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $user_id = intval($_POST['user_id']);
    
    if (resetUserScoreboard($user_id)) {
        $message = "Scoreboard reset successfully";
    } else {
        $error = "Failed to reset scoreboard";
    }
}

// Handle container assignment
if (isset($_POST['assign_container'])) {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $user_id = intval($_POST['user_id']);
    $port = intval($_POST['container_port']);
    
    if ($port > 0) {
        if (assignContainer($user_id, $port)) {
            $message = "Container assigned successfully";
        } else {
            $error = "Failed to assign container";
        }
    } else {
        // Remove container assignment
        $conn = getDBConnection();
        $stmt = $conn->prepare("UPDATE containers SET user_id = NULL, status = 'available' WHERE user_id = ?");
        $stmt->bind_param("i", $user_id);
        if ($stmt->execute()) {
            $stmt = $conn->prepare("UPDATE users SET instance_url = NULL WHERE id = ?");
            $stmt->bind_param("i", $user_id);
            $stmt->execute();
            $message = "Container unassigned";
        }
        $conn->close();
    }
}

// Handle CSV export
if (isset($_GET['export'])) {
    exportUsersToCSV();
}

// Get search and sort parameters
$search = $_GET['search'] ?? '';
$sort = $_GET['sort'] ?? 'created_at';
$order = $_GET['order'] ?? 'DESC';

// Get all users
$users = getAllUsers($search, $sort, $order);

// Get available containers
$conn = getDBConnection();
$available_containers = [];
$result = $conn->query("SELECT * FROM containers WHERE status = 'available' ORDER BY port");
while ($row = $result->fetch_assoc()) {
    $available_containers[] = $row;
}
$conn->close();

$csrf_token = generateCSRFToken();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management - WonkaTech CTF</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        .modal.active {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            width: 500px;
            max-width: 90%;
        }
        .modal-header {
            margin-bottom: 20px;
        }
        .modal-header h2 {
            margin: 0;
        }
        .close {
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .close:hover {
            color: #667eea;
        }
    </style>
    <script>
        function showModal(modalId) {
            document.getElementById(modalId).classList.add('active');
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }
        
        function editUser(id, username, email, verified) {
            document.getElementById('edit_user_id').value = id;
            document.getElementById('edit_username').value = username;
            document.getElementById('edit_email').value = email;
            document.getElementById('edit_verified').checked = verified == 1;
            showModal('editModal');
        }
        
        function resetPassword(id, username) {
            document.getElementById('reset_user_id').value = id;
            document.getElementById('reset_username').textContent = username;
            showModal('resetModal');
        }
        
        function assignContainerModal(id, username, currentPort) {
            document.getElementById('assign_user_id').value = id;
            document.getElementById('assign_username').textContent = username;
            document.getElementById('container_select').value = currentPort || '';
            showModal('containerModal');
        }
        
        function confirmDelete(username) {
            return confirm('Are you sure you want to delete user "' + username + '"? This action cannot be undone.');
        }
        
        function confirmReset(username) {
            return confirm('Are you sure you want to reset the scoreboard for user "' + username + '"? All their challenge progress will be lost.');
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
                <li class="active"><a href="users.php">👥 Users</a></li>
                <li><a href="progress.php">📈 Progress</a></li>
                <li><a href="containers.php">🐳 Containers</a></li>
                <li><a href="logout.php">🚪 Logout</a></li>
            </ul>
            <div class="sidebar-footer">
                <p>Logged in as:<br><?php echo htmlspecialchars($_SESSION['admin_email']); ?></p>
            </div>
        </nav>
        
        <!-- Main Content -->
        <main class="main-content">
            <header class="content-header">
                <h1>User Management</h1>
                <p>Manage registered users and their progress</p>
            </header>
            
            <?php if ($message): ?>
            <div class="alert alert-success"><?php echo htmlspecialchars($message); ?></div>
            <?php endif; ?>
            
            <?php if ($error): ?>
            <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
            <?php endif; ?>
            
            <!-- Search and Actions -->
            <div class="panel">
                <div class="panel-body">
                    <div class="action-buttons">
                        <form method="GET" action="" class="search-bar">
                            <input type="text" name="search" placeholder="Search by username or email..." 
                                   value="<?php echo htmlspecialchars($search); ?>" class="form-control">
                            <button type="submit" class="btn">Search</button>
                            <?php if ($search): ?>
                            <a href="users.php" class="btn">Clear</a>
                            <?php endif; ?>
                        </form>
                        <div>
                            <button onclick="showModal('createModal')" class="btn btn-success">➕ Add User</button>
                            <a href="users.php?export=1" class="btn">📥 Export CSV</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Users Table -->
            <div class="panel">
                <div class="panel-header">
                    <h2>Registered Users (<?php echo count($users); ?>)</h2>
                </div>
                <div class="panel-body">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Verified</th>
                                <th>Container</th>
                                <th>Score</th>
                                <th>Challenges</th>
                                <th>Created</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($users as $user): ?>
                            <tr>
                                <td><?php echo $user['id']; ?></td>
                                <td><?php echo htmlspecialchars($user['username']); ?></td>
                                <td><?php echo htmlspecialchars($user['email']); ?></td>
                                <td>
                                    <?php if ($user['email_verified']): ?>
                                    <span class="badge badge-success">Yes</span>
                                    <?php else: ?>
                                    <span class="badge badge-warning">No</span>
                                    <?php endif; ?>
                                </td>
                                <td>
                                    <?php if ($user['container_port']): ?>
                                    <span class="badge badge-info">Port <?php echo $user['container_port']; ?></span>
                                    <?php else: ?>
                                    <span class="badge badge-warning">None</span>
                                    <?php endif; ?>
                                </td>
                                <td><?php echo $user['total_score'] ?? 0; ?></td>
                                <td><?php echo $user['challenges_completed'] ?? 0; ?></td>
                                <td><?php echo formatDate($user['created_at']); ?></td>
                                <td>
                                    <div style="display: flex; gap: 5px; flex-wrap: wrap;">
                                        <button onclick="editUser(<?php echo $user['id']; ?>, '<?php echo addslashes($user['username']); ?>', '<?php echo addslashes($user['email']); ?>', <?php echo $user['email_verified']; ?>)" 
                                                class="btn btn-sm" title="Edit User">✏️</button>
                                        
                                        <button onclick="resetPassword(<?php echo $user['id']; ?>, '<?php echo addslashes($user['username']); ?>')" 
                                                class="btn btn-sm btn-warning" title="Reset Password">🔑</button>
                                        
                                        <button onclick="assignContainerModal(<?php echo $user['id']; ?>, '<?php echo addslashes($user['username']); ?>', '<?php echo $user['container_port'] ?? ''; ?>')" 
                                                class="btn btn-sm" title="Manage Container">🐳</button>
                                        
                                        <a href="progress.php?user_id=<?php echo $user['id']; ?>" 
                                           class="btn btn-sm" title="View Progress">📊</a>
                                        
                                        <form method="POST" style="display: inline;" 
                                              onsubmit="return confirmReset('<?php echo htmlspecialchars($user['username']); ?>')">
                                            <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                            <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                                            <button type="submit" name="reset_scoreboard" 
                                                    class="btn btn-sm btn-warning" title="Reset Scoreboard">🔄</button>
                                        </form>
                                        
                                        <form method="POST" style="display: inline;" 
                                              onsubmit="return confirmDelete('<?php echo htmlspecialchars($user['username']); ?>')">
                                            <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                                            <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                                            <button type="submit" name="delete_user" 
                                                    class="btn btn-sm btn-danger" title="Delete User">🗑️</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                    
                    <?php if (empty($users)): ?>
                    <p style="text-align: center; padding: 20px; color: #7f8c8d;">
                        No users found<?php echo $search ? ' matching your search' : ''; ?>
                    </p>
                    <?php endif; ?>
                </div>
            </div>
        </main>
    </div>
    
    <!-- Create User Modal -->
    <div id="createModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('createModal')">&times;</span>
                <h2>Create New User</h2>
            </div>
            <form method="POST" action="">
                <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" name="username" id="username" class="form-control" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" name="email" id="email" class="form-control" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" class="form-control" required>
                </div>
                
                <div class="modal-footer">
                    <button type="button" onclick="closeModal('createModal')" class="btn">Cancel</button>
                    <button type="submit" name="create_user" class="btn btn-success">Create User</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Edit User Modal -->
    <div id="editModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('editModal')">&times;</span>
                <h2>Edit User</h2>
            </div>
            <form method="POST" action="">
                <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                <input type="hidden" name="user_id" id="edit_user_id">
                
                <div class="form-group">
                    <label for="edit_username">Username</label>
                    <input type="text" name="username" id="edit_username" class="form-control" required>
                </div>
                
                <div class="form-group">
                    <label for="edit_email">Email</label>
                    <input type="email" name="email" id="edit_email" class="form-control" required>
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="email_verified" id="edit_verified">
                        Email Verified
                    </label>
                </div>
                
                <div class="modal-footer">
                    <button type="button" onclick="closeModal('editModal')" class="btn">Cancel</button>
                    <button type="submit" name="edit_user" class="btn btn-success">Save Changes</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Reset Password Modal -->
    <div id="resetModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('resetModal')">&times;</span>
                <h2>Reset Password</h2>
            </div>
            <form method="POST" action="">
                <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                <input type="hidden" name="user_id" id="reset_user_id">
                
                <p>Reset password for user: <strong id="reset_username"></strong></p>
                
                <div class="form-group">
                    <label for="new_password">New Password</label>
                    <input type="password" name="new_password" id="new_password" class="form-control" required>
                </div>
                
                <div class="modal-footer">
                    <button type="button" onclick="closeModal('resetModal')" class="btn">Cancel</button>
                    <button type="submit" name="reset_password" class="btn btn-warning">Reset Password</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Container Assignment Modal -->
    <div id="containerModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal('containerModal')">&times;</span>
                <h2>Manage Container</h2>
            </div>
            <form method="POST" action="">
                <input type="hidden" name="csrf_token" value="<?php echo $csrf_token; ?>">
                <input type="hidden" name="user_id" id="assign_user_id">
                
                <p>Assign container for user: <strong id="assign_username"></strong></p>
                
                <div class="form-group">
                    <label for="container_select">Container</label>
                    <select name="container_port" id="container_select" class="form-control">
                        <option value="">-- Unassign Container --</option>
                        <?php for ($port = 3001; $port <= 3005; $port++): ?>
                        <option value="<?php echo $port; ?>">Port <?php echo $port; ?></option>
                        <?php endfor; ?>
                    </select>
                </div>
                
                <div class="modal-footer">
                    <button type="button" onclick="closeModal('containerModal')" class="btn">Cancel</button>
                    <button type="submit" name="assign_container" class="btn btn-success">Update Container</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>