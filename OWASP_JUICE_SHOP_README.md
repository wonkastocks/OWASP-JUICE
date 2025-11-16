# OWASP Juice Shop - 110 Challenge Documentation

This repository contains all the code, scripts, artifacts, and documentation for solving the 110 OWASP Juice Shop challenges.

## Repository Purpose

This repository serves as a comprehensive documentation and automation toolkit for completing all OWASP Juice Shop CTF challenges. It includes:
- Challenge solving scripts (Python, JavaScript, Shell)
- Documentation and writeups for each challenge
- Deployment and setup scripts
- Monitoring and testing tools

## Challenge Categories

OWASP Juice Shop contains 110 challenges across multiple difficulty levels:

### Difficulty Levels
- ⭐ **1-Star** (Trivial)
- ⭐⭐ **2-Star** (Easy)
- ⭐⭐⭐ **3-Star** (Medium)
- ⭐⭐⭐⭐ **4-Star** (Hard)
- ⭐⭐⭐⭐⭐ **5-Star** (Expert)
- ⭐⭐⭐⭐⭐⭐ **6-Star** (Bonus)

### Challenge Categories
1. **Broken Access Control**
2. **Broken Authentication**
3. **Sensitive Data Exposure**
4. **XXE (XML External Entities)**
5. **Broken Anti Automation**
6. **XSS (Cross-Site Scripting)**
7. **Insecure Deserialization**
8. **Vulnerable Components**
9. **Security Misconfiguration**
10. **Injection**
11. **Cryptographic Issues**
12. **Improper Input Validation**
13. **Security Through Obscurity**
14. **Unvalidated Redirects**

## Documentation Files

### Main Documentation
- `JUICE_SHOP_CHALLENGE_SUMMARY.md` - Overview of all challenges
- `COMPREHENSIVE_SECURITY_REPORT.md` - Detailed security analysis
- `FINAL_WRITEUP.md` - Complete challenge writeup
- `FINAL_PROGRESS_REPORT.md` - Progress tracking
- `CTF_STATUS_REPORT.md` - CTF platform status

### Specific Challenge Writeups
- `Blockchain-Hype-Challenge.md` - Blockchain-related challenge
- `Forged-Coupon-Challenge.md` - Coupon forgery challenge
- `Leaked-Access-Logs-Challenge.md` - Access log exposure
- `Unsigned-JWT-Challenge.md` - JWT security challenge
- `SQL_INJECTION_WALKTHROUGH.md` - SQL injection guide
- `F12-SPA-Route-Discovery-Walkthrough.md` - SPA route discovery
- `forged-feedback-instructions.md` - Feedback manipulation

### Technical Guides
- `SPA-Security-Hackers-Guide.md` - Single Page Application security
- `SPA-vs-Traditional-Websites.md` - Architecture comparison
- `Tech-Stack-Comparison-JuiceShop-vs-Airbnb.md` - Tech stack analysis
- `juice_shop_architecture.md` - Application architecture
- `about_content_documentation.md` - About page documentation
- `admin_panel_documentation.md` - Admin panel details

### Setup and Deployment
- `DEPLOY_INSTRUCTIONS.md` - Deployment guide
- `STUDENT_LAB_GUIDE.md` - Lab setup for students
- `WALLYS_DEMO_GUIDE.md` - Demo environment guide
- `complete_platform_documentation.md` - Platform documentation

## Scripts and Tools

### Python Solvers
- `master_juice_shop_solver.py` - Master solver for all challenges
- `master_solver.py` - Comprehensive solver
- `complete_all_challenges.py` - Automated challenge completion
- `advanced_challenges_solver.py` - Advanced challenge automation
- `advanced_scoreboard_solver.py` - Scoreboard manipulation
- `advanced_solver.py` - Advanced techniques

### Specific Challenge Solvers
- **SQL Injection**: `juice5_sqli_exploit.py`, `juice_shop_sqli_demo.py`
- **JWT**: `advanced_jwt_solver.py`
- **XSS**: `bonus_payload_solver.py`, `solve_bonus_xss.py`, `dom_xss_*.py`
- **Chatbot**: `bully_chatbot_*.py`, `chatbot_coupon_solver.py`
- **NFT**: `juice5-nft-takeover.py`, `nft-takeover-*.py`
- **Privacy**: `privacy_policy_solver.py`, `browser_privacy_solver.py`
- **Admin**: `admin_test.py`, `admin_verify.py`

### Deployment Scripts
- `deploy_juice_docker.sh` - Docker deployment
- `deploy_multijuicer.sh` - Multi-user deployment
- `setup_registration_platform.sh` - Registration system
- `setup_vulnerable_lab.sh` - Lab environment setup
- `install_juiceshop_apache.sh` - Apache installation

### Monitoring and Testing
- `check_scoreboard.py` - Check challenge completion status
- `check_bonus_status.py` - Bonus challenge tracking
- `mark_challenges_solved.py` - Mark challenges as completed
- `exploit_challenge_api.py` - API exploitation

## Quick Start

### 1. Install OWASP Juice Shop
```bash
# Docker installation
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 bkimminich/juice-shop

# Or use the deployment scripts
./deploy_juice_docker.sh
```

### 2. Access the Application
- Main App: http://localhost:3000
- Score Board: http://localhost:3000/#/score-board

### 3. Run Automated Solvers
```bash
# Run master solver
python master_juice_shop_solver.py

# Run specific category solvers
python advanced_challenges_solver.py
```

## Challenge Tracking

Track your progress using:
1. The built-in Score Board at `/#/score-board`
2. `CTF_STATUS_REPORT.md` - Manual tracking
3. `check_scoreboard.py` - Automated checking

## Credentials and Access

See `CTF_PLATFORM_CREDENTIALS.md` and `WORKING_CREDENTIALS.md` for access information.

## Security Considerations

⚠️ **Important**: This repository contains tools for educational purposes only. Use only on:
- Your own local instances
- Authorized testing environments
- CTF competitions
- Security training labs

Never use these tools against production systems or without explicit authorization.

## Educational Value

This repository demonstrates:
- Common web application vulnerabilities
- OWASP Top 10 security issues
- Secure coding practices (by showing what NOT to do)
- Penetration testing methodologies
- Security automation techniques

## Contributing

If you solve a challenge in a new way or find improvements:
1. Document your approach
2. Create a script if possible
3. Add writeup to the appropriate markdown file
4. Update this README with your contribution

## Resources

- [OWASP Juice Shop Official](https://owasp.org/www-project-juice-shop/)
- [Juice Shop GitHub](https://github.com/juice-shop/juice-shop)
- [Challenge Solutions Book](https://pwning.owasp-juice.shop/)

## Progress Tracking

Use this section to track your challenge completion:

### Completed Challenges: 0/110

- [ ] Broken Access Control
- [ ] Broken Authentication
- [ ] Sensitive Data Exposure
- [ ] XXE
- [ ] Broken Anti Automation
- [ ] XSS
- [ ] Insecure Deserialization
- [ ] Vulnerable Components
- [ ] Security Misconfiguration
- [ ] Injection
- [ ] Cryptographic Issues
- [ ] Improper Input Validation
- [ ] Security Through Obscurity
- [ ] Unvalidated Redirects

---

**Note**: This repository is for educational and ethical hacking purposes only. Always obtain proper authorization before testing any system.
