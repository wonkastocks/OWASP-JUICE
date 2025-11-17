"""
Fingerprinting Module
DNS enumeration, banner grabbing, OS detection, and validation
"""

import dns.resolver
import socket
import re
import validators


def validate_target(target):
    """
    Validate target is a proper IP or hostname

    Args:
        target (str): IP address or hostname

    Returns:
        bool: True if valid
    """
    # Check if it's a valid IP
    if validators.ipv4(target) or validators.ipv6(target):
        return True

    # Check if it's a valid domain
    if validators.domain(target):
        return True

    # Check CIDR notation
    cidr_pattern = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    if re.match(cidr_pattern, target):
        return True

    return False


def dns_enumeration(target):
    """
    Comprehensive DNS enumeration

    Args:
        target (str): Domain name

    Returns:
        dict: DNS records and information
    """
    results = {
        'target': target,
        'records': {},
        'errors': []
    }

    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(target, record_type)
            results['records'][record_type] = [str(rdata) for rdata in answers]
        except dns.resolver.NoAnswer:
            results['records'][record_type] = []
        except dns.resolver.NXDOMAIN:
            results['errors'].append(f"{target} does not exist")
            break
        except Exception as e:
            results['errors'].append(f"{record_type}: {str(e)}")

    # Try reverse DNS if we have an IP
    if validators.ipv4(target):
        try:
            hostname = socket.gethostbyaddr(target)
            results['reverse_dns'] = hostname[0]
        except:
            results['reverse_dns'] = None

    # Get nameservers
    try:
        ns_records = dns.resolver.resolve(target, 'NS')
        nameservers = [str(ns) for ns in ns_records]
        results['nameservers'] = nameservers
    except:
        results['nameservers'] = []

    return results


def banner_grab_advanced(target, port, protocol='tcp'):
    """
    Advanced banner grabbing with protocol-specific probes

    Args:
        target (str): Target IP/hostname
        port (int): Port number
        protocol (str): tcp or udp

    Returns:
        dict: Banner information
    """
    result = {
        'target': target,
        'port': port,
        'protocol': protocol,
        'banner': None,
        'service_guess': None
    }

    # Protocol-specific probes
    probes = {
        80: b'GET / HTTP/1.0\r\nHost: ' + target.encode() + b'\r\n\r\n',
        443: b'GET / HTTP/1.0\r\nHost: ' + target.encode() + b'\r\n\r\n',
        21: b'USER anonymous\r\n',
        22: b'\r\n',
        23: b'\r\n',
        25: b'EHLO test\r\n',
        110: b'USER test\r\n',
        143: b'A001 CAPABILITY\r\n',
        3306: b'\r\n',
        5432: b'\r\n',
        6379: b'INFO\r\n'
    }

    probe = probes.get(port, b'\r\n')

    try:
        if protocol == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.settimeout(5)
        sock.connect((target, port))

        # Send probe
        sock.send(probe)

        # Receive response
        banner = b''
        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                banner += data
                if len(banner) > 4096:  # Limit banner size
                    break
        except socket.timeout:
            pass

        sock.close()

        if banner:
            result['banner'] = banner.decode('utf-8', errors='ignore').strip()
            result['service_guess'] = guess_service_from_banner(result['banner'])

    except Exception as e:
        result['error'] = str(e)

    return result


def guess_service_from_banner(banner):
    """
    Attempt to identify service from banner

    Args:
        banner (str): Banner text

    Returns:
        dict: Service identification
    """
    service_patterns = {
        'Apache': r'Apache/[\d.]+',
        'nginx': r'nginx/[\d.]+',
        'Microsoft IIS': r'Microsoft-IIS/[\d.]+',
        'OpenSSH': r'OpenSSH[_/][\d.]+',
        'ProFTPD': r'ProFTPD [\d.]+',
        'vsftpd': r'vsftpd [\d.]+',
        'Postfix': r'Postfix',
        'Exim': r'Exim [\d.]+',
        'MySQL': r'MySQL',
        'PostgreSQL': r'PostgreSQL',
        'Redis': r'Redis',
        'Elasticsearch': r'Elasticsearch'
    }

    for service, pattern in service_patterns.items():
        match = re.search(pattern, banner, re.IGNORECASE)
        if match:
            return {
                'service': service,
                'version': match.group(0)
            }

    return {'service': 'Unknown', 'version': ''}


def check_common_ports(target):
    """
    Quick check for common open ports

    Args:
        target (str): Target IP/hostname

    Returns:
        list: List of open ports
    """
    common_ports = [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
        3306, 3389, 5432, 5900, 6379, 8080, 8443
    ]

    open_ports = []

    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()

            if result == 0:
                open_ports.append(port)
        except:
            continue

    return open_ports


def detect_waf(target):
    """
    Detect Web Application Firewall

    Args:
        target (str): Target hostname/IP

    Returns:
        dict: WAF detection results
    """
    result = {
        'waf_detected': False,
        'waf_type': None,
        'indicators': []
    }

    try:
        import requests

        # Test payload
        test_url = f"http://{target}/?test=<script>alert(1)</script>"

        response = requests.get(test_url, timeout=5, allow_redirects=False)

        # Check headers for WAF signatures
        waf_headers = {
            'Cloudflare': ['cf-ray', 'cf-cache-status'],
            'AWS WAF': ['x-amzn-requestid', 'x-amz-cf-id'],
            'Akamai': ['x-akamai-request-id'],
            'Sucuri': ['x-sucuri-id'],
            'Imperva': ['x-iinfo'],
            'F5 BIG-IP': ['x-cnection']
        }

        for waf, headers in waf_headers.items():
            for header in headers:
                if header in response.headers:
                    result['waf_detected'] = True
                    result['waf_type'] = waf
                    result['indicators'].append(f"Header: {header}")

        # Check for common WAF response codes/bodies
        if response.status_code in [403, 406, 419, 420, 429]:
            result['indicators'].append(f"Suspicious status code: {response.status_code}")

        # Check for block messages
        block_keywords = ['blocked', 'forbidden', 'access denied', 'security', 'firewall']
        response_text = response.text.lower()

        for keyword in block_keywords:
            if keyword in response_text:
                result['indicators'].append(f"Block keyword found: {keyword}")
                result['waf_detected'] = True

    except Exception as e:
        result['error'] = str(e)

    return result


def enumerate_subdomains(domain, wordlist=None):
    """
    Basic subdomain enumeration

    Args:
        domain (str): Base domain
        wordlist (list): List of subdomains to try

    Returns:
        list: Found subdomains
    """
    if not wordlist:
        wordlist = [
            'www', 'mail', 'ftp', 'admin', 'webmail', 'portal',
            'api', 'dev', 'staging', 'test', 'vpn', 'remote',
            'blog', 'shop', 'store', 'cdn', 'static'
        ]

    found_subdomains = []

    for subdomain in wordlist:
        try:
            full_domain = f"{subdomain}.{domain}"
            answers = dns.resolver.resolve(full_domain, 'A')
            ips = [str(rdata) for rdata in answers]
            found_subdomains.append({
                'subdomain': full_domain,
                'ips': ips
            })
        except:
            continue

    return found_subdomains


def get_whois_info(domain):
    """
    Get WHOIS information (basic implementation)

    Args:
        domain (str): Domain name

    Returns:
        dict: WHOIS data
    """
    # This is a placeholder - would need python-whois package for full implementation
    result = {
        'domain': domain,
        'info': 'WHOIS lookup requires python-whois package',
        'note': 'Install with: pip install python-whois'
    }

    try:
        import whois
        w = whois.whois(domain)
        result['info'] = str(w)
        result['registrar'] = w.registrar
        result['creation_date'] = str(w.creation_date)
        result['expiration_date'] = str(w.expiration_date)
        result['nameservers'] = w.name_servers
    except ImportError:
        pass
    except Exception as e:
        result['error'] = str(e)

    return result


def ssl_certificate_info(target, port=443):
    """
    Get SSL certificate information

    Args:
        target (str): Target hostname
        port (int): HTTPS port

    Returns:
        dict: Certificate details
    """
    result = {}

    try:
        import ssl
        import OpenSSL

        context = ssl.create_default_context()
        with socket.create_connection((target, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert_bin = ssock.getpeercert(binary_form=True)
                cert = OpenSSL.crypto.load_certificate(
                    OpenSSL.crypto.FILETYPE_ASN1,
                    cert_bin
                )

                result['subject'] = dict(x[0] for x in cert.get_subject().get_components())
                result['issuer'] = dict(x[0] for x in cert.get_issuer().get_components())
                result['version'] = cert.get_version()
                result['serial_number'] = cert.get_serial_number()
                result['not_before'] = cert.get_notBefore().decode('utf-8')
                result['not_after'] = cert.get_notAfter().decode('utf-8')

    except ImportError:
        result['error'] = 'Requires pyOpenSSL: pip install pyOpenSSL'
    except Exception as e:
        result['error'] = str(e)

    return result
