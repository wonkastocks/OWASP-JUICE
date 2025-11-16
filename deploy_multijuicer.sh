#!/bin/bash

# Multi-Juicer Deployment Script
# This script installs Docker, K3s (lightweight Kubernetes), and Multi-Juicer

cat << 'DEPLOY_EOF' > /tmp/install_multijuicer.sh
#!/bin/bash

echo "================================================"
echo "Multi-Juicer CTF Platform Deployment"
echo "================================================"

# Step 1: Install Docker
echo ""
echo "Step 1: Installing Docker..."
if ! command -v docker &> /dev/null; then
    apt-get update
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Set up the repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Start Docker
    systemctl start docker
    systemctl enable docker
    echo "✓ Docker installed"
else
    echo "✓ Docker already installed"
fi

# Step 2: Install K3s (Lightweight Kubernetes)
echo ""
echo "Step 2: Installing K3s..."
if ! command -v k3s &> /dev/null; then
    curl -sfL https://get.k3s.io | sh -
    
    # Wait for K3s to be ready
    echo "Waiting for K3s to be ready..."
    sleep 30
    
    # Make kubectl accessible
    mkdir -p ~/.kube
    cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
    chmod 600 ~/.kube/config
    
    echo "✓ K3s installed"
else
    echo "✓ K3s already installed"
fi

# Step 3: Install Helm
echo ""
echo "Step 3: Installing Helm..."
if ! command -v helm &> /dev/null; then
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    echo "✓ Helm installed"
else
    echo "✓ Helm already installed"
fi

# Step 4: Clone Multi-Juicer repository
echo ""
echo "Step 4: Setting up Multi-Juicer..."
cd /opt
if [ ! -d "multi-juicer" ]; then
    git clone https://github.com/juice-shop/multi-juicer.git
fi
cd multi-juicer

# Step 5: Create Multi-Juicer configuration
echo ""
echo "Step 5: Creating Multi-Juicer configuration..."
cat > /opt/multi-juicer-values.yaml << 'CONFIG_EOF'
# Multi-Juicer Configuration
balancer:
  repository: iteratec/juice-balancer
  tag: latest
  replicas: 1
  service:
    type: NodePort
    nodePort: 30000

juiceShop:
  image: bkimminich/juice-shop
  tag: latest
  maxInstances: 10
  # Resources per Juice Shop instance
  resources:
    requests:
      memory: 200Mi
      cpu: 100m
    limits:
      memory: 500Mi
      cpu: 500m

# Admin settings
adminPassword: "CTFAdmin2024!"

# Instance cleanup (in seconds)
instanceCleanupAfter: 3600  # 1 hour

# Cookie settings
cookieSecret: "super-secret-cookie-key-change-me-in-production"

# Progress Watchdog settings
progressWatchdog:
  repository: iteratec/juice-progress-watchdog
  tag: latest

# Optional CTFd integration
ctfd:
  enabled: false
CONFIG_EOF

# Step 6: Deploy Multi-Juicer using Helm
echo ""
echo "Step 6: Deploying Multi-Juicer..."
cd /opt/multi-juicer
helm install multi-juicer ./helm/multi-juicer/ -f /opt/multi-juicer-values.yaml

# Wait for deployment
echo "Waiting for pods to be ready..."
sleep 45

# Step 7: Create Apache reverse proxy configuration
echo ""
echo "Step 7: Configuring Apache reverse proxy..."
cat > /etc/apache2/sites-available/multijuicer.conf << 'APACHE_EOF'
<VirtualHost *:80>
    ServerName 155.138.197.128
    DocumentRoot /var/www/html

    # Proxy to Multi-Juicer
    ProxyPreserveHost On
    ProxyPass /multi-juicer http://localhost:30000/
    ProxyPassReverse /multi-juicer http://localhost:30000/
    
    # WebSocket support
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/multi-juicer/(.*) "ws://localhost:30000/$1" [P,L]

    # Landing page at root
    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
APACHE_EOF

# Enable required Apache modules
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel
a2enmod rewrite

# Enable the site
a2ensite multijuicer
systemctl reload apache2

# Step 8: Create landing page
echo ""
echo "Step 8: Creating landing page..."
cat > /var/www/html/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Juicer CTF Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            max-width: 800px;
            width: 90%;
            text-align: center;
        }
        
        .logo {
            font-size: 72px;
            margin-bottom: 20px;
        }
        
        h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 40px;
            line-height: 1.6;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
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
            margin-bottom: 5px;
        }
        
        .feature-desc {
            color: #666;
            font-size: 0.9em;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 10px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .secondary-button {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .info-box {
            background: #f0f8ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 30px 0;
            text-align: left;
        }
        
        .info-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .info-content {
            color: #666;
        }
        
        .status {
            margin-top: 30px;
            padding: 15px;
            background: #e8f5e9;
            border-radius: 10px;
            color: #2e7d32;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🧃</div>
        <h1>Multi-Juicer CTF Platform</h1>
        <p class="subtitle">
            Multi-user OWASP Juice Shop environment for security training and Capture The Flag events
        </p>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Individual Instances</div>
                <div class="feature-desc">Each user gets their own Juice Shop instance</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🏆</div>
                <div class="feature-title">Score Tracking</div>
                <div class="feature-desc">Built-in scoreboard and progress tracking</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">Isolated Environment</div>
                <div class="feature-desc">Secure, sandboxed instances for each team</div>
            </div>
            <div class="feature">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Real-time Metrics</div>
                <div class="feature-desc">Monitor progress and challenge completion</div>
            </div>
        </div>
        
        <div class="info-box">
            <div class="info-title">🚀 Getting Started</div>
            <div class="info-content">
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>Click "Launch Multi-Juicer" to access the platform</li>
                    <li>Register with a team name or individual handle</li>
                    <li>Receive your unique access code</li>
                    <li>Start hacking on your personal Juice Shop instance!</li>
                </ol>
            </div>
        </div>
        
        <div>
            <a href="http://155.138.197.128:30000" class="cta-button">🚀 Launch Multi-Juicer</a>
            <a href="https://pwning.owasp-juice.shop/" target="_blank" class="cta-button secondary-button">📚 Documentation</a>
        </div>
        
        <div class="info-box">
            <div class="info-title">ℹ️ Platform Information</div>
            <div class="info-content">
                <strong>Admin Password:</strong> CTFAdmin2024!<br>
                <strong>Instance Timeout:</strong> 1 hour of inactivity<br>
                <strong>Max Concurrent Users:</strong> 10<br>
                <strong>Juice Shop Version:</strong> Latest
            </div>
        </div>
        
        <div class="status">
            ✅ Platform Status: <strong>OPERATIONAL</strong>
        </div>
    </div>
</body>
</html>
HTML_EOF

chown www-data:www-data /var/www/html/index.html

# Step 9: Check deployment status
echo ""
echo "Step 9: Checking deployment status..."
kubectl get pods
kubectl get svc

echo ""
echo "================================================"
echo "✓ MULTI-JUICER DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "Access Points:"
echo "- Landing Page: http://155.138.197.128/"
echo "- Multi-Juicer Direct: http://155.138.197.128:30000/"
echo "- Admin Password: CTFAdmin2024!"
echo ""
echo "Commands:"
echo "- Check pods: kubectl get pods"
echo "- Check logs: kubectl logs -f deployment/juice-balancer"
echo "- Scale instances: kubectl scale deployment juice-shop --replicas=5"
echo ""
echo "================================================"
DEPLOY_EOF

echo "Deployment script created at /tmp/install_multijuicer.sh"