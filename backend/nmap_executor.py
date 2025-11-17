"""
NMAP Executor - Handles all NMAP scanning operations
Supports various scan types, NSE scripts, and fingerprinting
"""

import nmap
import subprocess
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import os


class NmapExecutor:
    """Wrapper for NMAP operations"""

    def __init__(self, output_dir='scans'):
        self.nm = nmap.PortScanner()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def build_scan_command(self, scan_params):
        """
        Build NMAP command based on AI-interpreted parameters

        Args:
            scan_params (dict): Dictionary containing scan parameters
                - target: IP/hostname to scan
                - scan_type: quick, full, stealth, service, os, vuln, etc.
                - ports: Port range (e.g., '1-1000', 'all', '80,443')
                - scripts: NSE scripts to run
                - timing: Timing template (0-5)
                - additional_flags: Extra NMAP flags

        Returns:
            str: NMAP command string
        """
        target = scan_params.get('target')
        scan_type = scan_params.get('scan_type', 'quick')
        ports = scan_params.get('ports', '1-1000')
        scripts = scan_params.get('scripts', [])
        timing = scan_params.get('timing', 3)
        additional_flags = scan_params.get('additional_flags', '')

        # Base command
        cmd_parts = ['nmap']

        # Scan type specific flags
        if scan_type == 'quick':
            cmd_parts.extend(['-T4', '-F'])  # Fast scan, top 100 ports
        elif scan_type == 'full':
            cmd_parts.extend(['-T3', '-p-', '-sV', '-O'])  # All ports, service + OS detection
        elif scan_type == 'stealth':
            cmd_parts.extend(['-sS', '-T2', '-f'])  # SYN stealth, slower, fragmented
        elif scan_type == 'service':
            cmd_parts.extend(['-sV', '--version-intensity', '5'])  # Aggressive service detection
        elif scan_type == 'os':
            cmd_parts.extend(['-O', '--osscan-guess'])  # OS detection
        elif scan_type == 'vuln':
            cmd_parts.extend(['-sV', '--script=vuln'])  # Vulnerability scripts
        elif scan_type == 'webapp':
            cmd_parts.extend(['-sV', '--script=http-enum,http-headers,http-methods,http-title'])
        elif scan_type == 'dns':
            cmd_parts.extend(['--script=dns-brute,dns-zone-transfer'])
        else:
            cmd_parts.extend(['-T3'])  # Default timing

        # Port specification
        if ports and ports != 'default':
            if ports == 'all':
                cmd_parts.append('-p-')
            else:
                cmd_parts.extend(['-p', ports])

        # Timing template (if not already set)
        if f'-T{timing}' not in ' '.join(cmd_parts):
            cmd_parts.append(f'-T{timing}')

        # NSE Scripts
        if scripts:
            if isinstance(scripts, list):
                scripts_str = ','.join(scripts)
            else:
                scripts_str = scripts
            cmd_parts.extend(['--script', scripts_str])

        # Output formats
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_base = f"{self.output_dir}/scan_{target.replace('.', '_')}_{timestamp}"
        cmd_parts.extend(['-oN', f"{output_base}.txt"])
        cmd_parts.extend(['-oX', f"{output_base}.xml"])

        # Additional flags
        if additional_flags:
            cmd_parts.append(additional_flags)

        # Target
        cmd_parts.append(target)

        return ' '.join(cmd_parts), output_base

    def execute_scan(self, target, scan_params):
        """
        Execute NMAP scan

        Args:
            target (str): Target IP/hostname
            scan_params (dict): Scan parameters

        Returns:
            dict: Scan results with parsed data
        """
        scan_params['target'] = target
        command, output_base = self.build_scan_command(scan_params)

        print(f"[*] Executing: {command}")

        try:
            # Execute scan
            start_time = datetime.now()
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Parse results
            scan_results = {
                'command': command,
                'target': target,
                'started_at': start_time.isoformat(),
                'completed_at': end_time.isoformat(),
                'duration': duration,
                'status': 'completed' if result.returncode == 0 else 'failed',
                'raw_output': result.stdout,
                'error_output': result.stderr,
                'output_files': {
                    'txt': f"{output_base}.txt",
                    'xml': f"{output_base}.xml"
                }
            }

            # Parse XML for structured data
            if os.path.exists(f"{output_base}.xml"):
                scan_results['parsed_data'] = self.parse_xml_output(f"{output_base}.xml")

            return scan_results

        except subprocess.TimeoutExpired:
            return {
                'command': command,
                'target': target,
                'status': 'timeout',
                'error': 'Scan exceeded 1 hour timeout'
            }
        except Exception as e:
            return {
                'command': command,
                'target': target,
                'status': 'error',
                'error': str(e)
            }

    def parse_xml_output(self, xml_file):
        """
        Parse NMAP XML output to extract structured data

        Args:
            xml_file (str): Path to XML file

        Returns:
            dict: Parsed scan data
        """
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            parsed = {
                'hosts': [],
                'scan_info': {}
            }

            # Extract scan info
            scaninfo = root.find('scaninfo')
            if scaninfo is not None:
                parsed['scan_info'] = dict(scaninfo.attrib)

            # Extract host information
            for host in root.findall('host'):
                host_data = {
                    'addresses': {},
                    'hostnames': [],
                    'ports': [],
                    'os': {},
                    'status': ''
                }

                # Status
                status = host.find('status')
                if status is not None:
                    host_data['status'] = status.get('state', 'unknown')

                # Addresses
                for addr in host.findall('address'):
                    addr_type = addr.get('addrtype')
                    addr_value = addr.get('addr')
                    host_data['addresses'][addr_type] = addr_value
                    if addr_type == 'mac':
                        host_data['mac_vendor'] = addr.get('vendor', '')

                # Hostnames
                hostnames = host.find('hostnames')
                if hostnames is not None:
                    for hostname in hostnames.findall('hostname'):
                        host_data['hostnames'].append({
                            'name': hostname.get('name'),
                            'type': hostname.get('type')
                        })

                # Ports
                ports_elem = host.find('ports')
                if ports_elem is not None:
                    for port in ports_elem.findall('port'):
                        port_data = {
                            'port': int(port.get('portid')),
                            'protocol': port.get('protocol'),
                            'state': '',
                            'service': {},
                            'scripts': []
                        }

                        # Port state
                        state = port.find('state')
                        if state is not None:
                            port_data['state'] = state.get('state')

                        # Service info
                        service = port.find('service')
                        if service is not None:
                            port_data['service'] = {
                                'name': service.get('name', ''),
                                'product': service.get('product', ''),
                                'version': service.get('version', ''),
                                'extrainfo': service.get('extrainfo', ''),
                                'ostype': service.get('ostype', ''),
                                'method': service.get('method', ''),
                                'conf': service.get('conf', '')
                            }

                        # NSE Script results
                        for script in port.findall('script'):
                            script_data = {
                                'id': script.get('id'),
                                'output': script.get('output', '')
                            }
                            # Parse tables if present
                            tables = []
                            for table in script.findall('.//table'):
                                table_data = {}
                                for elem in table.findall('elem'):
                                    key = elem.get('key', 'value')
                                    table_data[key] = elem.text
                                tables.append(table_data)
                            if tables:
                                script_data['tables'] = tables

                            port_data['scripts'].append(script_data)

                        host_data['ports'].append(port_data)

                # OS detection
                os_elem = host.find('os')
                if os_elem is not None:
                    osmatch = os_elem.find('osmatch')
                    if osmatch is not None:
                        host_data['os'] = {
                            'name': osmatch.get('name'),
                            'accuracy': osmatch.get('accuracy'),
                            'line': osmatch.get('line')
                        }
                        # Get OS classes
                        osclass = osmatch.find('osclass')
                        if osclass is not None:
                            host_data['os']['type'] = osclass.get('type')
                            host_data['os']['vendor'] = osclass.get('vendor')
                            host_data['os']['osfamily'] = osclass.get('osfamily')
                            host_data['os']['osgen'] = osclass.get('osgen')

                parsed['hosts'].append(host_data)

            return parsed

        except Exception as e:
            return {'error': f"Failed to parse XML: {str(e)}"}

    def get_common_scripts(self, scan_purpose):
        """
        Return common NSE scripts for specific purposes

        Args:
            scan_purpose (str): Purpose of scan (webapp, vuln, enum, etc.)

        Returns:
            list: List of NSE script names
        """
        script_sets = {
            'webapp': [
                'http-enum', 'http-headers', 'http-methods', 'http-title',
                'http-robots.txt', 'http-sitemap-generator', 'http-git',
                'http-svn-enum', 'http-backup-finder'
            ],
            'vuln': [
                'vulners', 'vulscan', 'vuln'
            ],
            'enum': [
                'smb-enum-shares', 'smb-enum-users', 'smb-os-discovery',
                'ftp-anon', 'ssh-auth-methods', 'mysql-info',
                'dns-brute', 'dns-zone-transfer'
            ],
            'auth': [
                'ssh-brute', 'ftp-brute', 'http-brute',
                'mysql-brute', 'smb-brute'
            ],
            'safe': [
                'default', 'safe', 'discovery'
            ]
        }

        return script_sets.get(scan_purpose, [])

    def banner_grab(self, target, port):
        """
        Manual banner grabbing for a specific port

        Args:
            target (str): Target IP/hostname
            port (int): Port number

        Returns:
            dict: Banner information
        """
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))

            # Send generic probe
            sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()

            return {
                'port': port,
                'banner': banner.strip(),
                'method': 'socket'
            }
        except Exception as e:
            return {
                'port': port,
                'error': str(e)
            }
