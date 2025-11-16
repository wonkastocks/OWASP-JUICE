#!/usr/bin/env python3
"""
Test admin authentication flow
"""

import requests

session = requests.Session()

print("Testing admin authentication...")

# Login
login_url = "https://wonkatech.org/admin/admin_login.php"
login_data = {
    'email': 'admin@wonkatech.org',
    'password': 'R00tbeer',
    'login': 'Login'
}

response = session.post(login_url, data=login_data, allow_redirects=False)
print(f"Login response status: {response.status_code}")
print(f"Redirect location: {response.headers.get('Location', 'No redirect')}")

# Check cookies
print(f"Session cookies: {session.cookies.get_dict()}")

# Try to access dashboard
dashboard = session.get("https://wonkatech.org/admin/dashboard.php", allow_redirects=False)
print(f"\nDashboard access status: {dashboard.status_code}")
if dashboard.status_code == 302:
    print(f"Dashboard redirects to: {dashboard.headers.get('Location')}")
elif dashboard.status_code == 200:
    print("Dashboard accessible!")
    if "CTF Admin Dashboard" in dashboard.text:
        print("✅ Admin dashboard is working!")
    elif "admin_login.php" in dashboard.text:
        print("❌ Dashboard shows login page")
    else:
        print(f"Dashboard content: {dashboard.text[:200]}")