#!/bin/bash

# Simplified OWASP Juice Shop deployment with Docker Compose

cat << 'DEPLOY_EOF' > /tmp/deploy_juice_docker.sh
#!/bin/bash

echo "================================================"
echo "OWASP Juice Shop CTF Platform Deployment"
echo "================================================"

# Step 1: Stop K3s if it's running (from previous attempt)
echo ""
echo "Step 1: Cleaning up previous deployments..."
systemctl stop k3s 2>/dev/null
systemctl disable k3s 2>/dev/null
docker stop $(docker ps -aq) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Step 2: Create directory structure
echo ""
echo "Step 2: Creating directory structure..."
mkdir -p /opt/juice-shop-ctf
cd /opt/juice-shop-ctf

# Step 3: Create Docker Compose configuration
echo ""
echo "Step 3: Creating Docker Compose configuration..."
cat > docker-compose.yml << 'COMPOSE_EOF'
version: '3.7'

services:
  # Main Juice Shop instance
  juice-shop:
    image: bkimminich/juice-shop:latest
    container_name: juice-shop-main
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=ctf
    restart: unless-stopped
    networks:
      - juice-network

  # CTFd Platform (optional CTF scoreboard)
  ctfd:
    image: ctfd/ctfd:latest
    container_name: ctfd
    ports:
      - "8000:8000"
    environment:
      - WORKERS=4
      - DATABASE_URL=sqlite:////var/uploads/ctfd.db
    volumes:
      - ctfd-data:/var/uploads
      - ctfd-logs:/var/log/CTFd
    restart: unless-stopped
    networks:
      - juice-network

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: juice-nginx
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - juice-shop
      - ctfd
    restart: unless-stopped
    networks:
      - juice-network

volumes:
  ctfd-data:
  ctfd-logs:

networks:
  juice-network:
    driver: bridge
COMPOSE_EOF

# Step 4: Create Nginx configuration
echo ""
echo "Step 4: Creating Nginx configuration..."
cat > nginx.conf << 'NGINX_EOF'
events {
    worker_connections 1024;
}

http {
    upstream juice {
        server juice-shop:3000;
    }

    upstream ctfd {
        server ctfd:8000;
    }

    server {
        listen 80;
        server_name _;

        location / {
            root /usr/share/nginx/html;
            try_files $uri @juice;
        }

        location @juice {
            proxy_pass http://juice;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /ctfd/ {
            proxy_pass http://ctfd/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
NGINX_EOF

# Step 5: Create management script
echo ""
echo "Step 5: Creating management script..."
cat > manage.sh << 'MANAGE_EOF'
#!/bin/bash

case "$1" in
    start)
        echo "Starting Juice Shop CTF..."
        docker-compose up -d
        ;;
    stop)
        echo "Stopping Juice Shop CTF..."
        docker-compose down
        ;;
    restart)
        echo "Restarting Juice Shop CTF..."
        docker-compose restart
        ;;
    logs)
        docker-compose logs -f
        ;;
    status)
        docker-compose ps
        ;;
    scale)
        echo "Scaling Juice Shop instances to $2..."
        docker-compose up -d --scale juice-shop=$2
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status|scale <number>}"
        exit 1
        ;;
esac
MANAGE_EOF

chmod +x manage.sh

# Step 6: Start the services
echo ""
echo "Step 6: Starting services..."
docker-compose pull
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 30

# Step 7: Configure Apache to proxy to Docker services
echo ""
echo "Step 7: Configuring Apache proxy..."
cat > /etc/apache2/sites-available/juiceshop.conf << 'APACHE_EOF'
<VirtualHost *:80>
    ServerName 155.138.197.128
    DocumentRoot /var/www/html

    # Enable proxy modules
    ProxyPreserveHost On

    # Main site
    ProxyPass /juice http://localhost:3000/
    ProxyPassReverse /juice http://localhost:3000/

    # CTFd platform
    ProxyPass /ctfd http://localhost:8000/
    ProxyPassReverse /ctfd http://localhost:8000/

    # Combined platform on port 8080
    ProxyPass /platform http://localhost:8080/
    ProxyPassReverse /platform http://localhost:8080/

    # WebSocket support for Juice Shop
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/juice/(.*) "ws://localhost:3000/$1" [P,L]

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/juiceshop-error.log
    CustomLog ${APACHE_LOG_DIR}/juiceshop-access.log combined
</VirtualHost>
APACHE_EOF

# Disable previous site and enable new one
a2dissite multijuicer.conf 2>/dev/null
a2ensite juiceshop.conf
systemctl reload apache2

# Step 8: Update landing page
echo ""
echo "Step 8: Updating landing page..."
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
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 80px;
            margin-bottom: 20px;
        }
        
        h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
        }
        
        .platforms {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        
        .platform-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .platform-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .platform-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .platform-title {
            font-size: 1.4em;
            color: #333;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .platform-desc {
            color: #666;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        .platform-button {
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: opacity 0.3s;
        }
        
        .platform-button:hover {
            opacity: 0.9;
        }
        
        .features {
            background: #f0f0f0;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }
        
        .features-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .feature-check {
            color: #4CAF50;
            font-size: 20px;
        }
        
        .info-section {
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }
        
        .info-title {
            color: #856404;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .info-content {
            color: #856404;
            line-height: 1.6;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #4CAF50;
            border-radius: 50%;
            margin-right: 5px;
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
        <div class="header">
            <div class="logo">🧃</div>
            <h1>OWASP Juice Shop CTF</h1>
            <p class="subtitle">The Most Modern & Sophisticated Insecure Web Application</p>
        </div>
        
        <div class="platforms">
            <div class="platform-card">
                <div class="platform-icon">🎯</div>
                <div class="platform-title">Juice Shop</div>
                <div class="platform-desc">
                    Main vulnerable application with 100+ security challenges
                </div>
                <a href="http://155.138.197.128:3000" class="platform-button">Launch Juice Shop</a>
            </div>
            
            <div class="platform-card">
                <div class="platform-icon">🏆</div>
                <div class="platform-title">CTFd Platform</div>
                <div class="platform-desc">
                    Capture The Flag scoreboard and challenge tracking system
                </div>
                <a href="http://155.138.197.128:8000" class="platform-button">Open CTFd</a>
            </div>
            
            <div class="platform-card">
                <div class="platform-icon">📚</div>
                <div class="platform-title">Documentation</div>
                <div class="platform-desc">
                    Official guide for solving challenges and understanding vulnerabilities
                </div>
                <a href="https://pwning.owasp-juice.shop/" target="_blank" class="platform-button">View Docs</a>
            </div>
        </div>
        
        <div class="features">
            <div class="features-title">🎮 Platform Features</div>
            <div class="feature-list">
                <div class="feature-item">
                    <span class="feature-check">✅</span>
                    <span>100+ Hacking Challenges</span>
                </div>
                <div class="feature-item">
                    <span class="feature-check">✅</span>
                    <span>6 Difficulty Levels</span>
                </div>
                <div class="feature-item">
                    <span class="feature-check">✅</span>
                    <span>Score Tracking</span>
                </div>
                <div class="feature-item">
                    <span class="feature-check">✅</span>
                    <span>Progress Backup</span>
                </div>
                <div class="feature-item">
                    <span class="feature-check">✅</span>
                    <span>Built-in Hints</span>
                </div>
                <div class="feature-item">
                    <span class="feature-check">✅</span>
                    <span>Code Analysis</span>
                </div>
            </div>
        </div>
        
        <div class="info-section">
            <div class="info-title">⚡ Quick Start Guide</div>
            <div class="info-content">
                <ol style="margin-left: 20px;">
                    <li>Click "Launch Juice Shop" to start hacking</li>
                    <li>Look for the Score Board (it's hidden!)</li>
                    <li>Start with ⭐ (1-star) challenges</li>
                    <li>Use CTFd to track team progress (optional)</li>
                    <li>Check documentation if you get stuck</li>
                </ol>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <span class="status-indicator"></span>
            Platform Status: <strong>ONLINE</strong> | 
            Docker Services: <strong>RUNNING</strong> | 
            Version: <strong>Latest</strong>
        </div>
    </div>
</body>
</html>
HTML_EOF

chown www-data:www-data /var/www/html/index.html

# Step 9: Check status
echo ""
echo "Step 9: Checking service status..."
docker-compose ps

echo ""
echo "================================================"
echo "✓ JUICE SHOP CTF DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "🎯 Access Points:"
echo "   Landing Page: http://155.138.197.128/"
echo "   Juice Shop: http://155.138.197.128:3000/"
echo "   CTFd Platform: http://155.138.197.128:8000/"
echo ""
echo "📝 Management Commands:"
echo "   cd /opt/juice-shop-ctf"
echo "   ./manage.sh status    # Check status"
echo "   ./manage.sh logs      # View logs"
echo "   ./manage.sh restart   # Restart services"
echo ""
echo "🔧 Docker Commands:"
echo "   docker ps             # List containers"
echo "   docker logs juice-shop-main  # View Juice Shop logs"
echo "   docker logs ctfd      # View CTFd logs"
echo ""
echo "================================================"
DEPLOY_EOF

echo "Deployment script created at /tmp/deploy_juice_docker.sh"