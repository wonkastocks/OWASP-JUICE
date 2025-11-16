#!/bin/bash

# Setup Cloudflare Tunnel for WonkaTech CTF Platform
# This script sets up Cloudflare Tunnel to proxy ports 3001-3020

echo "Setting up Cloudflare Tunnel..."

# Step 1: Install cloudflared
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
rm cloudflared.deb

# Step 2: Authenticate (you'll need to login via browser)
echo "Authenticating with Cloudflare..."
echo "A browser window will open. Please log in to Cloudflare and authorize the tunnel."
cloudflared tunnel login

# Step 3: Create a tunnel
echo "Creating tunnel..."
cloudflared tunnel create wonkatech-ctf

# Step 4: Get tunnel UUID
TUNNEL_UUID=$(cloudflared tunnel list | grep wonkatech-ctf | awk '{print $1}')
echo "Tunnel UUID: $TUNNEL_UUID"

# Step 5: Create configuration file
cat > ~/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_UUID
credentials-file: /root/.cloudflared/$TUNNEL_UUID.json

ingress:
  # Main platform
  - hostname: wonkatech.org
    service: http://localhost:80
  - hostname: www.wonkatech.org
    service: http://localhost:80
    
  # Juice Shop instances - using subdomains
  - hostname: instance1.wonkatech.org
    service: http://localhost:3001
  - hostname: instance2.wonkatech.org
    service: http://localhost:3002
  - hostname: instance3.wonkatech.org
    service: http://localhost:3003
  - hostname: instance4.wonkatech.org
    service: http://localhost:3004
  - hostname: instance5.wonkatech.org
    service: http://localhost:3005
  - hostname: instance6.wonkatech.org
    service: http://localhost:3006
  - hostname: instance7.wonkatech.org
    service: http://localhost:3007
  - hostname: instance8.wonkatech.org
    service: http://localhost:3008
  - hostname: instance9.wonkatech.org
    service: http://localhost:3009
  - hostname: instance10.wonkatech.org
    service: http://localhost:3010
  - hostname: instance11.wonkatech.org
    service: http://localhost:3011
  - hostname: instance12.wonkatech.org
    service: http://localhost:3012
  - hostname: instance13.wonkatech.org
    service: http://localhost:3013
  - hostname: instance14.wonkatech.org
    service: http://localhost:3014
  - hostname: instance15.wonkatech.org
    service: http://localhost:3015
  - hostname: instance16.wonkatech.org
    service: http://localhost:3016
  - hostname: instance17.wonkatech.org
    service: http://localhost:3017
  - hostname: instance18.wonkatech.org
    service: http://localhost:3018
  - hostname: instance19.wonkatech.org
    service: http://localhost:3019
  - hostname: instance20.wonkatech.org
    service: http://localhost:3020
    
  # Catch-all
  - service: http_status:404
EOF

# Step 6: Route DNS to tunnel
echo "Routing DNS..."
cloudflared tunnel route dns wonkatech-ctf wonkatech.org
cloudflared tunnel route dns wonkatech-ctf '*.wonkatech.org'

# Step 7: Create systemd service
cloudflared service install

# Step 8: Start the tunnel
systemctl start cloudflared
systemctl enable cloudflared

echo "Tunnel setup complete!"
echo ""
echo "IMPORTANT NEXT STEPS:"
echo "1. Go to Cloudflare Dashboard > DNS"
echo "2. Delete the existing A record for wonkatech.org"
echo "3. You should see CNAME records pointing to the tunnel"
echo "4. Update dashboard.php to use subdomain URLs instead of ports"
echo ""
echo "Users will access instances at:"
echo "  https://instance1.wonkatech.org (instead of port 3001)"
echo "  https://instance2.wonkatech.org (instead of port 3002)"
echo "  etc..."