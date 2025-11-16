<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

// Get statistics
$stats = getUserStats();
$containers = getContainerStatus();
$challenge_stats = getChallengeStats();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - WonkaTech CTF</title>
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
                <li class="active"><a href="index.php">📊 Dashboard</a></li>
                <li><a href="users.php">👥 Users</a></li>
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
                <h1>Dashboard</h1>
                <p>Welcome to WonkaTech CTF Admin Panel</p>
            </header>
            
            <!-- Statistics Cards -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-details">
                        <h3><?php echo $stats['total_users']; ?></h3>
                        <p>Total Users</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">✅</div>
                    <div class="stat-details">
                        <h3><?php echo $stats['verified_users']; ?></h3>
                        <p>Verified Users</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🎯</div>
                    <div class="stat-details">
                        <h3><?php echo $stats['active_users']; ?></h3>
                        <p>Active (7 days)</p>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🏆</div>
                    <div class="stat-details">
                        <h3><?php echo $stats['challenges_completed']; ?></h3>
                        <p>Challenges Completed</p>
                    </div>
                </div>
            </div>
            
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
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($containers as $container): ?>
                            <tr>
                                <td><?php echo htmlspecialchars($container['container_name']); ?></td>
                                <td><?php echo $container['port']; ?></td>
                                <td>
                                    <span class="badge badge-<?php echo $container['status'] === 'assigned' ? 'success' : 'warning'; ?>">
                                        <?php echo ucfirst($container['status']); ?>
                                    </span>
                                </td>
                                <td><?php echo $container['username'] ?? '-'; ?></td>
                                <td>
                                    <a href="containers.php?id=<?php echo $container['id']; ?>" class="btn btn-sm">Manage</a>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Top Challenges -->
            <div class="panel">
                <div class="panel-header">
                    <h2>Popular Challenges</h2>
                </div>
                <div class="panel-body">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Challenge</th>
                                <th>Category</th>
                                <th>Completions</th>
                                <th>Avg Points</th>
                                <th>Avg Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($challenge_stats as $challenge): ?>
                            <tr>
                                <td><?php echo htmlspecialchars($challenge['challenge_name']); ?></td>
                                <td><?php echo htmlspecialchars($challenge['challenge_category'] ?? 'Unknown'); ?></td>
                                <td><?php echo $challenge['completion_count']; ?></td>
                                <td><?php echo round($challenge['avg_points']); ?></td>
                                <td><?php echo $challenge['avg_time'] ? round($challenge['avg_time'] / 60) . ' min' : '-'; ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>
</body>
</html>