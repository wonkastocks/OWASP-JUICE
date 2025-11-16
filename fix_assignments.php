<?php
// Fix container assignments and check status

// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "ctf_platform";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

echo "<h1>Fixing Container Assignments</h1>\n";

// Step 1: Clear existing assignments
echo "<h2>Step 1: Clearing existing assignments...</h2>\n";
$sql = "UPDATE containers SET user_id = NULL, allocated = 0";
$conn->query($sql);
echo "Cleared all assignments.<br>\n";

// Step 2: Get Docker container status
echo "<h2>Step 2: Checking Docker containers...</h2>\n";
$docker_output = shell_exec("docker ps -a --format 'table {{.Names}}\t{{.Status}}' | grep juice 2>&1");
echo "<pre>$docker_output</pre>\n";

// Step 3: Update container status in database
echo "<h2>Step 3: Updating container status...</h2>\n";
$containers = shell_exec("docker ps --format '{{.Names}}' | grep juice");
$running_containers = explode("\n", trim($containers));

foreach ($running_containers as $container) {
    if (!empty($container)) {
        $container_id = str_replace('juice', '', $container);
        $sql = "UPDATE containers SET status = 'running' WHERE container_id = '$container_id'";
        $conn->query($sql);
        echo "Updated $container to running<br>\n";
    }
}

// Step 4: Assign containers based on user instance URLs
echo "<h2>Step 4: Assigning containers to users...</h2>\n";
$sql = "UPDATE containers c
        JOIN users u ON u.instance_url = CONCAT('https://juice', c.container_id, '.wonkatech.org')
        SET c.user_id = u.id, c.allocated = 1
        WHERE u.instance_url IS NOT NULL";
$conn->query($sql);
echo "Assigned containers based on instance URLs.<br>\n";

// Step 5: Show current assignments
echo "<h2>Step 5: Current Assignments:</h2>\n";
$sql = "SELECT c.container_id, c.container_name, u.username, c.allocated, c.status
        FROM containers c
        LEFT JOIN users u ON c.user_id = u.id
        ORDER BY c.container_id";
$result = $conn->query($sql);

echo "<table border='1'>\n";
echo "<tr><th>Container ID</th><th>Container Name</th><th>Username</th><th>Allocated</th><th>Status</th></tr>\n";

while($row = $result->fetch_assoc()) {
    echo "<tr>";
    echo "<td>" . $row['container_id'] . "</td>";
    echo "<td>" . $row['container_name'] . "</td>";
    echo "<td>" . ($row['username'] ?: 'Not Assigned') . "</td>";
    echo "<td>" . ($row['allocated'] ? 'Yes' : 'No') . "</td>";
    echo "<td>" . $row['status'] . "</td>";
    echo "</tr>\n";
}
echo "</table>\n";

// Step 6: Test each juice instance
echo "<h2>Step 6: Testing Juice Shop Instances:</h2>\n";
echo "<table border='1'>\n";
echo "<tr><th>Instance</th><th>Status</th><th>Response Code</th></tr>\n";

for ($i = 1; $i <= 15; $i++) {
    $url = "https://juice$i.wonkatech.org";
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, true);
    curl_setopt($ch, CURLOPT_NOBODY, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    $status = ($httpcode == 200 || $httpcode == 301 || $httpcode == 302) ? "OK" : "FAILED";
    $color = ($status == "OK") ? "green" : "red";
    
    echo "<tr>";
    echo "<td>juice$i</td>";
    echo "<td style='color: $color'>$status</td>";
    echo "<td>$httpcode</td>";
    echo "</tr>\n";
    
    // If failed, try to restart the container
    if ($status == "FAILED") {
        shell_exec("docker start juice$i 2>&1");
    }
}
echo "</table>\n";

// Step 7: Restart stopped containers
echo "<h2>Step 7: Restarting any stopped containers...</h2>\n";
$stopped = shell_exec("docker ps -a | grep 'Exited' | grep juice | awk '{print $NF}'");
$stopped_containers = explode("\n", trim($stopped));

foreach ($stopped_containers as $container) {
    if (!empty($container)) {
        echo "Restarting $container...<br>\n";
        shell_exec("docker start $container 2>&1");
    }
}

echo "<h2>Fix Complete!</h2>\n";
echo "<p><a href='https://wonkatech.org/admin/containers.php'>Check Admin Panel</a></p>\n";

$conn->close();
?>