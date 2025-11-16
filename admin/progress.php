<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

// Get user ID from query parameter
$user_id = isset($_GET['user_id']) ? intval($_GET['user_id']) : 0;

// Get all users for dropdown
$all_users = getAllUsers();

// Get progress for selected user
$progress = [];
$selected_user = null;

if ($user_id > 0) {
    $progress = getUserProgress($user_id);
    
    // Find selected user details
    foreach ($all_users as $user) {
        if ($user['id'] == $user_id) {
            $selected_user = $user;
            break;
        }
    }
}

// Group progress by category
$categories = [];
if (!empty($progress)) {
    foreach ($progress as $item) {
        $category = $item['challenge_category'] ?? 'Uncategorized';
        if (!isset($categories[$category])) {
            $categories[$category] = [];
        }
        $categories[$category][] = $item;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Progress - WonkaTech CTF</title>
    <link rel="stylesheet" href="style.css">
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
                <li class="active"><a href="progress.php">📈 Progress</a></li>
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
                <h1>User Progress Tracking</h1>
                <p>View detailed challenge completion for each user</p>
            </header>
            
            <!-- User Selection -->
            <div class="panel">
                <div class="panel-body">
                    <form method="GET" action="">
                        <div class="form-group">
                            <label for="user_id">Select User:</label>
                            <select name="user_id" id="user_id" class="form-control" onchange="this.form.submit()">
                                <option value="">-- Select a user --</option>
                                <?php foreach ($all_users as $user): ?>
                                <option value="<?php echo $user['id']; ?>" <?php echo $user_id == $user['id'] ? 'selected' : ''; ?>>
                                    <?php echo htmlspecialchars($user['username']); ?> 
                                    (<?php echo htmlspecialchars($user['email']); ?>)
                                </option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    </form>
                </div>
            </div>
            
            <?php if ($selected_user): ?>
            <!-- User Summary -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">👤</div>
                    <div class="stat-details">
                        <h3><?php echo htmlspecialchars($selected_user['username']); ?></h3>
                        <p>Username</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🏆</div>
                    <div class="stat-details">
                        <h3><?php echo $selected_user['total_score'] ?? 0; ?></h3>
                        <p>Total Score</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">✅</div>
                    <div class="stat-details">
                        <h3><?php echo count($progress); ?></h3>
                        <p>Challenges Completed</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🐳</div>
                    <div class="stat-details">
                        <h3><?php echo $selected_user['container_port'] ? 'Port ' . $selected_user['container_port'] : 'None'; ?></h3>
                        <p>Container</p>
                    </div>
                </div>
            </div>
            
            <!-- Progress by Category -->
            <?php if (!empty($categories)): ?>
                <?php foreach ($categories as $category => $challenges): ?>
                <div class="panel">
                    <div class="panel-header">
                        <h2><?php echo htmlspecialchars($category); ?> (<?php echo count($challenges); ?> completed)</h2>
                    </div>
                    <div class="panel-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Challenge Name</th>
                                    <th>Points</th>
                                    <th>Completed At</th>
                                    <th>Time Taken</th>
                                    <th>Hints Used</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($challenges as $challenge): ?>
                                <tr>
                                    <td><?php echo htmlspecialchars($challenge['challenge_name']); ?></td>
                                    <td><?php echo $challenge['points']; ?></td>
                                    <td><?php echo formatDate($challenge['completed_at']); ?></td>
                                    <td>
                                        <?php 
                                        if ($challenge['time_taken']) {
                                            echo round($challenge['time_taken'] / 60) . ' min';
                                        } else {
                                            echo '-';
                                        }
                                        ?>
                                    </td>
                                    <td><?php echo $challenge['hints_used']; ?></td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                </div>
                <?php endforeach; ?>
            <?php else: ?>
                <div class="panel">
                    <div class="panel-body">
                        <p style="text-align: center; padding: 40px; color: #7f8c8d;">
                            No challenges completed yet by this user.
                        </p>
                    </div>
                </div>
            <?php endif; ?>
            
            <?php elseif ($user_id > 0): ?>
            <div class="alert alert-danger">
                User not found.
            </div>
            <?php else: ?>
            <div class="panel">
                <div class="panel-body">
                    <p style="text-align: center; padding: 40px; color: #7f8c8d;">
                        Please select a user to view their progress.
                    </p>
                </div>
            </div>
            <?php endif; ?>
        </main>
    </div>
</body>
</html>