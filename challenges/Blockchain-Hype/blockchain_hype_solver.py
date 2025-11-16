#!/usr/bin/env python3
"""
Blockchain Hype Challenge Solver
================================
Automated discovery of hidden blockchain/token sale information in Juice Shop.

Target: Juice Shop instance
Challenge: Find token sale information before official announcement

Usage:
    python3 blockchain_hype_solver.py
"""

import requests
import re
import time
import sys
import json
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================================
# CONFIGURATION - Change these values for your Juice Shop instance
# ============================================================================

# Change this URL to your Juice Shop instance
JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

# Blockchain/crypto-related paths to test
BLOCKCHAIN_PATHS = [
    # Directories
    "blockchain/", "token/", "ico/", "sale/", "tokensale/", "crypto/",
    "nft/", "web3/", "defi/", "coin/", "tokenomics/", "fundraising/",

    # Files
    "whitepaper.pdf", "tokensale.pdf", "tokenomics.pdf", "roadmap.pdf",
    "announcement.html", "press-release.pdf", "investor-deck.pdf",
    "token-sale.html", "blockchain.html", "crypto.html",

    # Hidden paths
    ".well-known/blockchain", "_blockchain/", "hidden/token/",
    "draft/tokensale/", "preview/announcement/", "test/ico/",

    # Admin/internal
    "admin/blockchain/", "internal/tokensale/", "management/ico/",

    # API endpoints
    "api/blockchain", "api/token", "api/ico", "rest/blockchain",
    "rest/token", "rest/tokensale",
]

# Keywords that indicate token sale information
TOKEN_SALE_KEYWORDS = [
    "token sale", "ico", "initial coin offering", "tokenomics",
    "smart contract", "ethereum", "blockchain", "whitepaper",
    "presale", "crowdsale", "fundraising", "investment",
    "token distribution", "total supply", "market cap"
]

# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class BlockchainHypeSolver:
    """Blockchain Hype Challenge solver"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.found_content = []
        self.tested_paths = 0

    def print_banner(self):
        """Print challenge banner"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  BLOCKCHAIN HYPE CHALLENGE SOLVER{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Target: {Colors.BOLD}{self.base_url}{Colors.ENDC}")
        print(f"{Colors.CYAN}Objective: Find token sale information before announcement{Colors.ENDC}\n")

    def test_blockchain_path(self, path):
        """Test if a blockchain-related path contains relevant information"""
        url = urljoin(self.base_url, path)

        try:
            response = self.session.get(url, timeout=10)
            self.tested_paths += 1

            if response.status_code == 200:
                content = response.text

                # Check if content contains token sale information
                content_lower = content.lower()
                keyword_matches = sum(1 for keyword in TOKEN_SALE_KEYWORDS
                                    if keyword.lower() in content_lower)

                # Consider it relevant if multiple keywords found or specific indicators
                if (keyword_matches >= 2 or
                    'token sale' in content_lower or
                    'whitepaper' in content_lower or
                    'ico' in content_lower or
                    'smart contract' in content_lower):

                    info = {
                        'path': path,
                        'url': url,
                        'size': len(content),
                        'content': content,
                        'keyword_matches': keyword_matches,
                        'content_type': response.headers.get('content-type', 'unknown')
                    }

                    self.found_content.append(info)
                    return info

        except requests.exceptions.RequestException:
            pass

        return None

    def analyze_javascript_for_blockchain_refs(self):
        """Analyze JavaScript files for blockchain references"""
        print(f"{Colors.CYAN}🔍 Analyzing JavaScript for blockchain references...{Colors.ENDC}")

        # Get main JavaScript files
        js_files = ['main.js', 'app.js', 'vendor.js', 'bundle.js']
        blockchain_refs = []

        for js_file in js_files:
            try:
                js_url = urljoin(self.base_url, js_file)
                response = self.session.get(js_url, timeout=10)

                if response.status_code == 200:
                    content = response.text

                    # Search for blockchain-related patterns
                    patterns = [
                        r'"[^"]*(?:blockchain|token|ico|sale)[^"]*"',
                        r"'[^']*(?:blockchain|token|ico|sale)[^']*'",
                        r'path:\s*"[^"]*(?:blockchain|token|ico)[^"]*"',
                        r'route:\s*"[^"]*(?:blockchain|token|ico)[^"]*"',
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        for match in matches:
                            # Clean up the match
                            clean_match = match.strip('"\'')
                            if (len(clean_match) > 3 and
                                not clean_match.startswith('http') and
                                any(keyword in clean_match.lower() for keyword in
                                    ['blockchain', 'token', 'ico', 'sale', 'crypto', 'nft'])):
                                blockchain_refs.append(clean_match)

                    print(f"   Analyzed {js_file} ({len(content):,} chars)")

            except Exception as e:
                continue

        if blockchain_refs:
            unique_refs = list(set(blockchain_refs))
            print(f"{Colors.GREEN}   Found {len(unique_refs)} blockchain references{Colors.ENDC}")

            # Test these references as potential paths
            for ref in unique_refs[:10]:  # Test first 10
                if ref.startswith('/') or '/' in ref:
                    test_path = ref.lstrip('/')
                    result = self.test_blockchain_path(test_path)
                    if result:
                        print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found via JS analysis: {test_path}{Colors.ENDC}")
                        return True

        return False

    def check_robots_and_sitemap(self):
        """Check robots.txt and sitemap for blockchain references"""
        print(f"{Colors.CYAN}🤖 Checking robots.txt and sitemap...{Colors.ENDC}")

        # Check robots.txt
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            robots_response = self.session.get(robots_url)

            if robots_response.status_code == 200:
                robots_content = robots_response.text
                print(f"   Found robots.txt ({len(robots_content)} chars)")

                # Look for disallowed blockchain paths
                disallowed_lines = [line for line in robots_content.split('\n')
                                  if line.startswith('Disallow:')]

                blockchain_disallowed = []
                for line in disallowed_lines:
                    if any(keyword in line.lower() for keyword in
                          ['blockchain', 'token', 'ico', 'sale', 'crypto']):
                        path = line.split('Disallow:')[1].strip().lstrip('/')
                        blockchain_disallowed.append(path)

                if blockchain_disallowed:
                    print(f"{Colors.GREEN}   Found blockchain paths in robots.txt{Colors.ENDC}")

                    # Test disallowed paths
                    for path in blockchain_disallowed:
                        result = self.test_blockchain_path(path)
                        if result:
                            print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found via robots.txt: {path}{Colors.ENDC}")
                            return True

        except:
            pass

        return False

    def enumerate_blockchain_content(self):
        """Enumerate blockchain-related content"""
        print(f"{Colors.CYAN}🔍 Enumerating blockchain-related paths...{Colors.ENDC}")

        # Test predefined paths
        for path in BLOCKCHAIN_PATHS:
            result = self.test_blockchain_path(path)
            if result:
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found token sale info: {path}{Colors.ENDC}")
                return True

            if self.tested_paths % 20 == 0:
                print(f"   Tested {self.tested_paths} paths...")

            time.sleep(0.1)  # Rate limiting

        return False

    def solve_challenge(self):
        """Main method to solve the blockchain hype challenge"""
        self.print_banner()

        # Method 1: Check robots.txt and sitemap
        print(f"{Colors.CYAN}🔍 Phase 1: Checking robots.txt and sitemap...{Colors.ENDC}")
        if self.check_robots_and_sitemap():
            return True

        # Method 2: JavaScript analysis
        print(f"\n{Colors.CYAN}🔍 Phase 2: Analyzing JavaScript for references...{Colors.ENDC}")
        if self.analyze_javascript_for_blockchain_refs():
            return True

        # Method 3: Direct enumeration
        print(f"\n{Colors.CYAN}🔍 Phase 3: Direct path enumeration...{Colors.ENDC}")
        if self.enumerate_blockchain_content():
            return True

        print(f"\n{Colors.RED}❌ Challenge not completed automatically{Colors.ENDC}")
        print(f"{Colors.YELLOW}Tested {self.tested_paths} paths total{Colors.ENDC}")

        return False


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Use default URL - CHANGE THIS FOR YOUR INSTANCE
        base_url = JUICE_SHOP_URL

    print(f"{Colors.YELLOW}🎯 Starting Blockchain Hype Challenge{Colors.ENDC}")
    print(f"{Colors.YELLOW}Target: {base_url}{Colors.ENDC}")

    solver = BlockchainHypeSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}💡 Manual investigation suggestions:{Colors.ENDC}")
        print(f"1. Check robots.txt for disallowed blockchain paths")
        print(f"2. Search main.js for 'blockchain', 'token', 'ico' keywords")
        print(f"3. Look for PDF files (whitepaper.pdf, tokensale.pdf)")
        print(f"4. Check social media and GitHub for early announcements")

        print(f"\n{Colors.CYAN}🔧 Manual testing commands:{Colors.ENDC}")
        print(f"curl -I {base_url}/blockchain/")
        print(f"curl -I {base_url}/whitepaper.pdf")
        print(f"curl {base_url}/robots.txt")

if __name__ == '__main__':
    main()