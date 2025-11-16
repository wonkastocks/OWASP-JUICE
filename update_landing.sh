#!/bin/bash

cat << 'UPDATE_EOF' > /tmp/update_landing.sh
#!/bin/bash

echo "================================================"
echo "Updating Landing Page and Apache Config"
echo "================================================"

# Update landing page to reflect actual working services
cat > /var/www/html/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OWASP Juice Shop CTF Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 60px;
            max-width: 900px;
            width: 90%;
            text-align: center;
        }
        
        .logo {
            font-size: 100px;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        h1 {
            color: #333;
            font-size: 3em;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.3em;
            margin-bottom: 40px;
            font-style: italic;
        }
        
        .main-cta {
            display: inline-block;
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
            color: white;
            padding: 20px 60px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.5em;
            font-weight: bold;
            margin: 30px 0;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .main-cta:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .feature {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .feature-icon {
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .feature-title {
            font-weight: bold;
            color: #333;
        }
        
        .challenge-levels {
            background: #f0f8ff;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .challenge-levels h2 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .level-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .level {
            padding: 10px;
            background: white;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        
        .level-stars {
            color: #ffd700;
            font-size: 1.2em;
        }
        
        .level-name {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .info-box {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
            text-align: left;
        }
        
        .info-title {
            color: #856404;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .status {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 10px;
            padding: 15px;
            color: #155724;
            margin-top: 30px;
        }
        
        .status-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #28a745;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🧃</div>
        <h1>OWASP Juice Shop</h1>
        <p class="subtitle">The Most Modern & Sophisticated Insecure Web Application</p>
        
        <a href="http://155.138.197.128:3000" class="main-cta">🚀 Start Hacking!</a>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">100+ Challenges</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🏆</div>
                <div class="feature-title">Score Board</div>
            </div>
            <div class="feature">
                <div class="feature-icon">💡</div>
                <div class="feature-title">Built-in Hints</div>
            </div>
            <div class="feature">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Progress Tracking</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Code Review</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🎓</div>
                <div class="feature-title">Tutorial Mode</div>
            </div>
        </div>
        
        <div class="challenge-levels">
            <h2>🎮 Challenge Difficulty Levels</h2>
            <div class="level-grid">
                <div class="level">
                    <div class="level-stars">⭐</div>
                    <div class="level-name">Trivial</div>
                </div>
                <div class="level">
                    <div class="level-stars">⭐⭐</div>
                    <div class="level-name">Easy</div>
                </div>
                <div class="level">
                    <div class="level-stars">⭐⭐⭐</div>
                    <div class="level-name">Medium</div>
                </div>
                <div class="level">
                    <div class="level-stars">⭐⭐⭐⭐</div>
                    <div class="level-name">Hard</div>
                </div>
                <div class="level">
                    <div class="level-stars">⭐⭐⭐⭐⭐</div>
                    <div class="level-name">Dreadful</div>
                </div>
                <div class="level">
                    <div class="level-stars">⭐⭐⭐⭐⭐⭐</div>
                    <div class="level-name">Diabolic</div>
                </div>
            </div>
        </div>
        
        <div class="info-box">
            <div class="info-title">🎯 Your First Challenge</div>
            <div style="color: #856404; line-height: 1.6;">
                <strong>Find the Score Board!</strong> It's intentionally hidden. This is your first challenge!<br><br>
                Hints:
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>Check the JavaScript files</li>
                    <li>Look at the source code</li>
                    <li>Try different URLs</li>
                    <li>Use your browser's developer tools</li>
                </ul>
            </div>
        </div>
        
        <div class="info-box" style="background: #e8f5e9; border-color: #4caf50;">
            <div class="info-title" style="color: #2e7d32;">📚 Resources</div>
            <div style="color: #2e7d32; line-height: 1.6;">
                <a href="https://pwning.owasp-juice.shop/" target="_blank" style="color: #2e7d32;">Official Documentation</a> |
                <a href="https://github.com/juice-shop/juice-shop" target="_blank" style="color: #2e7d32;">GitHub Repository</a> |
                <a href="https://owasp.org/www-project-juice-shop/" target="_blank" style="color: #2e7d32;">OWASP Project Page</a>
            </div>
        </div>
        
        <div class="status">
            <span class="status-dot"></span>
            <strong>Platform Status:</strong> ONLINE | 
            <strong>Version:</strong> Latest | 
            <strong>Docker:</strong> Running
        </div>
    </div>
</body>
</html>
HTML_EOF

# Check Docker services
echo ""
echo "Current Docker services:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "================================================"
echo "✓ Landing page updated!"
echo "================================================"
echo ""
echo "Access Points:"
echo "  Landing Page: http://155.138.197.128/"
echo "  Juice Shop Direct: http://155.138.197.128:3000/"
echo ""
UPDATE_EOF

echo "Update script created"