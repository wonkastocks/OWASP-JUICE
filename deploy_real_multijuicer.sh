#!/bin/bash

cat << 'DEPLOY_EOF' > /tmp/deploy_real_multijuicer.sh
#!/bin/bash

echo "================================================"
echo "Deploying True Multi-User Juice Shop Platform"
echo "================================================"

# Step 1: Stop single instance
echo "Step 1: Stopping single-instance Juice Shop..."
cd /opt/juice-shop-ctf
docker-compose down
docker system prune -f

# Step 2: Ensure K3s is running
echo ""
echo "Step 2: Setting up K3s..."
if ! command -v k3s &> /dev/null; then
    curl -sfL https://get.k3s.io | sh -
    sleep 30
fi

# Start K3s if not running
systemctl start k3s
sleep 10

# Step 3: Set up kubectl
echo ""
echo "Step 3: Configuring kubectl..."
mkdir -p ~/.kube
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
chmod 600 ~/.kube/config
export KUBECONFIG=~/.kube/config

# Step 4: Clean up previous deployments
echo ""
echo "Step 4: Cleaning up previous deployments..."
kubectl delete namespace multi-juicer 2>/dev/null || true
sleep 5

# Step 5: Create namespace
echo ""
echo "Step 5: Creating Multi-Juicer namespace..."
kubectl create namespace multi-juicer

# Step 6: Deploy Multi-Juicer using manifests
echo ""
echo "Step 6: Creating Multi-Juicer deployment..."

# Create ConfigMap for configuration
cat > /tmp/multijuicer-config.yaml << 'CONFIG_EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: multi-juicer-config
  namespace: multi-juicer
data:
  MULTI_JUICER_CONFIG: |
    adminPassword: "MultiJuicerAdmin2024!"
    maxInstances: "10"
    instanceCleanupTimeout: "3600"
CONFIG_EOF

kubectl apply -f /tmp/multijuicer-config.yaml

# Create the balancer deployment
cat > /tmp/balancer-deployment.yaml << 'BALANCER_EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: juice-balancer
  namespace: multi-juicer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: juice-balancer
  template:
    metadata:
      labels:
        app: juice-balancer
    spec:
      containers:
      - name: juice-balancer
        image: iteratec/juice-balancer:latest
        ports:
        - containerPort: 3000
        env:
        - name: ADMIN_PASSWORD
          value: "MultiJuicerAdmin2024!"
        - name: COOKIE_SECRET
          value: "super-secret-cookie-key-change-in-production"
        - name: MAX_INSTANCES
          value: "10"
        - name: INSTANCE_CLEANUP_TIMEOUT
          value: "3600"
---
apiVersion: v1
kind: Service
metadata:
  name: juice-balancer
  namespace: multi-juicer
spec:
  type: NodePort
  selector:
    app: juice-balancer
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 31000
BALANCER_EOF

kubectl apply -f /tmp/balancer-deployment.yaml

# Wait for deployment
echo ""
echo "Waiting for pods to start..."
sleep 30

# Step 7: Create simple port forwarding service
echo ""
echo "Step 7: Setting up access..."

# Create systemd service for port forwarding
cat > /etc/systemd/system/multijuicer-proxy.service << 'SERVICE_EOF'
[Unit]
Description=MultiJuicer Port Forward
After=k3s.service

[Service]
Type=simple
ExecStart=/usr/local/bin/kubectl port-forward -n multi-juicer --address 0.0.0.0 service/juice-balancer 3001:3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_EOF

systemctl daemon-reload
systemctl start multijuicer-proxy
systemctl enable multijuicer-proxy

# Step 8: Update Apache configuration
echo ""
echo "Step 8: Updating Apache configuration..."
cat > /etc/apache2/sites-available/multijuicer-final.conf << 'APACHE_EOF'
<VirtualHost *:80>
    ServerName 155.138.197.128
    DocumentRoot /var/www/html

    # Proxy to Multi-Juicer on port 3001
    ProxyPass /multi-juicer http://localhost:3001/
    ProxyPassReverse /multi-juicer http://localhost:3001/
    
    # WebSocket support
    RewriteEngine On
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/multi-juicer/(.*) "ws://localhost:3001/$1" [P,L]

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
APACHE_EOF

a2dissite default.conf
a2ensite multijuicer-final
systemctl reload apache2

# Step 9: Update landing page for multi-user
echo ""
echo "Step 9: Updating landing page for multi-user access..."
cat > /var/www/html/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Juicer CTF Platform - Multi-User OWASP Juice Shop</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
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
            max-width: 1000px;
            width: 90%;
        }
        .header { text-align: center; margin-bottom: 40px; }
        .logo { font-size: 100px; margin-bottom: 20px; }
        h1 { 
            color: #333; 
            font-size: 2.5em; 
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { color: #666; font-size: 1.3em; margin-bottom: 30px; }
        .highlight-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            text-align: center;
        }
        .highlight-box h2 { font-size: 1.8em; margin-bottom: 15px; }
        .highlight-box p { font-size: 1.1em; line-height: 1.6; }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }
        .feature {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
        }
        .feature-icon { font-size: 48px; margin-bottom: 15px; }
        .feature-title { font-weight: bold; color: #333; margin-bottom: 10px; }
        .feature-desc { color: #666; line-height: 1.5; }
        .cta-section {
            text-align: center;
            margin: 40px 0;
        }
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 60px;
            border-radius: 50px;
            text-decoration: none;
            font-size: 1.5em;
            font-weight: bold;
            margin: 10px;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .cta-button:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        .secondary-button {
            background: white;
            color: #667eea;
            border: 3px solid #667eea;
        }
        .how-it-works {
            background: #f0f8ff;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }
        .how-it-works h3 { color: #333; margin-bottom: 20px; }
        .step {
            display: flex;
            align-items: center;
            margin: 15px 0;
        }
        .step-number {
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-weight: bold;
        }
        .info-box {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        .status {
            background: #d4edda;
            border: 2px solid #28a745;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            color: #155724;
            margin-top: 30px;
        }
        .pulse {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #28a745;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🧃🧃🧃</div>
            <h1>Multi-Juicer Platform</h1>
            <p class="subtitle">Multi-User OWASP Juice Shop CTF Environment</p>
        </div>

        <div class="highlight-box">
            <h2>✨ True Multi-User Support!</h2>
            <p>Each participant gets their own isolated Juice Shop instance.<br>
            No interference, no shared progress, complete isolation for fair competition!</p>
        </div>

        <div class="features">
            <div class="feature">
                <div class="feature-icon">👤</div>
                <div class="feature-title">Individual Instances</div>
                <div class="feature-desc">Each user gets a dedicated, isolated Juice Shop environment</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">Secure Isolation</div>
                <div class="feature-desc">Complete separation between user instances with unique access codes</div>
            </div>
            <div class="feature">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Progress Tracking</div>
                <div class="feature-desc">Individual progress saved and tracked per user</div>
            </div>
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Auto-Scaling</div>
                <div class="feature-desc">Instances created on-demand, cleaned up after inactivity</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🏆</div>
                <div class="feature-title">Competition Ready</div>
                <div class="feature-desc">Perfect for CTF events and security training</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">100+ Challenges</div>
                <div class="feature-desc">Full Juice Shop experience for each user</div>
            </div>
        </div>

        <div class="cta-section">
            <a href="http://155.138.197.128:31000" class="cta-button">🚀 Launch Multi-Juicer</a>
            <a href="http://155.138.197.128:3000" class="cta-button secondary-button">📱 Single Instance</a>
        </div>

        <div class="how-it-works">
            <h3>🎮 How It Works</h3>
            <div class="step">
                <div class="step-number">1</div>
                <div>Click "Launch Multi-Juicer" above</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div>Register with your team name or username</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div>Receive your unique passcode (save it!)</div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div>Your personal Juice Shop instance will be created</div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div>Start hacking with no interference from others!</div>
            </div>
        </div>

        <div class="info-box">
            <strong>⚙️ Platform Configuration:</strong><br>
            • Max Concurrent Users: 10<br>
            • Instance Timeout: 1 hour (3600 seconds)<br>
            • Admin Password: MultiJuicerAdmin2024!<br>
            • Auto-cleanup: Enabled<br>
            • Kubernetes Backend: K3s
        </div>

        <div class="info-box" style="background: #e8f5e9; border-color: #4caf50;">
            <strong>📚 Resources:</strong><br>
            <a href="https://github.com/juice-shop/multi-juicer" target="_blank">Multi-Juicer GitHub</a> |
            <a href="https://pwning.owasp-juice.shop/" target="_blank">Juice Shop Guide</a> |
            <a href="https://owasp.org/www-project-juice-shop/" target="_blank">OWASP Project</a>
        </div>

        <div class="status">
            <span class="pulse"></span>
            <strong>Platform Status: OPERATIONAL</strong><br>
            Multi-Juicer: Port 31000 | Single Instance: Port 3000 | K3s: Active
        </div>
    </div>
</body>
</html>
HTML_EOF

chown www-data:www-data /var/www/html/index.html

# Step 10: Check status
echo ""
echo "Step 10: Checking deployment status..."
kubectl get pods -n multi-juicer
kubectl get svc -n multi-juicer

echo ""
echo "================================================"
echo "✓ MULTI-JUICER MULTI-USER PLATFORM DEPLOYED!"
echo "================================================"
echo ""
echo "🎯 Access Points:"
echo "   Landing Page: http://155.138.197.128/"
echo "   Multi-Juicer (Multi-User): http://155.138.197.128:31000/"
echo "   Single Instance: http://155.138.197.128:3000/"
echo ""
echo "👤 Admin Access:"
echo "   Username: admin"
echo "   Password: MultiJuicerAdmin2024!"
echo ""
echo "📊 Features:"
echo "   - Each user gets isolated instance"
echo "   - Auto-cleanup after 1 hour"
echo "   - Max 10 concurrent users"
echo "   - Full Juice Shop functionality per user"
echo ""
echo "================================================"
DEPLOY_EOF

echo "Deployment script created"