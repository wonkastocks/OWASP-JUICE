<?php
require_once 'config.php';
require_once 'functions.php';

// Check admin authentication
checkAdminAuth();

// Get container status with proper null handling
function getDetailedContainerStatus() {
    $containers = [];

    // Check each juice-user container (1-20)
    for ($i = 1; $i <= 20; $i++) {
        $containerName = "juice-user$i";
        $port = 3000 + $i;

        // Check if container is running
        $output = shell_exec("docker ps -q -f name=$containerName 2>/dev/null");
        $isRunning = !empty($output) && !empty(trim($output));

        // Get container stats if running
        if ($isRunning) {
            // Get last activity from logs
            $lastActivityRaw = shell_exec("docker logs --tail 10 $containerName 2>/dev/null | grep -E '(GET|POST)' | tail -1 | awk '{print \$1, \$2}' 2>/dev/null");
            $lastActivity = $lastActivityRaw ? trim($lastActivityRaw) : '';

            // Get container uptime
            $startTimeRaw = shell_exec("docker inspect $containerName --format='{{.State.StartedAt}}' 2>/dev/null");
            $startTime = $startTimeRaw ? trim($startTimeRaw) : '';

            // Get memory usage
            $statsRaw = shell_exec("docker stats $containerName --no-stream --format 'table {{.MemUsage}}' 2>/dev/null | tail -1");
            $stats = $statsRaw ? trim($statsRaw) : '';
        } else {
            $lastActivity = "Container not running";
            $startTime = "N/A";
            $stats = "N/A";
        }

        $containers[] = [
            'name' => $containerName,
            'port' => $port,
            'running' => $isRunning,
            'last_activity' => $lastActivity ?: 'No recent activity',
            'started' => $startTime ?: 'Unknown',
            'memory' => $stats ?: 'N/A',
            'url' => "https://juice$i.wonkatech.org"
        ];
    }

    return $containers;
}

$containers = getDetailedContainerStatus();
$totalContainers = count($containers);
$runningContainers = count(array_filter($containers, function($c) { return $c['running']; }));
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
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .monitor-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
        }

        .monitor-header h1 {
            margin: 0 0 10px 0;
            font-size: 2.5rem;
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
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-2px);
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .stat-number.running { color: #28a745; }
        .stat-number.stopped { color: #dc3545; }
        .stat-number.total { color: #007bff; }

        .container-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
        }

        .container-card {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        .container-card:hover {
            transform: translateY(-2px);
        }

        .container-card.running {
            border-left: 5px solid #28a745;
        }

        .container-card.stopped {
            border-left: 5px solid #dc3545;
        }

        .container-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .container-name {
            font-size: 1.3rem;
            font-weight: bold;
        }

        .status-badge {
            padding: 6px 15px;
            border-radius: 25px;
            font-size: 0.85rem;
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
            font-size: 0.95rem;
            line-height: 1.8;
        }

        .refresh-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.2s;
        }

        .refresh-btn:hover {
            background: #0056b3;
        }

        .auto-refresh {
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: 15px;
        }

        .actions {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
                            <?php echo $container['running'] ? '🟢 Running' : '🔴 Stopped'; ?>
                        </div>
                    </div>

                    <div class="container-details">
                        <strong>Port:</strong> <?php echo $container['port']; ?><br>

                        <?php if ($container['running']): ?>
                            <strong>URL:</strong> <a href="<?php echo $container['url']; ?>" target="_blank" style="color: #007bff;"><?php echo $container['url']; ?></a><br>
                            <strong>Last Activity:</strong> <?php echo htmlspecialchars($container['last_activity']); ?><br>
                            <strong>Memory Usage:</strong> <?php echo htmlspecialchars($container['memory']); ?><br>
                            <strong>Started:</strong> <?php echo htmlspecialchars(substr($container['started'], 0, 19)); ?>
                        <?php else: ?>
                            <strong>Status:</strong> <span style="color: #dc3545;">Container offline</span><br>
                            <button onclick="startContainer('<?php echo $container['name']; ?>')" class="refresh-btn" style="margin-top: 15px; font-size: 0.9rem;">
                                🚀 Start Container
                            </button>
                        <?php endif; ?>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>

        <div class="actions">
            <button onclick="location.reload()" class="refresh-btn">🔄 Refresh Now</button>
            <a href="index.php" class="refresh-btn" style="text-decoration: none; margin-left: 15px; display: inline-block;">← Dashboard</a>
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