"""
AI Analyzer - Uses OpenAI to interpret scan requests and analyze results
"""

import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()


class AIAnalyzer:
    """AI-powered scan request interpretation and results analysis"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        else:
            print("[!] Warning: OpenAI API key not set. AI features will be limited.")

    def interpret_scan_request(self, user_request, target):
        """
        Use AI to interpret natural language scan request

        Args:
            user_request (str): User's natural language request
            target (str): Target IP/hostname

        Returns:
            dict: Structured scan parameters
        """
        if not self.api_key:
            return self._fallback_interpretation(user_request, target)

        system_prompt = """You are a network security expert helping interpret scan requests for NMAP.
Convert natural language requests into structured NMAP scan parameters.

Return a JSON object with these fields:
{
    "scan_type": "quick|full|stealth|service|os|vuln|webapp|dns|custom",
    "ports": "port range or 'all' or 'default'",
    "scripts": ["list", "of", "nse", "scripts"],
    "timing": 0-5 (NMAP timing template),
    "additional_flags": "any extra NMAP flags",
    "reasoning": "brief explanation of choices"
}

Scan types:
- quick: Fast scan, top 100 ports
- full: Comprehensive scan, all ports, OS + service detection
- stealth: Slow, evade detection
- service: Focus on service/version detection
- os: OS fingerprinting
- vuln: Vulnerability scanning
- webapp: Web application enumeration
- dns: DNS enumeration

Examples:
- "do a quick scan" -> quick scan, default ports
- "check for web vulnerabilities" -> webapp scan with http scripts
- "comprehensive scan with OS detection" -> full scan with -O flag
- "stealthy scan to avoid detection" -> stealth scan, T1 timing
"""

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Target: {target}\nRequest: {user_request}"}
                ],
                temperature=0.3,
                max_tokens=500
            )

            result = response.choices[0].message.content.strip()

            # Extract JSON from response
            if '```json' in result:
                result = result.split('```json')[1].split('```')[0].strip()
            elif '```' in result:
                result = result.split('```')[1].split('```')[0].strip()

            params = json.loads(result)
            params['target'] = target
            params['user_request'] = user_request

            return params

        except Exception as e:
            print(f"[!] AI interpretation failed: {e}")
            return self._fallback_interpretation(user_request, target)

    def analyze_scan_results(self, scan_results):
        """
        Use AI to analyze and interpret scan results

        Args:
            scan_results (dict): Parsed scan results

        Returns:
            dict: AI analysis with insights, risks, and recommendations
        """
        if not self.api_key:
            return self._fallback_analysis(scan_results)

        system_prompt = """You are a cybersecurity expert analyzing NMAP scan results.
Provide a comprehensive analysis including:
1. Summary of findings
2. Security risks identified
3. Notable services and versions
4. Recommendations for further investigation
5. Risk level assessment (low, medium, high, critical)

Return JSON format:
{
    "summary": "Brief overview",
    "risks": ["list", "of", "security", "risks"],
    "notable_services": ["interesting", "services", "found"],
    "recommendations": ["what", "to", "investigate"],
    "risk_level": "low|medium|high|critical",
    "vulnerabilities": ["potential", "vulnerabilities"]
}

Focus on:
- Outdated software versions with known CVEs
- Unnecessary open ports
- Misconfigured services
- Weak authentication mechanisms
- Information disclosure
"""

        try:
            # Prepare scan data for AI
            scan_summary = self._prepare_scan_summary(scan_results)

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze these scan results:\n\n{json.dumps(scan_summary, indent=2)}"}
                ],
                temperature=0.4,
                max_tokens=1000
            )

            result = response.choices[0].message.content.strip()

            # Extract JSON
            if '```json' in result:
                result = result.split('```json')[1].split('```')[0].strip()
            elif '```' in result:
                result = result.split('```')[1].split('```')[0].strip()

            analysis = json.loads(result)
            return analysis

        except Exception as e:
            print(f"[!] AI analysis failed: {e}")
            return self._fallback_analysis(scan_results)

    def _prepare_scan_summary(self, scan_results):
        """Prepare concise scan summary for AI analysis"""
        summary = {
            'target': scan_results.get('target'),
            'duration': scan_results.get('duration'),
            'status': scan_results.get('status')
        }

        if 'parsed_data' in scan_results and 'hosts' in scan_results['parsed_data']:
            hosts = scan_results['parsed_data']['hosts']
            if hosts:
                host = hosts[0]
                summary['host_status'] = host.get('status')
                summary['os'] = host.get('os', {})
                summary['open_ports'] = []

                for port in host.get('ports', []):
                    if port.get('state') == 'open':
                        port_info = {
                            'port': port['port'],
                            'service': port.get('service', {}).get('name'),
                            'product': port.get('service', {}).get('product'),
                            'version': port.get('service', {}).get('version'),
                            'scripts': [s['id'] for s in port.get('scripts', [])]
                        }
                        summary['open_ports'].append(port_info)

        return summary

    def _fallback_interpretation(self, user_request, target):
        """Fallback interpretation when AI is unavailable"""
        request_lower = user_request.lower()

        # Simple keyword matching
        if any(word in request_lower for word in ['quick', 'fast', 'basic']):
            scan_type = 'quick'
            ports = 'default'
            timing = 4
        elif any(word in request_lower for word in ['full', 'comprehensive', 'complete', 'all']):
            scan_type = 'full'
            ports = 'all'
            timing = 3
        elif any(word in request_lower for word in ['stealth', 'quiet', 'sneaky', 'evade']):
            scan_type = 'stealth'
            ports = 'default'
            timing = 1
        elif any(word in request_lower for word in ['web', 'http', 'webapp', 'website']):
            scan_type = 'webapp'
            ports = '80,443,8080,8443'
            timing = 3
        elif any(word in request_lower for word in ['vuln', 'vulnerability', 'exploit']):
            scan_type = 'vuln'
            ports = 'default'
            timing = 3
        elif any(word in request_lower for word in ['os', 'operating system', 'fingerprint']):
            scan_type = 'os'
            ports = 'default'
            timing = 3
        else:
            scan_type = 'quick'
            ports = 'default'
            timing = 3

        return {
            'target': target,
            'scan_type': scan_type,
            'ports': ports,
            'scripts': [],
            'timing': timing,
            'additional_flags': '',
            'reasoning': 'Keyword-based interpretation (AI unavailable)',
            'user_request': user_request
        }

    def _fallback_analysis(self, scan_results):
        """Fallback analysis when AI is unavailable"""
        analysis = {
            'summary': 'Scan completed. AI analysis unavailable.',
            'risks': [],
            'notable_services': [],
            'recommendations': ['Configure OpenAI API key for detailed analysis'],
            'risk_level': 'unknown',
            'vulnerabilities': []
        }

        # Basic analysis
        if 'parsed_data' in scan_results and 'hosts' in scan_results['parsed_data']:
            hosts = scan_results['parsed_data']['hosts']
            if hosts:
                host = hosts[0]
                open_ports = [p for p in host.get('ports', []) if p.get('state') == 'open']

                analysis['summary'] = f"Found {len(open_ports)} open ports"

                for port in open_ports:
                    service = port.get('service', {})
                    service_name = service.get('name', 'unknown')
                    product = service.get('product', '')
                    version = service.get('version', '')

                    if product and version:
                        analysis['notable_services'].append(f"{port['port']}/{service_name}: {product} {version}")

                    # Flag common risky ports
                    risky_ports = {
                        21: 'FTP - unencrypted file transfer',
                        23: 'Telnet - unencrypted remote access',
                        139: 'NetBIOS - potential SMB exposure',
                        445: 'SMB - file sharing, check for vulnerabilities',
                        3306: 'MySQL - database exposure',
                        5432: 'PostgreSQL - database exposure',
                        6379: 'Redis - potential unauthorized access'
                    }

                    if port['port'] in risky_ports:
                        analysis['risks'].append(f"Port {port['port']}: {risky_ports[port['port']]}")

        return analysis

    def suggest_next_scan(self, current_results):
        """
        Suggest next scan based on current results

        Args:
            current_results (dict): Current scan results

        Returns:
            str: Suggestion for next scan
        """
        suggestions = []

        if 'parsed_data' in current_results:
            hosts = current_results['parsed_data'].get('hosts', [])
            if hosts:
                host = hosts[0]
                ports = host.get('ports', [])

                # Check for web ports
                web_ports = [p for p in ports if p.get('port') in [80, 443, 8080, 8443] and p.get('state') == 'open']
                if web_ports:
                    suggestions.append("Run webapp enumeration scan for detailed HTTP analysis")

                # Check for SMB
                smb_ports = [p for p in ports if p.get('port') in [139, 445] and p.get('state') == 'open']
                if smb_ports:
                    suggestions.append("Run SMB enumeration scripts to check for shares and vulnerabilities")

                # Check for databases
                db_ports = [p for p in ports if p.get('port') in [3306, 5432, 1433, 27017] and p.get('state') == 'open']
                if db_ports:
                    suggestions.append("Investigate database services for misconfigurations")

        if not suggestions:
            suggestions.append("Run a full scan for comprehensive analysis")

        return " | ".join(suggestions)
