# 🔐 HTTPS Setup Complete for CTF Platform

## Overview
All Juice Shop container instances now use HTTPS via Cloudflare Tunnel subdomains. Each container has its own secure subdomain for participants to access.

## ✅ Completed Features

### 1. **HTTPS Subdomains Configuration**
- Each container (ports 3001-3020) mapped to secure subdomain
- Cloudflare Tunnel configured for all 20 instances
- SSL/TLS encryption for all container traffic

### 2. **Container URLs**
The following HTTPS URLs are now available:
- `https://juice1.wonkatech.org` → Port 3001
- `https://juice2.wonkatech.org` → Port 3002
- `https://juice3.wonkatech.org` → Port 3003
- `https://juice4.wonkatech.org` → Port 3004
- `https://juice5.wonkatech.org` → Port 3005
- `https://juice6.wonkatech.org` → Port 3006
- `https://juice7.wonkatech.org` → Port 3007
- `https://juice8.wonkatech.org` → Port 3008
- `https://juice9.wonkatech.org` → Port 3009
- `https://juice10.wonkatech.org` → Port 3010
- `https://juice11.wonkatech.org` → Port 3011
- `https://juice12.wonkatech.org` → Port 3012
- `https://juice13.wonkatech.org` → Port 3013
- `https://juice14.wonkatech.org` → Port 3014
- `https://juice15.wonkatech.org` → Port 3015
- `https://juice16.wonkatech.org` → Port 3016
- `https://juice17.wonkatech.org` → Port 3017
- `https://juice18.wonkatech.org` → Port 3018
- `https://juice19.wonkatech.org` → Port 3019
- `https://juice20.wonkatech.org` → Port 3020

### 3. **Database Updates**
- Added `container_url` column to containers table
- All container records updated with HTTPS URLs
- URLs automatically assigned when containers are created

### 4. **Admin Panel Updates**
- Container management shows HTTPS URLs
- User management displays assigned HTTPS URLs
- JavaScript enhancement for visual HTTPS indicators

### 5. **Cloudflare Tunnel Configuration**
- Tunnel: `wonkatech-ctf`
- Config file: `/etc/cloudflared/config.yml`
- All 20 juice subdomains configured
- Service running and auto-starts on boot

## 🔒 Security Benefits

1. **End-to-End Encryption**: All traffic between users and containers is encrypted
2. **No Direct Port Exposure**: Containers accessed via Cloudflare proxy, not direct IP:port
3. **DDoS Protection**: Cloudflare provides automatic DDoS mitigation
4. **SSL Certificate Management**: Cloudflare handles all SSL certificates automatically
5. **Professional Appearance**: Clean HTTPS URLs instead of IP:port combinations

## 📊 Current Status

- ✅ All 5 test containers (juice1-juice5) verified working
- ✅ HTTPS access confirmed via browser
- ✅ Admin panel updated with HTTPS links
- ✅ Database contains all HTTPS URLs
- ✅ Cloudflare Tunnel active and running

## 🚀 Usage

### For Administrators:
1. Access admin panel at: `https://wonkatech.org/admin/`
2. Container URLs are automatically shown in the interface
3. No additional configuration needed

### For CTF Participants:
1. Register on the platform
2. Get assigned a container (e.g., juice3)
3. Access via HTTPS: `https://juice3.wonkatech.org`
4. Start hacking with secure connection!

## 📝 DNS Configuration Note

If adding more subdomains in the future:
1. Log into Cloudflare Dashboard
2. Add CNAME records:
   - Name: `juiceX` (where X is the instance number)
   - Target: `wonkatech.org`
3. Update `/etc/cloudflared/config.yml` with new entries
4. Restart cloudflared service

## 🔧 Maintenance Commands

```bash
# Check Cloudflare Tunnel status
systemctl status cloudflared

# Restart Cloudflare Tunnel
systemctl restart cloudflared

# View tunnel configuration
cat /etc/cloudflared/config.yml

# Check container URLs in database
mysql -u root ctf_platform -e "SELECT container_name, port, container_url FROM containers ORDER BY port;"
```

## ✨ Summary

The CTF platform now provides secure HTTPS access to all Juice Shop container instances. Each participant gets their own secure subdomain, ensuring encrypted communication and a professional CTF experience.

---
**Deployment Date**: September 1, 2025
**Platform**: https://wonkatech.org
**Admin Panel**: https://wonkatech.org/admin/