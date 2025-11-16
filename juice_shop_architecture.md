# OWASP Juice Shop CTF Platform - Architecture Diagram

## 🏗️ Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           WONKATECH CTF PLATFORM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

                                    INTERNET
                                        │
                                        │
                            ┌───────────▼───────────┐
                            │                       │
                            │   CLOUDFLARE TUNNEL   │
                            │   wonkatech.org       │
                            │   (HTTPS/SSL)         │
                            │                       │
                            └───────────┬───────────┘
                                        │
                                        │
                        ┌───────────────▼────────────────┐
                        │                                │
                        │     VULTR VPS SERVER          │
                        │   155.138.197.128             │
                        │   Ubuntu 22.04.5 LTS          │
                        │   75GB Storage / 4GB RAM      │
                        │                                │
                        └───────────────┬────────────────┘
                                        │
            ┌───────────────────────────┴───────────────────────────┐
            │                                                       │
            │                    DOCKER ENGINE                      │
            │                     (Container Host)                  │
            │                                                       │
            └───────────────────────────┬───────────────────────────┘
                                        │
    ┌───────────────────────────────────┴───────────────────────────────────┐
    │                                                                       │
    │                         CONTAINERIZED SERVICES                        │
    │                                                                       │
    ├─────────────┬──────────────┬──────────────┬──────────────┬──────────┤
    │             │              │              │              │          │
┌───▼──────┐ ┌───▼──────┐ ┌────▼─────┐ ┌────▼─────┐ ┌────▼─────┐       │
│ JUICE #1 │ │ JUICE #2 │ │ JUICE #3 │ │ JUICE #4 │ │ JUICE #5 │       │
│ Port:3001│ │ Port:3002│ │ Port:3003│ │ Port:3004│ │ Port:3005│       │
│ User 1   │ │ User 2   │ │ Wonka    │ │ User 4   │ │ User 5   │       │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
                                                                         │
┌────────────────────────────────────────────────────────────────────────┤
│                         WEB SERVICES                                   │
├─────────────────────────┬──────────────────────────────────────────────┤
│                         │                                              │
│    ┌──────────────┐     │              ┌─────────────────┐            │
│    │   APACHE2    │     │              │   MySQL/MariaDB │            │
│    │   Port: 80   │◄────┼──────────────┤   Port: 3306    │            │
│    │   PHP 8.1    │     │              │   CTF Database   │            │
│    └──────────────┘     │              └─────────────────┘            │
│           │              │                                             │
│           ▼              │                                             │
│  ┌────────────────┐     │                                             │
│  │ CTF Platform   │     │                                             │
│  │ Registration   │     │                                             │
│  │ /var/www/html  │     │                                             │
│  └────────────────┘     │                                             │
│                         │                                             │
└─────────────────────────┴──────────────────────────────────────────────┘
```

## 📊 Technical Stack Breakdown

```
┌──────────────────────────────────────────────────────────────┐
│                    JUICE SHOP TECH STACK                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend (Client-Side)                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • Angular 17.0.0 (TypeScript)                     │     │
│  │  • Angular Material (UI Components)                │     │
│  │  • Bootstrap 5 (CSS Framework)                     │     │
│  │  • FontAwesome (Icons)                             │     │
│  │  • SPA (Single Page Application)                   │     │
│  └────────────────────────────────────────────────────┘     │
│                           │                                  │
│                           ▼                                  │
│  Backend (Server-Side)                                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • Node.js 20.x (JavaScript Runtime)               │     │
│  │  • Express.js (Web Framework)                      │     │
│  │  • SQLite3 (Embedded Database)                     │     │
│  │  • Sequelize ORM (Database Abstraction)            │     │
│  │  • JWT (JSON Web Tokens for Auth)                  │     │
│  │  • Bcrypt (Password Hashing)                       │     │
│  │  • Socket.io (Real-time Communication)             │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Container & Deployment                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • Docker (Containerization)                       │     │
│  │  • Alpine Linux (Base Image)                       │     │
│  │  • PM2 (Process Manager)                           │     │
│  │  • nginx (Reverse Proxy - optional)                │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🔧 CTF Platform Stack

```
┌──────────────────────────────────────────────────────────────┐
│                  CTF REGISTRATION PLATFORM                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Web Server                                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • Apache2 2.4.x                                   │     │
│  │  • PHP 8.1 (Server-side scripting)                 │     │
│  │  • mod_rewrite (URL rewriting)                     │     │
│  │  • mod_ssl (HTTPS support via Cloudflare)          │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Database                                                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • MySQL 8.0 / MariaDB 10.x                        │     │
│  │  • InnoDB Engine                                   │     │
│  │  • UTF8MB4 Character Set                           │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Application Features                                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • User Registration & Authentication              │     │
│  │  • Email Verification (Gmail SMTP)                 │     │
│  │  • Instance Assignment (Ports 3001-3005)           │     │
│  │  • Password Reset Functionality                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🖥️ Server Requirements & Specifications

```
┌──────────────────────────────────────────────────────────────┐
│                    HOSTING REQUIREMENTS                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Minimum Requirements (5 users):                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │  CPU:     2 vCPUs @ 2.0GHz+                        │     │
│  │  RAM:     4GB (minimum)                            │     │
│  │  Storage: 40GB SSD                                 │     │
│  │  Network: 100Mbps                                  │     │
│  │  OS:      Ubuntu 20.04+ LTS                        │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Current Setup (Vultr VPS):                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  CPU:     2-4 vCPUs                                │     │
│  │  RAM:     4GB                                      │     │
│  │  Storage: 75GB SSD                                 │     │
│  │  Network: 1Gbps                                    │     │
│  │  OS:      Ubuntu 22.04.5 LTS                       │     │
│  │  IP:      155.138.197.128                          │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Resource Usage Per Container:                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │  CPU:     ~200-400m (0.2-0.4 cores)                │     │
│  │  RAM:     ~200-400MB per instance                  │     │
│  │  Storage: ~500MB per container                      │     │
│  │  Network: ~10-50Mbps during active use             │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🔒 Security & Network Configuration

```
┌──────────────────────────────────────────────────────────────┐
│                    SECURITY ARCHITECTURE                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Network Security                                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Cloudflare Tunnel (Argo)                          │     │
│  │  ├─ DDoS Protection                                │     │
│  │  ├─ SSL/TLS Termination                            │     │
│  │  ├─ Web Application Firewall (WAF)                 │     │
│  │  └─ Bot Protection                                 │     │
│  └────────────────────────────────────────────────────┘     │
│                           │                                  │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────┐     │
│  │  UFW Firewall Rules                                │     │
│  │  ├─ Port 22: SSH (Restricted)                      │     │
│  │  ├─ Port 80: HTTP (Apache)                         │     │
│  │  ├─ Port 443: HTTPS (Cloudflare)                   │     │
│  │  ├─ Ports 3001-3005: Juice Shop Instances          │     │
│  │  └─ Port 3306: MySQL (Local only)                  │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  Container Isolation                                         │
│  ┌────────────────────────────────────────────────────┐     │
│  │  • Docker Network Isolation                        │     │
│  │  • Resource Limits (CPU/Memory)                    │     │
│  │  • Read-only Root Filesystem                      │     │
│  │  • Non-root User Execution                        │     │
│  │  • No Privileged Containers                       │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 📁 Directory Structure

```
┌──────────────────────────────────────────────────────────────┐
│                    FILESYSTEM LAYOUT                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  /                                                           │
│  ├── /var/                                                   │
│  │   ├── /www/                                               │
│  │   │   ├── /html/          # Apache DocumentRoot           │
│  │   │   │   ├── index.php   # CTF Landing Page              │
│  │   │   │   ├── register.php                                │
│  │   │   │   ├── login.php                                   │
│  │   │   │   ├── dashboard.php                               │
│  │   │   │   └── assets/                                     │
│  │   │   └── /ctf-platform/  # Platform Files                │
│  │   └── /lib/mysql/         # MySQL Data                    │
│  │                                                           │
│  ├── /home/                                                  │
│  │   └── /juice-shop/        # Docker Volumes                │
│  │                                                           │
│  ├── /root/                                                  │
│  │   ├── juice-custom-content/                               │
│  │   └── sql-injection-lab/                                  │
│  │                                                           │
│  └── /usr/local/bin/         # Docker & Tools                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Deployment Commands

```bash
# Docker Deployment for Each Instance
docker run -d \
  --name juice-user${N} \
  --restart unless-stopped \
  -p 300${N}:3000 \
  -e NODE_ENV=ctf \
  bkimminich/juice-shop:latest

# Database Schema
CREATE DATABASE ctf_platform;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    email_verified BOOLEAN DEFAULT 0,
    instance_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📈 Scaling Considerations

```
┌──────────────────────────────────────────────────────────────┐
│                    SCALING ARCHITECTURE                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Current: 5 Users                                            │
│  ├─ 1 VPS Server                                             │
│  ├─ 5 Docker Containers                                      │
│  └─ ~2GB RAM Usage                                           │
│                                                              │
│  Scale to 25 Users:                                          │
│  ├─ Upgrade to 8GB RAM                                       │
│  ├─ Add Docker Swarm                                         │
│  └─ Implement Redis Cache                                    │
│                                                              │
│  Scale to 100+ Users:                                        │
│  ├─ Multiple VPS Servers                                     │
│  ├─ Kubernetes Orchestration                                 │
│  ├─ Load Balancer (HAProxy)                                  │
│  ├─ Shared Storage (NFS/S3)                                  │
│  └─ Monitoring (Prometheus/Grafana)                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

```
User Browser → Cloudflare → VPS Server → Apache/PHP → MySQL
                                ↓
                         Docker Container
                                ↓
                         Juice Shop App
                                ↓
                         SQLite (per instance)
```

## 📝 Configuration Files

- **Docker**: `/etc/docker/daemon.json`
- **Apache**: `/etc/apache2/sites-available/000-default.conf`
- **MySQL**: `/etc/mysql/mysql.conf.d/mysqld.cnf`
- **UFW**: `/etc/ufw/rules.v4`
- **PHP**: `/etc/php/8.1/apache2/php.ini`
- **Cloudflare**: `~/.cloudflared/config.yml`

This architecture supports 5 concurrent users with room for growth!