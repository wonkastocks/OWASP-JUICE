<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

// Get container status
function getContainerStatus() {
    $containers = [];

    // Check each juice-user container (1-20)
    for ($i = 1; $i <= 20; $i++) {
        $containerName = "juice-user$i";
        $port = 3000 + $i;

        // Check if container is running
        $output = shell_exec("docker ps -q -f name=$containerName 2>/dev/null");
        $isRunning = !empty(trim($output));

        // Get container stats if running
        if ($isRunning) {
            // Get last activity from logs
            $lastActivity = shell_exec("docker logs --tail 10 $containerName 2>/dev/null | grep -E '(GET|POST)' | tail -1 | awk '{print $1, $2}'");

            // Get container uptime
            $startTime = shell_exec("docker inspect $containerName --format='{{.State.StartedAt}}' 2>/dev/null");

            // Get memory usage
            $stats = shell_exec("docker stats $containerName --no-stream --format 'table {{.MemUsage}}' 2>/dev/null | tail -1");
        } else {
            $lastActivity = "Container not running";
            $startTime = "N/A";
            $stats = "N/A";
        }

        $containers[] = [
            'name' => $containerName,
            'port' => $port,
            'running' => $isRunning,
            'last_activity' => trim($lastActivity) ?: 'No recent activity',
            'started' => trim($startTime),
            'memory' => trim($stats) ?: 'N/A',
            'url' => "https://juice$i.wonkatech.org"
        ];
    }

    return $containers;
}

$containers = getContainerStatus();
$totalContainers = count($containers);
$runningContainers = count(array_filter($containers, fn($c) => $c['running']));
$stoppedContainers = $totalContainers - $runningContainers;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Container Monitor - Juice Shop Admin</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .monitor-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .stat-number.running { color: #28a745; }
        .stat-number.stopped { color: #dc3545; }
        .stat-number.total { color: #007bff; }

        .container-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }

        .container-card {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .container-card.running {
            border-left: 4px solid #28a745;
        }

        .container-card.stopped {
            border-left: 4px solid #dc3545;
        }

        .container-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .container-name {
            font-size: 1.2rem;
            font-weight: bold;
        }

        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-badge.running {
            background: #d4edda;
            color: #155724;
        }

        .status-badge.stopped {
            background: #f8d7da;
            color: #721c24;
        }

        .container-details {
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .refresh-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
        }

        .refresh-btn:hover {
            background: #0056b3;
        }

        .auto-refresh {
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="monitor-header">
            <h1>🐳 Container Monitor</h1>
            <p>Real-time monitoring of Juice Shop container instances</p>
            <div class="auto-refresh">
                Auto-refreshing every 30 seconds | Last updated: <?php echo date('Y-m-d H:i:s'); ?>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number running"><?php echo $runningContainers; ?></div>
                <div>Running Containers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stopped"><?php echo $stoppedContainers; ?></div>
                <div>Stopped Containers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number total"><?php echo $totalContainers; ?></div>
                <div>Total Containers</div>
            </div>
        </div>

        <div class="container-grid">
            <?php foreach ($containers as $container): ?>
                <div class="container-card <?php echo $container['running'] ? 'running' : 'stopped'; ?>">
                    <div class="container-header">
                        <div class="container-name"><?php echo htmlspecialchars($container['name']); ?></div>
                        <div class="status-badge <?php echo $container['running'] ? 'running' : 'stopped'; ?>">
                            <?php echo $container['running'] ? 'Running' : 'Stopped'; ?>
                        </div>
                    </div>

                    <div class="container-details">
                        <strong>Port:</strong> <?php echo $container['port']; ?><br>

                        <?php if ($container['running']): ?>
                            <strong>URL:</strong> <a href="<?php echo $container['url']; ?>" target="_blank"><?php echo $container['url']; ?></a><br>
                            <strong>Last Activity:</strong> <?php echo htmlspecialchars($container['last_activity']); ?><br>
                            <strong>Memory Usage:</strong> <?php echo htmlspecialchars($container['memory']); ?><br>
                            <strong>Started:</strong> <?php echo htmlspecialchars(substr($container['started'], 0, 19)); ?>
                        <?php else: ?>
                            <strong>Status:</strong> <span style="color: #dc3545;">Container not running</span><br>
                            <button onclick="startContainer('<?php echo $container['name']; ?>')" class="refresh-btn" style="margin-top: 10px;">
                                Start Container
                            </button>
                        <?php endif; ?>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <button onclick="location.reload()" class="refresh-btn">🔄 Refresh Now</button>
            <a href="index.php" class="refresh-btn" style="text-decoration: none; margin-left: 10px;">← Back to Dashboard</a>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {
            location.reload();
        }, 30000);

        // Start container function
        function startContainer(containerName) {
            if (confirm(`Start container ${containerName}?`)) {
                fetch('', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `action=start_container&container=${containerName}&csrf_token=<?php echo generateCSRFToken(); ?>`
                }).then(() => {
                    location.reload();
                });
            }
        }
    </script>
</body>
</html>

<?php
// Handle container start requests
if (isset($_POST['action']) && $_POST['action'] === 'start_container') {
    verifyCSRFToken($_POST['csrf_token'] ?? '');
    $containerName = $_POST['container'] ?? '';

    if (preg_match('/^juice-user\d+$/', $containerName)) {
        $result = shell_exec("docker start $containerName 2>&1");
        error_log("Started container $containerName: $result");
    }
}
?>