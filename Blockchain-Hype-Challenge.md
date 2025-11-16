# Blockchain Hype Challenge - OWASP Juice Shop

## Complete Security Analysis and Exploitation Guide

---

## Table of Contents

1. [Challenge Overview](#challenge-overview)
2. [Vulnerability Introduction](#vulnerability-introduction)
3. [CVSS Analysis](#cvss-analysis)
4. [Manual Exploitation](#manual-exploitation)
5. [Automated Python Script](#automated-python-script)
6. [Mitigation Strategies](#mitigation-strategies)
7. [References](#references)

---

## Challenge Overview

**Challenge Name**: Blockchain Hype
**Difficulty**: ⭐⭐⭐⭐ (4/6)
**Category**: Security through Obscurity
**Target Instance**: https://juice5.wonkatech.org/#/ *(Change to your instance)*

**Objective**: Learn about the Token Sale before its official announcement.

---

## Vulnerability Introduction

### What is Security through Obscurity?

**Security through Obscurity** is a flawed security principle that relies on keeping implementation details secret rather than using strong security mechanisms. In web applications, this often manifests as:

1. **Hidden endpoints** that are "secret" but not properly secured
2. **Undocumented features** accessible through direct URLs
3. **Development/staging content** left in production
4. **Marketing materials** or announcements published early
5. **Configuration files** with sensitive information exposed

### Blockchain/Token Sale Context

**Token Sales** (ICOs - Initial Coin Offerings) are events where companies sell cryptocurrency tokens to raise funds. Information about token sales includes:

- **Token economics** - Price, total supply, distribution
- **Sale timeline** - Pre-sale, public sale dates
- **Whitepaper** - Technical details about the blockchain project
- **Team information** - Founders, developers, advisors
- **Smart contract addresses** - Ethereum contract addresses

**Why This Information is Valuable**:
- **Investment decisions** - Early access to token sale details
- **Market manipulation** - Insider information before public announcement
- **Security risks** - Smart contract vulnerabilities in early versions
- **Competitive intelligence** - Business strategy and roadmap

### Real-World Examples

**Information Disclosure in Blockchain Projects**:
- **Premature announcements** in hidden website sections
- **Test token contracts** deployed to mainnet with real addresses
- **Whitepaper drafts** accessible via direct URLs
- **Team information** exposed before official launch
- **Tokenomics details** in configuration files

---

## CVSS Analysis

### CVSS v3.1 Score: 5.3 (Medium)

**Vector String**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`

**Breakdown**:
- **Attack Vector (AV): Network (N)** - Accessible over the network
- **Attack Complexity (AC): Low (L)** - Simple enumeration techniques
- **Privileges Required (PR): None (N)** - No authentication required
- **User Interaction (UI): None (N)** - No user interaction needed
- **Scope (S): Unchanged (U)** - Impact within the application
- **Confidentiality (C): Low (L)** - Disclosure of non-critical business information
- **Integrity (I): None (N)** - Cannot modify data
- **Availability (A): None (N)** - No impact on system availability

**Simple Explanation**:
This is a **Medium severity** vulnerability because:
- 🔍 **Information disclosure** - Access to confidential business information
- 🔍 **No authentication required** - Anyone can access if they find the path
- 🔍 **Business impact** - Early access to sensitive announcements
- ⚠️ **Limited scope** - Only affects information confidentiality
- ⚠️ **No system compromise** - Cannot modify application or access user data

---

## Manual Exploitation

### Step 1: Understanding the Target

**Goal**: Find hidden information about a blockchain token sale before its official announcement.

**What to Look For**:
- Hidden pages with token sale information
- Draft announcements or press releases
- Whitepaper documents (PDF files)
- Team member information
- Token contract addresses
- Sale timeline and pricing

### Step 2: Directory Enumeration

**Common Blockchain/Token Sale Paths**:

```
/blockchain/
/token/
/ico/
/sale/
/tokensale/
/whitepaper/
/announcement/
/press/
/news/
/blog/
/investor/
/fundraising/
```

**File Types to Look For**:
```
whitepaper.pdf
tokensale.pdf
announcement.html
press-release.pdf
tokenomics.pdf
team.html
roadmap.pdf
```

### Step 3: Manual Enumeration

**Using Browser**:

1. **Try common blockchain-related paths**:
   ```
   https://juice5.wonkatech.org/blockchain/
   https://juice5.wonkatech.org/token/
   https://juice5.wonkatech.org/ico/
   https://juice5.wonkatech.org/whitepaper/
   ```

2. **Check for PDF documents**:
   ```
   https://juice5.wonkatech.org/whitepaper.pdf
   https://juice5.wonkatech.org/tokensale.pdf
   https://juice5.wonkatech.org/tokenomics.pdf
   ```

3. **Look for announcement pages**:
   ```
   https://juice5.wonkatech.org/announcement/
   https://juice5.wonkatech.org/press/
   https://juice5.wonkatech.org/news/token-sale
   ```

**Using curl**:
```bash
# Test blockchain-related directories
curl -I https://juice5.wonkatech.org/blockchain/
curl -I https://juice5.wonkatech.org/token/
curl -I https://juice5.wonkatech.org/ico/

# Test for PDF documents
curl -I https://juice5.wonkatech.org/whitepaper.pdf
curl -I https://juice5.wonkatech.org/tokensale.pdf

# Test hidden announcement pages
curl https://juice5.wonkatech.org/announcement/
curl https://juice5.wonkatech.org/token-sale/
```

### Step 4: Source Code Analysis

**Search JavaScript for References**:

1. **Download main.js**:
   ```bash
   curl https://juice5.wonkatech.org/main.js -o main.js
   ```

2. **Search for blockchain-related keywords**:
   ```bash
   grep -i "blockchain" main.js
   grep -i "token" main.js
   grep -i "ico" main.js
   grep -i "sale" main.js
   grep -i "whitepaper" main.js
   ```

3. **Look for hidden routes**:
   ```bash
   grep -oE 'path:"[^"]*(?:blockchain|token|ico|sale)[^"]*"' main.js
   grep -oE '"/[^"]*(?:blockchain|token|ico|sale)[^"]*"' main.js
   ```

### Step 5: Social Engineering & OSINT

**Open Source Intelligence Gathering**:

1. **Check social media** for early announcements
2. **GitHub repositories** for token contracts or documentation
3. **Domain registrations** for blockchain-related subdomains
4. **DNS enumeration** for hidden subdomains:
   ```bash
   # Subdomain enumeration
   nslookup blockchain.juice-sh.op
   nslookup token.juice-sh.op
   nslookup ico.juice-sh.op
   ```

### Step 6: Web Archive Investigation

**Wayback Machine Analysis**:

1. **Visit** [web.archive.org](https://web.archive.org/)
2. **Search for** your target domain
3. **Look for historical versions** that might have exposed token sale information
4. **Check for deleted pages** that contained announcements

**Example**:
```bash
# Check if pages were archived
curl "https://web.archive.org/cdx/search/cdx?url=juice-sh.op&matchType=domain&filter=statuscode:200&output=json"
```

### Step 7: Robots.txt and Sitemap Analysis

**Check robots.txt**:
```bash
curl https://juice5.wonkatech.org/robots.txt
```

**Look for**:
- Disallowed directories that might contain token sale info
- Sitemap references
- Hidden directories

**Example robots.txt**:
```
User-agent: *
Disallow: /blockchain/
Disallow: /token-sale/
Disallow: /announcement/
```

---

## Automated Python Script

```python
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
import os
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

        # Check sitemap.xml
        try:
            sitemap_url = urljoin(self.base_url, '/sitemap.xml')
            sitemap_response = self.session.get(sitemap_url)

            if sitemap_response.status_code == 200:
                sitemap_content = sitemap_response.text

                # Extract URLs containing blockchain keywords
                blockchain_urls = re.findall(r'<loc>([^<]*(?:blockchain|token|ico|sale)[^<]*)</loc>',
                                           sitemap_content, re.IGNORECASE)

                for url in blockchain_urls:
                    # Convert to relative path
                    path = url.replace(self.base_url, '').lstrip('/')
                    result = self.test_blockchain_path(path)
                    if result:
                        print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found via sitemap: {path}{Colors.ENDC}")
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

    def analyze_found_content(self, content_info):
        """Analyze found blockchain content for key information"""
        print(f"\n{Colors.CYAN}📋 Analyzing token sale content...{Colors.ENDC}")

        content = content_info['content']
        content_lower = content.lower()

        # Extract key information
        findings = {}

        # Look for token information
        token_patterns = {
            'Token Name': [r'token\s+name[:\s]+([^<\n,]+)', r'token[:\s]+([A-Z]{3,10})'],
            'Token Symbol': [r'symbol[:\s]+([A-Z]{3,10})', r'ticker[:\s]+([A-Z]{3,10})'],
            'Total Supply': [r'(?:total\s+)?supply[:\s]+([0-9,]+)', r'max\s+supply[:\s]+([0-9,]+)'],
            'Token Price': [r'price[:\s]+\$?([0-9.]+)', r'cost[:\s]+\$?([0-9.]+)'],
            'Sale Date': [r'sale\s+(?:date|start)[:\s]+([^<\n]+)', r'launch[:\s]+([^<\n]+)'],
            'Contract Address': [r'0x[a-fA-F0-9]{40}', r'contract[:\s]+(0x[a-fA-F0-9]{40})']
        }

        for category, patterns in token_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    findings[category] = matches[0] if isinstance(matches[0], str) else matches[0][0]
                    break

        # Look for team information
        if 'team' in content_lower or 'founder' in content_lower:
            findings['Team Info'] = 'Present in document'

        # Look for roadmap
        if 'roadmap' in content_lower or 'milestone' in content_lower:
            findings['Roadmap'] = 'Present in document'

        # Display findings
        if findings:
            print(f"{Colors.GREEN}🔍 Token Sale Information Found:{Colors.ENDC}")
            for category, info in findings.items():
                print(f"   {Colors.CYAN}{category}:{Colors.ENDC} {info}")
        else:
            print(f"{Colors.YELLOW}⚠️  Content found but no specific token details extracted{Colors.ENDC}")

        return findings

    def solve_challenge(self):
        """Main method to solve the blockchain hype challenge"""
        self.print_banner()

        # Method 1: Check robots.txt and sitemap
        print(f"{Colors.CYAN}🔍 Phase 1: Checking robots.txt and sitemap...{Colors.ENDC}")
        if self.check_robots_and_sitemap():
            if self.found_content:
                self.analyze_found_content(self.found_content[0])
            return True

        # Method 2: JavaScript analysis
        print(f"\n{Colors.CYAN}🔍 Phase 2: Analyzing JavaScript for references...{Colors.ENDC}")
        if self.analyze_javascript_for_blockchain_refs():
            return True

        # Method 3: Direct enumeration
        print(f"\n{Colors.CYAN}🔍 Phase 3: Direct path enumeration...{Colors.ENDC}")
        if self.enumerate_blockchain_content():
            if self.found_content:
                self.analyze_found_content(self.found_content[0])
            return True

        print(f"\n{Colors.RED}❌ Challenge not completed automatically{Colors.ENDC}")
        print(f"{Colors.YELLOW}Tested {self.tested_paths} paths total{Colors.ENDC}")

        return False


# Specialized scanner for different content types
class BlockchainContentScanner:
    """Specialized scanner for different types of blockchain content"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def scan_for_pdfs(self):
        """Scan specifically for PDF documents"""
        print(f"{Colors.CYAN}📄 Scanning for PDF documents...{Colors.ENDC}")

        pdf_names = [
            "whitepaper.pdf", "tokensale.pdf", "tokenomics.pdf",
            "roadmap.pdf", "announcement.pdf", "press-release.pdf",
            "investor-deck.pdf", "token-economics.pdf", "ico-details.pdf"
        ]

        for pdf_name in pdf_names:
            url = urljoin(self.base_url, pdf_name)

            try:
                response = self.session.head(url, timeout=5)

                if (response.status_code == 200 and
                    response.headers.get('content-type', '').startswith('application/pdf')):

                    print(f"{Colors.GREEN}✅ Found PDF: {pdf_name}{Colors.ENDC}")

                    # Download and analyze
                    pdf_response = self.session.get(url)
                    file_path = f"downloaded_{pdf_name}"

                    with open(file_path, 'wb') as f:
                        f.write(pdf_response.content)

                    print(f"   Downloaded to: {file_path}")
                    print(f"   Size: {len(pdf_response.content):,} bytes")
                    return True

            except:
                continue

        return False

    def scan_for_json_config(self):
        """Look for JSON configuration files with blockchain info"""
        print(f"{Colors.CYAN}⚙️ Scanning for configuration files...{Colors.ENDC}")

        config_paths = [
            "config/blockchain.json", "config/token.json",
            "blockchain.json", "token.json", "ico.json",
            "assets/config/blockchain.json", "data/token.json"
        ]

        for config_path in config_paths:
            try:
                url = urljoin(self.base_url, config_path)
                response = self.session.get(url, timeout=5)

                if response.status_code == 200:
                    try:
                        config_data = response.json()

                        # Look for blockchain-related configuration
                        config_str = json.dumps(config_data, indent=2)
                        if any(keyword.lower() in config_str.lower()
                              for keyword in TOKEN_SALE_KEYWORDS):

                            print(f"{Colors.GREEN}✅ Found blockchain config: {config_path}{Colors.ENDC}")
                            print(f"   Content preview:")
                            print(f"   {config_str[:300]}...")
                            return True

                    except:
                        # Not valid JSON, but might still contain blockchain info
                        if any(keyword.lower() in response.text.lower()
                              for keyword in TOKEN_SALE_KEYWORDS):

                            print(f"{Colors.GREEN}✅ Found blockchain data: {config_path}{Colors.ENDC}")
                            return True

            except:
                continue

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

    # Main solver
    solver = BlockchainHypeSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}🔍 Trying specialized scanners...{Colors.ENDC}")

        # Specialized content scanners
        content_scanner = BlockchainContentScanner(base_url)

        if content_scanner.scan_for_pdfs():
            print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED via PDF discovery!{Colors.ENDC}")
            success = True
        elif content_scanner.scan_for_json_config():
            print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED via config discovery!{Colors.ENDC}")
            success = True

    if not success:
        print(f"\n{Colors.CYAN}💡 Manual investigation suggestions:{Colors.ENDC}")
        print(f"1. Check robots.txt for disallowed blockchain paths")
        print(f"2. Search main.js for 'blockchain', 'token', 'ico' keywords")
        print(f"3. Look for PDF files (whitepaper.pdf, tokensale.pdf)")
        print(f"4. Check social media and GitHub for early announcements")
        print(f"5. Use directory enumeration tools (dirb, gobuster)")
        print(f"6. Check DNS subdomains (blockchain.domain.com)")

        print(f"\n{Colors.CYAN}🔧 Manual testing commands:{Colors.ENDC}")
        print(f"curl -I {base_url}/blockchain/")
        print(f"curl -I {base_url}/whitepaper.pdf")
        print(f"curl {base_url}/robots.txt")
        print(f"curl {base_url}/token/")

        # Show potential URLs to check manually
        print(f"\n{Colors.CYAN}🎯 Potential URLs to check manually:{Colors.ENDC}")
        manual_urls = [
            f"{base_url}/blockchain/",
            f"{base_url}/token/",
            f"{base_url}/ico/",
            f"{base_url}/whitepaper.pdf",
            f"{base_url}/announcement/",
        ]
        for url in manual_urls:
            print(f"   {url}")

if __name__ == '__main__':
    main()
```

---

## Mitigation Strategies

### 1. Secure Content Management

**Development vs Production Separation**:

```javascript
// Environment-based content control
const isDevelopment = process.env.NODE_ENV === 'development';
const isStaging = process.env.NODE_ENV === 'staging';
const isProduction = process.env.NODE_ENV === 'production';

// Content routing with environment checks
app.get('/blockchain/*', (req, res, next) => {
    // Only allow blockchain content in development
    if (!isDevelopment) {
        return res.status(404).json({ error: 'Not found' });
    }
    next();
});

app.get('/token/*', (req, res, next) => {
    // Token sale content only after announcement date
    const announcementDate = new Date('2025-12-01');
    const now = new Date();

    if (now < announcementDate && isProduction) {
        return res.status(404).json({ error: 'Content not available yet' });
    }
    next();
});
```

**Content Access Control**:

```javascript
// Role-based access to sensitive content
function requireRole(allowedRoles) {
    return (req, res, next) => {
        const userRole = req.user?.role;

        if (!allowedRoles.includes(userRole)) {
            return res.status(403).json({ error: 'Access denied' });
        }

        next();
    };
}

// Protect blockchain content
app.use('/blockchain/*', requireAuth, requireRole(['admin', 'investor']));
app.use('/tokensale/*', requireAuth, requireRole(['admin', 'investor']));

// Time-based access control
function requireAfterDate(targetDate) {
    return (req, res, next) => {
        const now = new Date();
        const releaseDate = new Date(targetDate);

        if (now < releaseDate) {
            return res.status(404).json({ error: 'Content not available yet' });
        }

        next();
    };
}

// Token sale content only after announcement
app.use('/announcement/*', requireAfterDate('2025-12-01T10:00:00Z'));
```

### 2. File System Security

**Secure File Placement**:

```bash
# GOOD - Outside web root
/opt/app/private/blockchain/
/var/app/restricted/tokensale/
/home/app/confidential/announcements/

# BAD - Inside web root (publicly accessible)
/var/www/html/blockchain/
/var/www/html/token/
/var/www/html/announcement/
```

**Web Server Configuration**:

**Apache (.htaccess)**:
```apache
# Deny access to blockchain directories until announcement
<Directory "/var/www/html/blockchain">
    Require all denied
    ErrorDocument 403 "Content not available"
    ErrorDocument 404 "Content not available"
</Directory>

# Deny access to draft documents
<FilesMatch "(?i)(draft|preview|test|temp).*\.(pdf|html|doc)$">
    Require all denied
</FilesMatch>

# Deny access to backup files
<FilesMatch "\.(bak|backup|old|tmp|draft)$">
    Require all denied
</FilesMatch>
```

**Nginx**:
```nginx
# Deny access to blockchain content
location /blockchain/ {
    deny all;
    return 404;
}

location /token/ {
    deny all;
    return 404;
}

# Deny access to draft files
location ~* \.(draft|preview|temp|bak|backup|old)$ {
    deny all;
    return 404;
}
```

### 3. Information Disclosure Prevention

**Robots.txt Best Practices**:

```
# DON'T include sensitive paths in robots.txt
# This tells attackers where to look!

# BAD robots.txt:
User-agent: *
Disallow: /admin/
Disallow: /blockchain/          # Reveals hidden content!
Disallow: /secret-tokensale/    # Even worse!

# GOOD robots.txt:
User-agent: *
Disallow: /private/
Disallow: /temp/

# Or don't include sensitive paths at all
User-agent: *
Crawl-delay: 1
```

**Secure Error Handling**:

```javascript
// BAD - Reveals information
app.get('/blockchain/*', (req, res) => {
    throw new Error(`Blockchain content at ${req.path} not ready for release until December 2025`);
});

// GOOD - Generic error
app.get('/blockchain/*', (req, res) => {
    res.status(404).json({ error: 'Not found' });
});

// BETTER - No route at all until ready
// Simply don't register the route until announcement date
```

### 4. Secure Development Practices

**Content Lifecycle Management**:

```javascript
class ContentManager {
    constructor() {
        this.contentSchedule = {
            'blockchain-announcement': {
                path: '/announcement/blockchain',
                releaseDate: '2025-12-01T10:00:00Z',
                requiredRole: 'public'
            },
            'token-sale-details': {
                path: '/tokensale/',
                releaseDate: '2025-12-15T09:00:00Z',
                requiredRole: 'verified-user'
            },
            'investor-materials': {
                path: '/investor/',
                releaseDate: '2025-11-15T12:00:00Z',
                requiredRole: 'accredited-investor'
            }
        };
    }

    isContentAvailable(contentKey, userRole = 'public') {
        const content = this.contentSchedule[contentKey];
        if (!content) return false;

        const now = new Date();
        const releaseDate = new Date(content.releaseDate);

        return now >= releaseDate && this.hasRequiredRole(userRole, content.requiredRole);
    }

    hasRequiredRole(userRole, requiredRole) {
        const roleHierarchy = {
            'public': 0,
            'user': 1,
            'verified-user': 2,
            'accredited-investor': 3,
            'admin': 4
        };

        return (roleHierarchy[userRole] || 0) >= (roleHierarchy[requiredRole] || 0);
    }

    registerContentRoutes(app) {
        Object.entries(this.contentSchedule).forEach(([key, content]) => {
            app.get(content.path, (req, res) => {
                if (this.isContentAvailable(key, req.user?.role)) {
                    // Serve content
                    res.sendFile(path.join(__dirname, 'content', key + '.html'));
                } else {
                    res.status(404).json({ error: 'Not found' });
                }
            });
        });
    }
}

// Usage
const contentManager = new ContentManager();
contentManager.registerContentRoutes(app);
```

### 5. Security Testing and Monitoring

**Automated Security Scanning**:

```bash
#!/bin/bash
# security_scan.sh - Regular security scanning script

echo "=== Information Disclosure Scan ==="

# Test for exposed files
SENSITIVE_PATHS=(
    "blockchain/" "token/" "ico/" "admin/"
    "config/" "backup/" ".git/" "robots.txt"
    "whitepaper.pdf" "tokensale.pdf"
)

for path in "${SENSITIVE_PATHS[@]}"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" "https://your-domain.com/$path")
    if [ "$status" = "200" ]; then
        echo "WARNING: $path is accessible (HTTP $status)"
        # Send alert to security team
        curl -X POST https://security-alerts.company.com/webhook \
             -d "{'alert': 'Exposed path found', 'path': '$path'}"
    fi
done

echo "=== Scan completed ==="
```

**Monitoring and Alerting**:

```javascript
// Monitor access to sensitive paths
app.use((req, res, next) => {
    const sensitivePaths = [
        '/blockchain/', '/token/', '/ico/', '/admin/',
        '/config/', '/backup/', '.pdf'
    ];

    const isSensitivePath = sensitivePaths.some(path =>
        req.url.toLowerCase().includes(path.toLowerCase())
    );

    if (isSensitivePath) {
        // Log access attempt
        logger.warn('Sensitive path access attempt', {
            path: req.url,
            ip: req.ip,
            userAgent: req.get('User-Agent'),
            timestamp: new Date().toISOString()
        });

        // Rate limit sensitive path access
        rateLimitSensitivePaths(req, res, next);
    } else {
        next();
    }
});

// Implement honeypot endpoints
app.get('/blockchain/secret/', (req, res) => {
    // Log honeypot access
    logger.error('SECURITY ALERT: Honeypot blockchain path accessed', {
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        path: req.url,
        timestamp: new Date().toISOString()
    });

    // Trigger security response
    triggerSecurityAlert('Blockchain honeypot accessed', req.ip);

    // Return fake content to keep attacker engaged
    res.json({
        message: "Blockchain module initializing...",
        status: "coming_soon"
    });
});
```

---

## References

### NIST Guidelines

**NIST SP 800-53 Controls**:
- **AC-3**: Access Enforcement - Implement proper access controls for sensitive content
- **AC-6**: Least Privilege - Users should only access necessary information
- **SC-13**: Cryptographic Protection - Protect sensitive documents with encryption
- **AU-2**: Auditable Events - Log access to sensitive content areas

**NIST Privacy Framework**:
- **Identify-P**: Identify and inventory sensitive information assets
- **Protect-P**: Implement technical safeguards for information protection
- **Detect-P**: Develop monitoring processes for unauthorized access

**NIST Risk Management Framework**:
- **Categorize**: Classify information based on potential impact
- **Select**: Choose appropriate security controls
- **Implement**: Deploy security measures
- **Monitor**: Continuous monitoring and assessment

### OWASP Guidelines

**OWASP Top 10 2021**:
- **A01: Broken Access Control** - Unauthorized access to sensitive content
- **A05: Security Misconfiguration** - Exposed development content
- **A09: Security Logging and Monitoring Failures** - Inadequate access monitoring

**OWASP Application Security Verification Standard (ASVS)**:
- **V4.1**: General Access Control Design
- **V4.2**: Operation Level Access Control
- **V14.4**: HTTP Security Headers Requirements

**OWASP Testing Guide**:
- **Testing for Information Disclosure** - Systematic approach to finding exposed information
- **Testing for Sensitive Information in Source Code** - Analyzing client-side code
- **Testing Directory Traversal** - Path manipulation techniques

### Industry Standards

**ISO/IEC 27001:2013**:
- **A.8.2.1**: Classification of information
- **A.8.2.2**: Labeling of information
- **A.8.2.3**: Handling of assets
- **A.13.2.1**: Information transfer policies and procedures

**PCI DSS (if handling payments)**:
- **Requirement 2**: Do not use vendor-supplied defaults for system passwords
- **Requirement 6**: Develop and maintain secure systems and applications
- **Requirement 7**: Restrict access to cardholder data by business need-to-know

**SOC 2 Type II**:
- **Security**: Access controls and monitoring
- **Confidentiality**: Protection of confidential information
- **Processing Integrity**: System processing accuracy and completeness

### Blockchain Security Standards

**NIST Blockchain Framework**:
- **NISTIR 8202**: Blockchain Technology Overview
- **NIST SP 1800-25**: Data Integrity: Recovering from Ransomware and Other Destructive Events

**Cryptocurrency Security Standards**:
- **EIP-20**: Ethereum Token Standard security considerations
- **OpenZeppelin Standards**: Secure smart contract development practices
- **ConsenSys Security Best Practices**: Smart contract security guidelines

### Security Resources

**Documentation**:
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [SANS Information Disclosure Prevention](https://www.sans.org/white-papers/36297/)
- [CWE-200: Information Exposure](https://cwe.mitre.org/data/definitions/200.html)

**Tools**:
- [Dirb](http://dirb.sourceforge.net/) - Directory enumeration
- [Gobuster](https://github.com/OJ/gobuster) - Fast directory brute forcer
- [Burp Suite](https://portswigger.net/burp) - Manual testing and crawling
- [FFUF](https://github.com/ffuf/ffuf) - Fast web fuzzer

**Blockchain Security Tools**:
- [MythX](https://mythx.io/) - Smart contract security analysis
- [Slither](https://github.com/crytic/slither) - Solidity static analyzer
- [Echidna](https://github.com/crytic/echidna) - Smart contract fuzzer
- [Manticore](https://github.com/trailofbits/manticore) - Symbolic execution tool

**Training Resources**:
- [Ethernaut](https://ethernaut.openzeppelin.com/) - Smart contract security challenges
- [Damn Vulnerable DeFi](https://www.damnvulnerabledefi.xyz/) - DeFi security scenarios
- [Cryptozombies](https://cryptozombies.io/) - Learn blockchain development
- [SANS FOR585](https://www.sans.org/cyber-security-courses/smartphone-mobile-device-forensics/) - Mobile and blockchain forensics

**Regulatory Resources**:
- [SEC Cryptocurrency Guidance](https://www.sec.gov/digital-assets) - US Securities and Exchange Commission
- [FINRA Cryptocurrency Notice](https://www.finra.org/rules-guidance/key-topics/cryptocurrency) - Financial Industry Regulatory Authority
- [FATF Cryptocurrency Guidelines](https://www.fatf-gafi.org/publications/fatfrecommendations/documents/guidance-virtual-assets.html) - Financial Action Task Force
- [European Banking Authority Crypto-Assets Regulation](https://www.eba.europa.eu/regulation-and-policy/crypto-assets) - EU financial regulation

---

**Document Version**: 1.0
**Last Updated**: 2025-10-10
**Author**: Walter Barr
**Challenge Difficulty**: ⭐⭐⭐⭐ (4/6)
**Estimated Time**: 30-60 minutes