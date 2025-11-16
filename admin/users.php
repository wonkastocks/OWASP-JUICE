<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

$message = '';
$error = '';

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

$csrf_token = generateCSRFToken();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Management - WonkaTech CTF</title>
    <link rel="stylesheet" href="style.css">
    <script>
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
                        <a href="users.php?export=1" class="btn btn-success">📥 Export CSV</a>
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
                                <th><a href="?sort=id&order=<?php echo $order === 'ASC' ? 'DESC' : 'ASC'; ?>">ID</a></th>
                                <th><a href="?sort=username&order=<?php echo $order === 'ASC' ? 'DESC' : 'ASC'; ?>">Username</a></th>
                                <th><a href="?sort=email&order=<?php echo $order === 'ASC' ? 'DESC' : 'ASC'; ?>">Email</a></th>
                                <th>Verified</th>
                                <th>Container</th>
                                <th>Score</th>
                                <th>Challenges</th>
                                <th><a href="?sort=created_at&order=<?php echo $order === 'ASC' ? 'DESC' : 'ASC'; ?>">Registered</a></th>
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
                                    <div style="display: flex; gap: 5px;">
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
</body>
</html>