<?php
// Test script to populate and verify scoring system
require_once 'config.php';

echo "<h2>Testing Scoring System</h2>";

$conn = getDBConnection();

// Test user ID (you can change this)
$test_user_id = 1;

echo "<h3>1. Adding Test Challenge Progress</h3>";

// Sample challenges to add
$challenges = [
    ['name' => 'Score Board', 'category' => 'Trivial', 'points' => 100],
    ['name' => 'DOM XSS', 'category' => 'XSS', 'points' => 100],
    ['name' => 'SQL Injection', 'category' => 'Injection', 'points' => 250],
    ['name' => 'Admin Section', 'category' => 'Broken Access Control', 'points' => 200],
    ['name' => 'Password Strength', 'category' => 'Broken Authentication', 'points' => 150],
];

foreach ($challenges as $challenge) {
    // Check if challenge already exists for user
    $stmt = $conn->prepare("SELECT id FROM challenge_progress WHERE user_id = ? AND challenge_name = ?");
    $stmt->bind_param("is", $test_user_id, $challenge['name']);
    $stmt->execute();
    
    if ($stmt->get_result()->num_rows == 0) {
        // Add challenge progress
        $stmt = $conn->prepare("INSERT INTO challenge_progress (user_id, challenge_name, challenge_category, points, completed_at, time_taken, hints_used) VALUES (?, ?, ?, ?, NOW(), ?, ?)");
        $time_taken = rand(60, 3600); // Random time between 1 min and 1 hour
        $hints_used = rand(0, 3);
        $stmt->bind_param("issiii", $test_user_id, $challenge['name'], $challenge['category'], $challenge['points'], $time_taken, $hints_used);
        
        if ($stmt->execute()) {
            echo "✅ Added challenge: {$challenge['name']} ({$challenge['points']} points)<br>";
        } else {
            echo "❌ Failed to add challenge: {$challenge['name']}<br>";
        }
    } else {
        echo "⚠️ Challenge already exists: {$challenge['name']}<br>";
    }
}

echo "<h3>2. Updating User Score</h3>";

// Calculate total score for user
$stmt = $conn->prepare("SELECT SUM(points) as total_points, COUNT(*) as total_challenges FROM challenge_progress WHERE user_id = ?");
$stmt->bind_param("i", $test_user_id);
$stmt->execute();
$result = $stmt->get_result()->fetch_assoc();

$total_score = $result['total_points'] ?? 0;
$total_challenges = $result['total_challenges'] ?? 0;

// Update or insert score record
$stmt = $conn->prepare("INSERT INTO scores (user_id, total_score, challenges_completed) VALUES (?, ?, ?) 
                        ON DUPLICATE KEY UPDATE total_score = ?, challenges_completed = ?");
$stmt->bind_param("iiiii", $test_user_id, $total_score, $total_challenges, $total_score, $total_challenges);

if ($stmt->execute()) {
    echo "✅ Updated score: $total_score points from $total_challenges challenges<br>";
} else {
    echo "❌ Failed to update score<br>";
}

echo "<h3>3. Calculate Rankings</h3>";

// Update rankings for all users
$conn->query("SET @rank = 0");
$conn->query("UPDATE scores SET user_rank = (@rank := @rank + 1) ORDER BY total_score DESC");

echo "✅ Rankings updated<br>";

echo "<h3>4. Display Leaderboard</h3>";

// Show top users
$result = $conn->query("
    SELECT u.username, u.email, s.total_score, s.challenges_completed, s.user_rank 
    FROM scores s 
    JOIN users u ON s.user_id = u.id 
    ORDER BY s.total_score DESC 
    LIMIT 10
");

echo "<table border='1' style='border-collapse: collapse; margin: 10px 0;'>";
echo "<tr><th>Rank</th><th>Username</th><th>Email</th><th>Score</th><th>Challenges</th></tr>";

while ($row = $result->fetch_assoc()) {
    echo "<tr>";
    echo "<td style='padding: 5px;'>{$row['user_rank']}</td>";
    echo "<td style='padding: 5px;'>{$row['username']}</td>";
    echo "<td style='padding: 5px;'>{$row['email']}</td>";
    echo "<td style='padding: 5px;'>{$row['total_score']}</td>";
    echo "<td style='padding: 5px;'>{$row['challenges_completed']}</td>";
    echo "</tr>";
}
echo "</table>";

echo "<h3>5. Test Juice Shop Integration</h3>";

// Check if we can connect to a Juice Shop instance
$port = 3003; // Wonka's port
$juice_url = "http://155.138.197.128:$port/api/Challenges";

echo "Attempting to fetch challenges from Juice Shop on port $port...<br>";

$ch = curl_init($juice_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code == 200) {
    $data = json_decode($response, true);
    $challenge_count = count($data['data'] ?? []);
    echo "✅ Successfully connected! Found $challenge_count challenges in Juice Shop<br>";
} else {
    echo "⚠️ Could not connect to Juice Shop (HTTP $http_code)<br>";
}

$conn->close();

echo "<br><a href='users.php'>← Back to User Management</a>";
?>