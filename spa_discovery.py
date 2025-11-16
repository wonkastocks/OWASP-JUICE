#!/usr/bin/env python3
"""
SPA Discovery Tool
==================
Automated Single Page Application route and API endpoint discovery.

Usage:
    python3 spa_discovery.py                          # Interactive menu
    python3 spa_discovery.py --url https://example.com
    python3 spa_discovery.py --preset juice5
    python3 spa_discovery.py --preset airbnb

Author: Walter Barr
Date: 2025-09-26
"""

import re
import json
import time
import argparse
import sys
from urllib.parse import urlparse, urljoin
from collections import defaultdict

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ Missing required dependency: {e}")
    print("\n📦 Install dependencies with:")
    print("   pip3 install requests beautifulsoup4")
    sys.exit(1)


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
    UNDERLINE = '\033[4m'


class SPADiscovery:
    """Main SPA discovery class"""

    PRESETS = {
        'juice5': 'https://juice5.wonkatech.org',
        'airbnb': 'https://www.airbnb.com'
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        'Angular': [
            r'ng-version',
            r'angular\.js',
            r'angular\.min\.js',
            r'@angular',
            r'ng-app',
            r'<app-root',
            r'_angular_',
            r'platformBrowserDynamic'
        ],
        'React': [
            r'react\.js',
            r'react\.min\.js',
            r'react-dom',
            r'__REACT_DEVTOOLS',
            r'data-reactroot',
            r'data-reactid',
            r'_react',
            r'createElement'
        ],
        'Vue': [
            r'vue\.js',
            r'vue\.min\.js',
            r'v-for',
            r'v-if',
            r'v-bind',
            r'__VUE__',
            r'createApp'
        ],
        'Ember': [
            r'ember\.js',
            r'ember\.min\.js',
            r'ember-application'
        ],
        'Svelte': [
            r'svelte',
            r'class="svelte-'
        ],
        'Next.js': [
            r'__NEXT_DATA__',
            r'_next/static'
        ]
    }

    def __init__(self, url, timeout=30):
        """Initialize SPA discovery"""
        self.url = url.rstrip('/')
        self.base_domain = urlparse(url).netloc
        self.timeout = timeout

        # Results storage
        self.is_spa = False
        self.framework = None
        self.routes = set()
        self.api_endpoints = set()
        self.javascript_files = []
        self.hash_routing = False
        self.history_api = False

        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def detect_framework(self, html_content, js_content):
        """Detect JavaScript framework"""
        print(f"{Colors.CYAN}🔍 Detecting JavaScript framework...{Colors.ENDC}")

        detected = []
        combined_content = html_content + '\n' + js_content

        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, combined_content, re.IGNORECASE):
                    detected.append(framework)
                    break

        if detected:
            self.framework = detected[0]  # Primary framework
            print(f"{Colors.GREEN}✅ Framework detected: {Colors.BOLD}{self.framework}{Colors.ENDC}")
            if len(detected) > 1:
                print(f"   {Colors.CYAN}Also found: {', '.join(detected[1:])}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  No framework detected (might be vanilla JS or SSR){Colors.ENDC}")

        return bool(detected)

    def check_spa_indicators(self, html_content):
        """Check for SPA indicators in HTML"""
        print(f"{Colors.CYAN}🔍 Checking SPA indicators...{Colors.ENDC}")

        indicators = {
            'Single root div': False,
            'Large JS bundles': False,
            'Minimal HTML': False,
            'Client-side routing': False
        }

        # Check for single root element
        root_patterns = [
            r'<div id=["\']root["\']',
            r'<div id=["\']app["\']',
            r'<app-root',
            r'<div data-reactroot',
            r'<div id=["\']__next["\']'
        ]
        for pattern in root_patterns:
            if re.search(pattern, html_content):
                indicators['Single root div'] = True
                break

        # Check for large JS bundles
        js_tags = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html_content)
        self.javascript_files = js_tags

        large_bundles = [js for js in js_tags if any(name in js.lower() for name in
                        ['main', 'bundle', 'app', 'vendor', 'chunk', 'runtime'])]
        if large_bundles:
            indicators['Large JS bundles'] = True

        # Check for minimal HTML (SPA characteristic)
        body_content = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
        if body_content:
            body_text = re.sub(r'<script.*?</script>', '', body_content.group(1), flags=re.DOTALL)
            body_text = re.sub(r'<[^>]+>', '', body_text)
            if len(body_text.strip()) < 500:  # Very little static content
                indicators['Minimal HTML'] = True

        # Check for hash routing
        if re.search(r'#/', html_content) or 'hashchange' in html_content:
            indicators['Client-side routing'] = True
            self.hash_routing = True

        # Check for History API usage
        if 'pushState' in html_content or 'replaceState' in html_content:
            indicators['Client-side routing'] = True
            self.history_api = True

        # Print results
        for indicator, detected in indicators.items():
            status = f"{Colors.GREEN}✓{Colors.ENDC}" if detected else f"{Colors.RED}✗{Colors.ENDC}"
            print(f"   {status} {indicator}")

        # Determine if it's an SPA
        self.is_spa = sum(indicators.values()) >= 2

        return self.is_spa

    def extract_routes_from_js(self, js_content):
        """Extract routes from JavaScript bundles"""
        print(f"\n{Colors.CYAN}🔍 Extracting routes from JavaScript...{Colors.ENDC}")

        route_patterns = [
            # Angular routes - more specific patterns
            r'path:\s*"([^"]{2,50})"',
            r"path:\s*'([^']{2,50})'",
            r'route\(\s*["\']([^"\']{2,50})["\']',

            # React Router routes
            r'<Route\s+path=["\']([^"\']+)["\']',
            r'path:\s*["\']([^"\']{2,50})["\']',

            # Vue Router routes
            r'path:\s*["\']([^"\']{2,50})["\']',

            # General path patterns in routing configs
            r'["\']path["\']\s*:\s*["\']([^"\']{2,50})["\']',

            # Hash routes in code
            r'#/([a-zA-Z0-9\-_/:{]+)',
        ]

        found_routes = set()

        for pattern in route_patterns:
            matches = re.findall(pattern, js_content)
            for match in matches:
                # Filter out common false positives
                if (match and
                    not match.startswith('http') and
                    not match.startswith('www.') and
                    not match.endswith('.js') and
                    not match.endswith('.css') and
                    not match.endswith('.png') and
                    not match.endswith('.jpg') and
                    not match.endswith('.svg') and
                    not match.startswith('data:') and
                    not match.startswith('blob:') and
                    '.' not in match.split('/')[-1] and
                    match not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options'] and
                    len(match) > 1):

                    # Clean up the route
                    route = match.strip('/').strip()
                    if route and route != '**':  # Skip catch-all routes
                        if not route.startswith('/'):
                            route = '/' + route
                        found_routes.add(route)

        self.routes.update(found_routes)

        if found_routes:
            print(f"{Colors.GREEN}✅ Found {len(found_routes)} potential routes{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  No routes found in JavaScript{Colors.ENDC}")

        return found_routes

    def extract_api_endpoints(self, js_content):
        """Extract API endpoints from JavaScript"""
        print(f"{Colors.CYAN}🔍 Extracting API endpoints...{Colors.ENDC}")

        api_patterns = [
            # REST and API paths
            r'"/(rest|api|graphql)/([^"]{2,80})"',
            r"'/(rest|api|graphql)/([^']{2,80})'",

            # Full URLs with API paths
            r'https?://[^/]+/(rest|api)/([^"\']+)["\']',

            # Fetch and axios calls
            r'fetch\(["\']([^"\']+)["\']',
            r'axios\.[a-z]+\(["\']([^"\']+)["\']',

            # HTTP method patterns
            r'\.get\(["\']([^"\']+)["\']',
            r'\.post\(["\']([^"\']+)["\']',
            r'\.put\(["\']([^"\']+)["\']',
            r'\.delete\(["\']([^"\']+)["\']',
            r'\.patch\(["\']([^"\']+)["\']',

            # Common API endpoint patterns
            r'endpoint:\s*["\']([^"\']+)["\']',
            r'url:\s*["\']([^"\']+)["\']',
            r'uri:\s*["\']([^"\']+)["\']',
        ]

        found_endpoints = set()

        for pattern in api_patterns:
            matches = re.findall(pattern, js_content)
            for match in matches:
                # Handle tuple results from capturing groups
                if isinstance(match, tuple):
                    # Reconstruct the endpoint
                    if len(match) == 2:
                        endpoint = f'/{match[0]}/{match[1]}'
                    else:
                        endpoint = '/'.join([m for m in match if m])
                else:
                    endpoint = match

                # Filter and clean
                if endpoint:
                    # Skip non-API paths
                    if not any(api_part in endpoint for api_part in ['/api/', '/rest/', '/graphql']):
                        continue

                    # Skip static resources
                    if endpoint.endswith(('.js', '.css', '.png', '.jpg', '.svg', '.gif', '.woff', '.ttf', '.ico')):
                        continue

                    # Extract path from full URL
                    if endpoint.startswith('http'):
                        parsed = urlparse(endpoint)
                        endpoint = parsed.path

                    # Clean up
                    endpoint = endpoint.strip()
                    if endpoint:
                        found_endpoints.add(endpoint)

        self.api_endpoints.update(found_endpoints)

        if found_endpoints:
            print(f"{Colors.GREEN}✅ Found {len(found_endpoints)} API endpoints{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  No API endpoints found{Colors.ENDC}")

        return found_endpoints

    def fetch_javascript_content(self, html_content):
        """Fetch JavaScript bundle content"""
        print(f"{Colors.CYAN}📦 Fetching JavaScript bundles...{Colors.ENDC}")

        js_content = ""

        # Extract script src tags
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts = soup.find_all('script', src=True)

        # Prioritize main application bundles
        priority_patterns = ['main.js', 'app.js', 'bundle.js', 'vendor.js', 'runtime.js']
        script_urls = []

        for script in scripts:
            src = script['src']
            # Skip external CDN scripts
            if not any(cdn in src for cdn in ['cdnjs.cloudflare.com', 'googleapis.com', 'jquery']):
                script_urls.append(src)

        # Sort by priority
        def priority_key(url):
            for i, pattern in enumerate(priority_patterns):
                if pattern in url.lower():
                    return i
            return 100

        script_urls.sort(key=priority_key)

        # Fetch top JavaScript files
        fetched_count = 0
        for src in script_urls[:15]:  # Limit to first 15 files
            try:
                js_url = urljoin(self.url, src)
                print(f"   Fetching: {src}")
                response = self.session.get(js_url, timeout=10)
                if response.status_code == 200:
                    js_content += response.text + "\n"
                    fetched_count += 1
            except Exception as e:
                print(f"   {Colors.YELLOW}Failed to fetch {src}: {e}{Colors.ENDC}")
                continue

        print(f"{Colors.GREEN}✅ Fetched {fetched_count} JavaScript bundles ({len(js_content)} chars){Colors.ENDC}\n")
        return js_content

    def analyze(self):
        """Main analysis method"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  SPA DISCOVERY TOOL{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

        print(f"{Colors.CYAN}🎯 Target: {Colors.BOLD}{self.url}{Colors.ENDC}\n")

        try:
            # Load the page
            print(f"{Colors.CYAN}📡 Loading page...{Colors.ENDC}")
            response = self.session.get(self.url, timeout=self.timeout)

            if response.status_code != 200:
                print(f"{Colors.RED}❌ Failed to load page: HTTP {response.status_code}{Colors.ENDC}")
                return

            html_content = response.text
            print(f"{Colors.GREEN}✅ Page loaded successfully ({len(html_content)} chars){Colors.ENDC}\n")

            # Fetch JavaScript content
            js_content = self.fetch_javascript_content(html_content)

            # Run detection
            framework_detected = self.detect_framework(html_content, js_content)
            spa_detected = self.check_spa_indicators(html_content)

            # If it's an SPA, do deeper analysis
            if self.is_spa:
                print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SPA DETECTED!{Colors.ENDC}\n")

                # Extract routes and APIs
                self.extract_routes_from_js(js_content)
                self.extract_api_endpoints(js_content)

                # Print comprehensive results
                self.print_results()

            else:
                print(f"\n{Colors.RED}{Colors.BOLD}❌ NOT A SINGLE PAGE APPLICATION{Colors.ENDC}\n")
                print(f"{Colors.YELLOW}This appears to be a traditional multi-page website.{Colors.ENDC}")
                print(f"{Colors.YELLOW}Characteristics of traditional sites:{Colors.ENDC}")
                print(f"   • Server-side rendering")
                print(f"   • Full page reloads on navigation")
                print(f"   • Multiple HTML documents")
                print(f"   • Traditional form submissions")

                if self.framework:
                    print(f"\n{Colors.CYAN}Note: {self.framework} detected, but used for enhancement,")
                    print(f"      not as a full SPA framework.{Colors.ENDC}")

        except requests.exceptions.Timeout:
            print(f"{Colors.RED}❌ Request timeout - site took too long to respond{Colors.ENDC}")
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}❌ Connection error - could not reach site{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")

    def print_results(self):
        """Print comprehensive results"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  ANALYSIS RESULTS{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

        # SPA Type
        print(f"{Colors.BOLD}🎨 SPA Characteristics:{Colors.ENDC}")
        print(f"   Framework: {Colors.GREEN}{self.framework or 'Unknown'}{Colors.ENDC}")

        if self.hash_routing:
            print(f"   Routing Type: {Colors.GREEN}Hash-based (#/route){Colors.ENDC}")
        elif self.history_api:
            print(f"   Routing Type: {Colors.GREEN}History API (/route){Colors.ENDC}")
        else:
            print(f"   Routing Type: {Colors.YELLOW}Unknown{Colors.ENDC}")

        # Routes
        print(f"\n{Colors.BOLD}🗺️  Frontend Routes ({len(self.routes)}):{Colors.ENDC}")
        if self.routes:
            sorted_routes = sorted(self.routes)
            for route in sorted_routes[:50]:  # Show first 50
                print(f"   {Colors.CYAN}├──{Colors.ENDC} {route}")
            if len(self.routes) > 50:
                print(f"   {Colors.YELLOW}└── ... and {len(self.routes) - 50} more{Colors.ENDC}")
        else:
            print(f"   {Colors.YELLOW}No routes discovered{Colors.ENDC}")

        # API Endpoints
        print(f"\n{Colors.BOLD}🔌 API Endpoints ({len(self.api_endpoints)}):{Colors.ENDC}")
        if self.api_endpoints:
            # Group by prefix
            grouped = defaultdict(list)
            for endpoint in self.api_endpoints:
                parts = endpoint.split('/')
                prefix = parts[1] if len(parts) > 1 and parts[1] else 'root'
                grouped[prefix].append(endpoint)

            for prefix, endpoints in sorted(grouped.items()):
                print(f"\n   {Colors.GREEN}{prefix}/{Colors.ENDC}")
                for endpoint in sorted(endpoints)[:30]:  # Show first 30 per group
                    print(f"   {Colors.CYAN}├──{Colors.ENDC} {endpoint}")
                if len(endpoints) > 30:
                    print(f"   {Colors.YELLOW}└── ... and {len(endpoints) - 30} more{Colors.ENDC}")
        else:
            print(f"   {Colors.YELLOW}No API endpoints discovered{Colors.ENDC}")

        # JavaScript Bundles
        print(f"\n{Colors.BOLD}📦 JavaScript Bundles ({len(self.javascript_files)}):{Colors.ENDC}")
        if self.javascript_files:
            for js_file in self.javascript_files[:15]:  # Show first 15
                print(f"   {Colors.CYAN}├──{Colors.ENDC} {js_file}")
            if len(self.javascript_files) > 15:
                print(f"   {Colors.YELLOW}└── ... and {len(self.javascript_files) - 15} more{Colors.ENDC}")

        # Export options
        print(f"\n{Colors.BOLD}💾 Export Results:{Colors.ENDC}")
        print(f"   Run with --export flag to save detailed JSON report")

        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

    def export_json(self, filename='spa_discovery_report.json'):
        """Export results to JSON"""
        report = {
            'url': self.url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'is_spa': self.is_spa,
            'framework': self.framework,
            'routing': {
                'hash_based': self.hash_routing,
                'history_api': self.history_api
            },
            'routes': sorted(list(self.routes)),
            'api_endpoints': sorted(list(self.api_endpoints)),
            'javascript_files': self.javascript_files
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"{Colors.GREEN}✅ Report saved to: {filename}{Colors.ENDC}")


def interactive_menu():
    """Interactive menu for site selection"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}  SPA DISCOVERY TOOL - Interactive Mode{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Select a target:{Colors.ENDC}\n")
    print(f"  1. Juice Shop (juice5.wonkatech.org)")
    print(f"  2. Airbnb (www.airbnb.com)")
    print(f"  3. Custom URL")
    print(f"  4. Exit\n")

    choice = input(f"{Colors.CYAN}Enter choice (1-4): {Colors.ENDC}").strip()

    if choice == '1':
        return SPADiscovery.PRESETS['juice5']
    elif choice == '2':
        return SPADiscovery.PRESETS['airbnb']
    elif choice == '3':
        url = input(f"{Colors.CYAN}Enter URL: {Colors.ENDC}").strip()
        if not url.startswith('http'):
            url = 'https://' + url
        return url
    elif choice == '4':
        print(f"\n{Colors.YELLOW}Goodbye!{Colors.ENDC}\n")
        sys.exit(0)
    else:
        print(f"{Colors.RED}Invalid choice{Colors.ENDC}")
        return interactive_menu()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='SPA Discovery Tool - Automated Single Page Application Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Interactive menu
  %(prog)s --preset juice5              # Analyze Juice Shop
  %(prog)s --preset airbnb              # Analyze Airbnb
  %(prog)s --url https://example.com    # Analyze custom URL
  %(prog)s --url example.com --export   # Export results to JSON
        """
    )

    parser.add_argument('--url', help='Target URL to analyze')
    parser.add_argument('--preset', choices=['juice5', 'airbnb'],
                       help='Use preset URL (juice5 or airbnb)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds (default: 30)')
    parser.add_argument('--export', action='store_true',
                       help='Export results to JSON file')

    args = parser.parse_args()

    # Determine target URL
    if args.preset:
        url = SPADiscovery.PRESETS[args.preset]
    elif args.url:
        url = args.url
        if not url.startswith('http'):
            url = 'https://' + url
    else:
        url = interactive_menu()

    # Run analysis
    try:
        discovery = SPADiscovery(url, timeout=args.timeout)
        discovery.analyze()

        if args.export and discovery.is_spa:
            discovery.export_json()

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Analysis interrupted by user{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.ENDC}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()