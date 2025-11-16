# OWASP Juice Shop - 110 Challenge Documentation & Solutions

This repository contains comprehensive documentation, automated scripts, and detailed writeups for solving all 110 OWASP Juice Shop challenges.

## 🎯 Project Overview

Complete educational resource for mastering web application security through:
- Detailed writeups for all 110 challenges
- Automated solving scripts (Python, Shell, Expect)
- Security vulnerability analysis and explanations
- Real-world attack scenarios and mitigations
- CTF platform setup and deployment tools

## 📚 Documentation Structure

See **[OWASP_JUICE_SHOP_README.md](./OWASP_JUICE_SHOP_README.md)** for complete documentation.

### Key Resources
- **JUICE_SHOP_CHALLENGE_SUMMARY.md** - All challenges overview
- **COMPREHENSIVE_SECURITY_REPORT.md** - Security analysis
- **FINAL_WRITEUP.md** - Complete solutions
- **STUDENT_LAB_GUIDE.md** - Lab setup guide
- **CTF_STATUS_REPORT.md** - Progress tracking

### Challenge-Specific Writeups
- SQL Injection techniques and exploitation
- XSS (Stored, Reflected, DOM-based)
- JWT vulnerabilities and bypasses
- Blockchain & NFT security
- Authentication & Authorization bypasses
- CSRF, XXE, and more

## 🚀 Quick Start

### Deploy Juice Shop
```bash
# Using Docker
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 bkimminich/juice-shop

# Or use included deployment script
./deploy_juice_docker.sh
```

### Run Automated Solvers
```bash
python master_juice_shop_solver.py
python advanced_challenges_solver.py
python complete_all_challenges.py
```

## 📊 110 Challenges Organized By

### Difficulty Levels
- ⭐ 1-Star (Trivial)
- ⭐⭐ 2-Star (Easy)
- ⭐⭐⭐ 3-Star (Medium)
- ⭐⭐⭐⭐ 4-Star (Hard)
- ⭐⭐⭐⭐⭐ 5-Star (Expert)
- ⭐⭐⭐⭐⭐⭐ 6-Star (Bonus)

### Vulnerability Categories
1. Broken Access Control
2. Broken Authentication
3. Sensitive Data Exposure
4. XXE (XML External Entities)
5. Broken Anti Automation
6. XSS (Cross-Site Scripting)
7. Insecure Deserialization
8. Vulnerable Components
9. Security Misconfiguration
10. Injection (SQL, NoSQL, Command)
11. Cryptographic Issues
12. Improper Input Validation
13. Security Through Obscurity
14. Unvalidated Redirects

## 🛠️ Tools & Scripts

### Automated Solvers
- `master_juice_shop_solver.py` - Complete automation
- `advanced_challenges_solver.py` - Advanced techniques
- `juice_solver.py` - Core solver
- Category-specific solvers (SQL, XSS, JWT, etc.)

### Deployment & Setup
- `deploy_juice_docker.sh` - Docker deployment
- `deploy_multijuicer.sh` - Multi-user environment
- `setup_vulnerable_lab.sh` - Full lab setup
- `setup_registration_platform.sh` - CTF platform

### Challenge-Specific Scripts
- **SQL Injection**: `juice5_sqli_exploit.py`
- **XSS**: `dom_xss_playwright.py`, `bonus_payload_solver.py`
- **JWT**: `advanced_jwt_solver.py`
- **NFT**: `juice5-nft-takeover.py`
- **Chatbot**: `bully_chatbot_solver.py`
- And many more...

## 🎓 Educational Value

Perfect for:
- Security students learning web application security
- Penetration testers practicing skills
- Developers understanding vulnerabilities
- CTF competitors preparing
- Security trainers teaching

## 🔒 Security Notice

**⚠️ EDUCATIONAL USE ONLY**

Authorized environments only:
- Personal local instances
- Authorized penetration tests
- CTF competitions
- Security training labs
- Research with authorization

Never use on production systems or without explicit permission.

## 📁 Repository Structure

```
OWASP-JUICE/
├── docs/                         # Documentation
│   └── OWASP_JUICE_SHOP_README.md
├── guides/                       # Learning guides
│   ├── COMPREHENSIVE_STUDY_GUIDE.md
│   └── ATTACK_METHODOLOGY_GUIDE.md
├── solvers/                      # Automated solvers
│   ├── complete_juice_shop_solver.py
│   └── comprehensive_writeup_generator.py
├── challenge_writeups/           # Individual challenge writeups (79+)
│   ├── Broken_Access_Control/
│   ├── Broken_Authentication/
│   ├── Injection/
│   ├── XSS_Cross-Site_Scripting/
│   └── ... (14 categories total)
├── challenges/                   # Legacy challenge files
├── Challenge-Scripts/            # Legacy solver scripts
└── README.md                     # This file
```

## 🏆 Progress Tracking

- Built-in Score Board: `http://localhost:3000/#/score-board`
- Manual tracking: `CTF_STATUS_REPORT.md`
- Automated: `python check_scoreboard.py`

**Current Progress: 0/110 challenges**

## 💡 Learning Path

Recommended approach:
1. Start with 1-2 star challenges
2. Progress through 3-4 star challenges
3. Tackle 5-6 star expert challenges
4. Document your solutions
5. Automate with scripts
6. Share knowledge

## 📖 Resources

- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
- [Official GitHub](https://github.com/juice-shop/juice-shop)
- [Solution Guide](https://pwning.owasp-juice.shop/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## 🔧 Prerequisites

- Docker (recommended)
- Python 3.x
- Node.js
- Web browser (Chrome/Firefox)
- Optional: Burp Suite, OWASP ZAP, Postman

## ⚡ Quick Commands

```bash
# Check status
python check_scoreboard.py

# Deploy platform
./setup_registration_platform.sh

# Solve challenges
python master_solver.py

# Monitor progress
python check_bonus_status.py
```

---

**Remember: Use responsibly. Ethical hacking only.**
