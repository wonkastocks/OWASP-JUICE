#!/usr/bin/env python3
"""
8-Hour Password Cracking Script for OWASP Juice Shop
Runs multiple strategies for up to 8 hours to crack remaining MD5 hashes
"""

import hashlib
import itertools
import time
import signal
import sys
import os
import random
import string
from datetime import datetime, timedelta
import threading
import json

# Configuration
MAX_RUNTIME_HOURS = 8
SAVE_INTERVAL = 60  # Save progress every 60 seconds
PROGRESS_FILE = "crack_progress.json"
RESULTS_FILE = "cracked_passwords_8hr.txt"
LOG_FILE = f"crack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Remaining uncracked hashes
UNCRACKED_HASHES = {
    "bjoern.kimminich@gmail.com": "6edd9d726cbdc873c539e41ae8757b8c",
    "ciso@juice-sh.op": "861917d5fa5f1172f931dc700d81a8fb",
    "support@juice-sh.op": "3869433d74e3d0c86fd25562f836bc82",
    "morty@juice-sh.op": "f2f933d0bb0ba057bc8e33b8ebd6d9e8",
    "J12934@juice-sh.op": "3c2abc04e4a6ea8f1327d0aae3714b7d",
    "wurstbrot@juice-sh.op": "9ad5b0492bbe528583e128d2a8941de4",
    "bjoern@juice-sh.op": "7f311911af16fa8f418dd1a3051d6810",
    "bjoern@owasp.org": "9283f1b2e9669749081963be0462e466",
    "chris.pike@juice-sh.op": "10a783b9ed19ea1c67c3a27699f0095b",
    "accountant@juice-sh.op": "963e10f92a70b4b463220cb4c5d636dc",
    "uvogin@juice-sh.op": "05f92148b4b60f7dacd04cceebb8f1af",
    "john@juice-sh.op": "00479e957b6b42c459ee5746478e4d45",
    "emma@juice-sh.op": "402f1c4a75e316afec5a6ea63147f739",
    "stan@juice-sh.op": "e9048a3f43dd5e094ef733f3bd88ea64",
    "testing@juice-sh.op": "b616a64605a07941fbd31868aea3b54b"
}

class PasswordCracker:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = self.start_time + (MAX_RUNTIME_HOURS * 3600)
        self.attempts = 0
        self.found_passwords = {}
        self.current_strategy = ""
        self.should_stop = False
        self.last_save = time.time()
        self.hash_lookup = {v: k for k, v in UNCRACKED_HASHES.items()}
        
        # Load previous progress if exists
        self.load_progress()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown gracefully"""
        print("\n🛑 Stopping gracefully...")
        self.should_stop = True
        self.save_progress()
        self.print_summary()
        sys.exit(0)
    
    def log(self, message):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(LOG_FILE, 'a') as f:
            f.write(log_msg + "\n")
    
    def check_password(self, password):
        """Check if password matches any uncracked hash"""
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        if password_hash in self.hash_lookup:
            user = self.hash_lookup[password_hash]
            if user not in self.found_passwords:
                self.found_passwords[user] = password
                self.log(f"🔓 CRACKED: {user} : {password}")
                self.save_found_password(user, password)
                
                # Remove from uncracked list
                del self.hash_lookup[password_hash]
                
                return True
        return False
    
    def save_found_password(self, user, password):
        """Save found password immediately"""
        with open(RESULTS_FILE, 'a') as f:
            f.write(f"{datetime.now()} - {user}:{password}\n")
    
    def save_progress(self):
        """Save current progress to file"""
        progress = {
            'start_time': self.start_time,
            'attempts': self.attempts,
            'found_passwords': self.found_passwords,
            'current_strategy': self.current_strategy,
            'runtime': time.time() - self.start_time
        }
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)
        self.last_save = time.time()
    
    def load_progress(self):
        """Load previous progress if exists"""
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    progress = json.load(f)
                    self.found_passwords = progress.get('found_passwords', {})
                    self.log(f"Loaded {len(self.found_passwords)} previously found passwords")
                    
                    # Remove already found from hash lookup
                    for user in self.found_passwords:
                        if user in UNCRACKED_HASHES:
                            hash_val = UNCRACKED_HASHES[user]
                            if hash_val in self.hash_lookup:
                                del self.hash_lookup[hash_val]
            except:
                pass
    
    def should_continue(self):
        """Check if should continue running"""
        if self.should_stop:
            return False
        if len(self.hash_lookup) == 0:
            self.log("✅ All passwords cracked!")
            return False
        if time.time() >= self.end_time:
            self.log("⏰ 8-hour time limit reached")
            return False
        
        # Save progress periodically
        if time.time() - self.last_save > SAVE_INTERVAL:
            self.save_progress()
        
        return True
    
    def strategy_dictionary(self):
        """Strategy 1: Dictionary attack with common passwords"""
        self.current_strategy = "Dictionary Attack"
        self.log(f"Starting {self.current_strategy}...")
        
        # Extended wordlist
        wordlist = [
            # Common passwords
            "password", "123456", "password123", "12345678", "qwerty", "abc123",
            "monkey", "1234567", "letmein", "trustno1", "dragon", "baseball",
            "111111", "iloveyou", "master", "sunshine", "ashley", "bailey",
            "passw0rd", "shadow", "123123", "654321", "superman", "qazwsx",
            
            # Juice Shop specific
            "juice", "juiceshop", "owasp", "ctf", "security", "hack", "admin",
            "test", "demo", "guest", "user", "root", "toor", "secret",
            
            # Character names (Rick and Morty theme for morty@)
            "rick", "morty", "summer", "beth", "jerry", "birdperson", "squanch",
            "pickle", "schwifty", "wubba", "lubba", "portal", "c137",
            
            # Star Trek theme (for chris.pike@)
            "enterprise", "captain", "pike", "spock", "kirk", "bones", "uhura",
            "scotty", "sulu", "chekov", "tribble", "klingon", "vulcan",
            
            # German words (for wurstbrot@, bjoern@)
            "wurst", "brot", "wurstbrot", "bier", "deutschland", "kartoffel",
            "sauerkraut", "bratwurst", "schnitzel", "apfelstrudel",
            
            # Accounting theme (for accountant@)
            "money", "cash", "profit", "ledger", "balance", "debit", "credit",
            "account", "finance", "budget", "revenue", "expense",
            
            # Hunter x Hunter theme (for uvogin@)
            "hunter", "phantom", "troupe", "spider", "nen", "gon", "killua",
            "kurapika", "leorio", "hisoka", "chrollo", "uvogin",
            
            # Support theme
            "support", "help", "ticket", "helpdesk", "service", "assist",
            
            # Years
            "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"
        ]
        
        # Try each word with variations
        for word in wordlist:
            if not self.should_continue():
                return
            
            variations = [
                word,
                word.capitalize(),
                word.upper(),
                word + "123",
                word + "1234",
                word + "!",
                word + "@",
                word + "#",
                word + "2019",
                word + "2020",
                word + "2021",
                word + "2022",
                word + "2023",
                word + "2024",
                "123" + word,
                word[::-1],  # reversed
            ]
            
            for variant in variations:
                self.attempts += 1
                if self.attempts % 10000 == 0:
                    self.log(f"Attempts: {self.attempts:,} | Strategy: {self.current_strategy}")
                
                if self.check_password(variant):
                    self.log(f"Found using dictionary: {variant}")
    
    def strategy_mutations(self):
        """Strategy 2: Username-based mutations"""
        self.current_strategy = "Username Mutations"
        self.log(f"Starting {self.current_strategy}...")
        
        for user in list(self.hash_lookup.values()):
            if not self.should_continue():
                return
            
            # Extract username part
            username = user.split('@')[0]
            parts = username.split('.')
            
            # Generate mutations
            mutations = []
            mutations.append(username)
            mutations.extend(parts)
            
            for part in parts:
                mutations.extend([
                    part, part.capitalize(), part.upper(),
                    part + "123", part + "1234", part + "12345",
                    part + "!", part + "@", part + "#",
                    part + "2019", part + "2020", part + "2021",
                    part + "2022", part + "2023", part + "2024",
                ])
            
            # Try combinations of parts
            if len(parts) > 1:
                mutations.append(''.join(parts))
                mutations.append(''.join(parts[::-1]))
                mutations.append('_'.join(parts))
                mutations.append('-'.join(parts))
            
            for mutation in mutations:
                self.attempts += 1
                if self.check_password(mutation):
                    self.log(f"Found using mutation: {mutation}")
    
    def strategy_patterns(self):
        """Strategy 3: Common password patterns"""
        self.current_strategy = "Pattern Attack"
        self.log(f"Starting {self.current_strategy}...")
        
        # Common patterns
        patterns = [
            # Word + numbers
            ("password", range(0, 10000)),
            ("admin", range(0, 10000)),
            ("juice", range(0, 10000)),
            ("test", range(0, 10000)),
            ("user", range(0, 10000)),
            
            # Letter + numbers
            ("a", range(0, 100000)),
            ("p", range(0, 100000)),
            ("q", range(0, 100000)),
        ]
        
        for base, numbers in patterns:
            if not self.should_continue():
                return
            
            for num in numbers:
                password = f"{base}{num}"
                self.attempts += 1
                
                if self.attempts % 50000 == 0:
                    self.log(f"Attempts: {self.attempts:,} | Testing: {password}")
                
                if self.check_password(password):
                    self.log(f"Found using pattern: {password}")
    
    def strategy_bruteforce_short(self):
        """Strategy 4: Brute force short passwords"""
        self.current_strategy = "Brute Force (1-6 chars)"
        self.log(f"Starting {self.current_strategy}...")
        
        # Characters to use
        chars = string.ascii_lowercase + string.digits
        
        # Try all combinations up to 4 characters
        for length in range(1, 5):
            if not self.should_continue():
                return
            
            self.log(f"Trying {length} character passwords...")
            
            for combo in itertools.product(chars, repeat=length):
                if not self.should_continue():
                    return
                
                password = ''.join(combo)
                self.attempts += 1
                
                if self.attempts % 100000 == 0:
                    self.log(f"Attempts: {self.attempts:,} | Testing: {password}")
                
                if self.check_password(password):
                    self.log(f"Found using brute force: {password}")
    
    def strategy_leetspeak(self):
        """Strategy 5: Leetspeak variations"""
        self.current_strategy = "Leetspeak Variations"
        self.log(f"Starting {self.current_strategy}...")
        
        leet_map = {
            'a': ['4', '@'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['5', '$'],
            't': ['7'],
            'l': ['1'],
            'g': ['9']
        }
        
        base_words = [
            "password", "admin", "juice", "hack", "leet", "elite",
            "master", "secret", "security", "owasp", "phantom",
            "troupe", "hunter", "morty", "rick", "support"
        ]
        
        for word in base_words:
            if not self.should_continue():
                return
            
            # Generate leet variations
            positions = []
            for i, char in enumerate(word):
                if char in leet_map:
                    positions.append((i, char, leet_map[char]))
            
            # Try different combinations
            for r in range(len(positions) + 1):
                for combo in itertools.combinations(positions, r):
                    password = list(word)
                    for pos, _, replacements in combo:
                        password[pos] = random.choice(replacements)
                    
                    password_str = ''.join(password)
                    self.attempts += 1
                    
                    if self.check_password(password_str):
                        self.log(f"Found using leetspeak: {password_str}")
                    
                    # Also try with numbers
                    for suffix in ['', '1', '12', '123', '1234', '!', '@']:
                        self.attempts += 1
                        if self.check_password(password_str + suffix):
                            self.log(f"Found using leetspeak: {password_str + suffix}")
    
    def strategy_keyboard_patterns(self):
        """Strategy 6: Keyboard pattern passwords"""
        self.current_strategy = "Keyboard Patterns"
        self.log(f"Starting {self.current_strategy}...")
        
        patterns = [
            "qwerty", "qwertyuiop", "asdfgh", "asdfghjkl", "zxcvbn", "zxcvbnm",
            "123qwe", "qwe123", "qazwsx", "qazxsw", "qweasd", "asdqwe",
            "zaq1xsw2", "xsw2cde3", "1qaz2wsx", "2wsx3edc", "!QAZ@WSX",
            "poiuyt", "lkjhgf", "mnbvcx", "098765", "987654", "456789",
            "qwert12345", "asdfg12345", "zxcvb12345", "1234qwer", "1234asdf"
        ]
        
        for pattern in patterns:
            if not self.should_continue():
                return
            
            variations = [
                pattern,
                pattern.upper(),
                pattern.capitalize(),
                pattern[::-1],
                pattern + "!",
                pattern + "@",
                pattern + "#",
                pattern + "123",
                "123" + pattern
            ]
            
            for variant in variations:
                self.attempts += 1
                if self.check_password(variant):
                    self.log(f"Found using keyboard pattern: {variant}")
    
    def strategy_dates(self):
        """Strategy 7: Date-based passwords"""
        self.current_strategy = "Date Patterns"
        self.log(f"Starting {self.current_strategy}...")
        
        # Common date formats
        for year in range(1970, 2026):
            if not self.should_continue():
                return
            
            for month in range(1, 13):
                for day in range(1, 32):
                    # Different formats
                    dates = [
                        f"{year}{month:02d}{day:02d}",
                        f"{day:02d}{month:02d}{year}",
                        f"{month:02d}{day:02d}{year}",
                        f"{year}-{month:02d}-{day:02d}",
                        f"{day:02d}/{month:02d}/{year}",
                    ]
                    
                    for date_str in dates:
                        self.attempts += 1
                        if self.attempts % 100000 == 0:
                            self.log(f"Attempts: {self.attempts:,} | Testing dates...")
                        
                        if self.check_password(date_str):
                            self.log(f"Found using date: {date_str}")
    
    def strategy_random(self):
        """Strategy 8: Random generation with common patterns"""
        self.current_strategy = "Random Generation"
        self.log(f"Starting {self.current_strategy}...")
        
        while self.should_continue():
            # Generate random passwords with different patterns
            patterns = [
                # Random lowercase
                lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8))),
                # Random with digits
                lambda: ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(4, 10))),
                # Word + number
                lambda: random.choice(['admin', 'pass', 'test', 'user', 'juice']) + str(random.randint(0, 9999)),
                # Special pattern
                lambda: random.choice(['!', '@', '#', '$']) + ''.join(random.choices(string.ascii_letters, k=6)),
            ]
            
            password = random.choice(patterns)()
            self.attempts += 1
            
            if self.attempts % 100000 == 0:
                self.log(f"Attempts: {self.attempts:,} | Random: {password}")
            
            if self.check_password(password):
                self.log(f"Found using random: {password}")
    
    def print_summary(self):
        """Print final summary"""
        runtime = time.time() - self.start_time
        hours = int(runtime // 3600)
        minutes = int((runtime % 3600) // 60)
        seconds = int(runtime % 60)
        
        self.log("\n" + "="*60)
        self.log("CRACKING SESSION COMPLETE")
        self.log("="*60)
        self.log(f"Runtime: {hours}h {minutes}m {seconds}s")
        self.log(f"Total attempts: {self.attempts:,}")
        self.log(f"Passwords cracked: {len(self.found_passwords)}")
        self.log(f"Remaining uncracked: {len(self.hash_lookup)}")
        
        if self.found_passwords:
            self.log("\n🔓 Cracked Passwords:")
            for user, password in self.found_passwords.items():
                self.log(f"  {user} : {password}")
        
        if self.hash_lookup:
            self.log("\n❌ Still Uncracked:")
            for user in self.hash_lookup.values():
                self.log(f"  {user}")
        
        self.log(f"\nResults saved to: {RESULTS_FILE}")
        self.log(f"Log saved to: {LOG_FILE}")
        self.log(f"Progress saved to: {PROGRESS_FILE}")
    
    def run(self):
        """Main execution loop"""
        self.log("="*60)
        self.log("8-HOUR PASSWORD CRACKING SESSION STARTED")
        self.log("="*60)
        self.log(f"Target hashes: {len(self.hash_lookup)}")
        self.log(f"Max runtime: {MAX_RUNTIME_HOURS} hours")
        self.log(f"Press Ctrl+C to stop gracefully\n")
        
        # Run strategies in order
        strategies = [
            self.strategy_dictionary,
            self.strategy_mutations,
            self.strategy_leetspeak,
            self.strategy_keyboard_patterns,
            self.strategy_patterns,
            self.strategy_dates,
            self.strategy_bruteforce_short,
            self.strategy_random,
        ]
        
        for strategy in strategies:
            if not self.should_continue():
                break
            strategy()
        
        # Final summary
        self.print_summary()

def main():
    """Main entry point"""
    print("🔐 OWASP Juice Shop - 8 Hour Password Cracker")
    print("="*60)
    
    cracker = PasswordCracker()
    
    try:
        cracker.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        cracker.print_summary()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        cracker.save_progress()
        cracker.print_summary()

if __name__ == "__main__":
    main()