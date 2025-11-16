#!/bin/bash

# Setup HTTPS access for Juice Shop containers via Cloudflare Tunnel

echo "🔐 Setting up HTTPS for Juice Shop containers..."

# Container configuration
CONTAINERS=(
    "juice1:3001"
    "juice2:3002"
    "juice3:3003"
    "juice4:3004"
    "juice5:3005"
    "juice6:3006"
    "juice7:3007"
    "juice8:3008"
    "juice9:3009"
    "juice10:3010"
    "juice11:3011"
    "juice12:3012"
    "juice13:3013"
    "juice14:3014"
    "juice15:3015"
    "juice16:3016"
    "juice17:3017"
    "juice18:3018"
    "juice19:3019"
    "juice20:3020"
)

echo "📝 Creating Cloudflare Tunnel configuration..."

# Create the tunnel configuration file
cat > /tmp/cloudflare_tunnel_config.yml << 'EOF'
tunnel: wonkatech-tunnel
credentials-file: /root/.cloudflared/cert.pem

ingress:
  # Main site
  - hostname: wonkatech.org
    service: http://localhost:80
  
  # Admin panel
  - hostname: admin.wonkatech.org
    service: http://localhost:80
    path: /admin/
  
  # Juice Shop instances
  - hostname: juice1.wonkatech.org
    service: http://localhost:3001
  
  - hostname: juice2.wonkatech.org
    service: http://localhost:3002
  
  - hostname: juice3.wonkatech.org
    service: http://localhost:3003
  
  - hostname: juice4.wonkatech.org
    service: http://localhost:3004
  
  - hostname: juice5.wonkatech.org
    service: http://localhost:3005
  
  - hostname: juice6.wonkatech.org
    service: http://localhost:3006
  
  - hostname: juice7.wonkatech.org
    service: http://localhost:3007
  
  - hostname: juice8.wonkatech.org
    service: http://localhost:3008
  
  - hostname: juice9.wonkatech.org
    service: http://localhost:3009
  
  - hostname: juice10.wonkatech.org
    service: http://localhost:3010
  
  - hostname: juice11.wonkatech.org
    service: http://localhost:3011
  
  - hostname: juice12.wonkatech.org
    service: http://localhost:3012
  
  - hostname: juice13.wonkatech.org
    service: http://localhost:3013
  
  - hostname: juice14.wonkatech.org
    service: http://localhost:3014
  
  - hostname: juice15.wonkatech.org
    service: http://localhost:3015
  
  - hostname: juice16.wonkatech.org
    service: http://localhost:3016
  
  - hostname: juice17.wonkatech.org
    service: http://localhost:3017
  
  - hostname: juice18.wonkatech.org
    service: http://localhost:3018
  
  - hostname: juice19.wonkatech.org
    service: http://localhost:3019
  
  - hostname: juice20.wonkatech.org
    service: http://localhost:3020
  
  # Catch-all
  - service: http_status:404
EOF

echo "✅ Cloudflare Tunnel configuration created"

# Create SQL update script
cat > /tmp/update_container_urls.sql << 'EOF'
-- Update container URLs to use HTTPS subdomains
UPDATE containers SET container_url = CASE
    WHEN port = 3001 THEN 'https://juice1.wonkatech.org'
    WHEN port = 3002 THEN 'https://juice2.wonkatech.org'
    WHEN port = 3003 THEN 'https://juice3.wonkatech.org'
    WHEN port = 3004 THEN 'https://juice4.wonkatech.org'
    WHEN port = 3005 THEN 'https://juice5.wonkatech.org'
    WHEN port = 3006 THEN 'https://juice6.wonkatech.org'
    WHEN port = 3007 THEN 'https://juice7.wonkatech.org'
    WHEN port = 3008 THEN 'https://juice8.wonkatech.org'
    WHEN port = 3009 THEN 'https://juice9.wonkatech.org'
    WHEN port = 3010 THEN 'https://juice10.wonkatech.org'
    WHEN port = 3011 THEN 'https://juice11.wonkatech.org'
    WHEN port = 3012 THEN 'https://juice12.wonkatech.org'
    WHEN port = 3013 THEN 'https://juice13.wonkatech.org'
    WHEN port = 3014 THEN 'https://juice14.wonkatech.org'
    WHEN port = 3015 THEN 'https://juice15.wonkatech.org'
    WHEN port = 3016 THEN 'https://juice16.wonkatech.org'
    WHEN port = 3017 THEN 'https://juice17.wonkatech.org'
    WHEN port = 3018 THEN 'https://juice18.wonkatech.org'
    WHEN port = 3019 THEN 'https://juice19.wonkatech.org'
    WHEN port = 3020 THEN 'https://juice20.wonkatech.org'
    ELSE container_url
END;

-- Show updated URLs
SELECT container_name, port, container_url FROM containers ORDER BY port;
EOF

echo "✅ Database update script created"
echo ""
echo "📌 Next steps:"
echo "1. Deploy the Cloudflare Tunnel configuration"
echo "2. Add DNS records for juice1-juice20.wonkatech.org"
echo "3. Update the database with HTTPS URLs"
echo "4. Restart Cloudflare Tunnel"