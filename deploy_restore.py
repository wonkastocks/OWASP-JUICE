#!/usr/bin/env python3
"""
Deploy and run the restore script on the server
"""

import subprocess
import time
import sys

print("="*50)
print("🚀 DEPLOYING RESTORE SCRIPT")
print("="*50)

# Server details
HOST = "155.138.197.128"
USER = "root"
SCRIPT_LOCAL = "/Users/walterbarr_1/sql-injection-lab/restore_all_services.sh"
SCRIPT_REMOTE = "/tmp/restore_all_services.sh"

print("\n📋 Manual deployment required due to password complexity")
print("="*50)

print("\n1️⃣ First, copy the script:")
print(f"   scp {SCRIPT_LOCAL} {USER}@{HOST}:{SCRIPT_REMOTE}")
print("   Password: $Hg5sD&8Lp@9")

print("\n2️⃣ Then SSH to the server:")
print(f"   ssh {USER}@{HOST}")
print("   Password: $Hg5sD&8Lp@9")

print("\n3️⃣ Run the restore script:")
print(f"   bash {SCRIPT_REMOTE}")

print("\n4️⃣ The script will:")
print("   ✅ Start Apache web server")
print("   ✅ Create CTF landing page")
print("   ✅ Start Juice Shop Docker")
print("   ✅ Install Juice Shop Standalone on port 4000")
print("   ✅ Configure firewall")
print("   ✅ Test all services")

print("\n5️⃣ After completion, access:")
print("   🌐 http://155.138.197.128 - CTF Platform")
print("   🌐 http://155.138.197.128:4000 - Juice Shop (No filters!)")
print("   🌐 https://juice3.wonkatech.org - Juice Shop Docker")

print("\n" + "="*50)
print("💡 For DOM XSS testing:")
print("="*50)
print("1. Open http://155.138.197.128:4000")
print("2. Press F12 for browser console")
print("3. Type: location.href = '#/search?q=<iframe src=\"javascript:alert(1)\">'")
print("4. The XSS will work on the standalone instance!")

# Try using sshpass if available
print("\n" + "="*50)
print("Checking for sshpass...")
try:
    result = subprocess.run(['which', 'sshpass'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ sshpass found, attempting automated deployment...")
        
        # Copy file
        cmd1 = f"sshpass -p '$Hg5sD&8Lp@9' scp {SCRIPT_LOCAL} {USER}@{HOST}:{SCRIPT_REMOTE}"
        print(f"Copying script...")
        result = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Script copied!")
            
            # Execute script
            cmd2 = f"sshpass -p '$Hg5sD&8Lp@9' ssh {USER}@{HOST} 'bash {SCRIPT_REMOTE}'"
            print("Executing restore script (this will take a few minutes)...")
            result = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
            print(result.stdout)
            if result.returncode == 0:
                print("✅ Restore completed successfully!")
        else:
            print("❌ Copy failed, use manual steps above")
    else:
        print("❌ sshpass not found")
        print("Install with: brew install hudochenkov/sshpass/sshpass")
        print("\nUse the manual steps above to deploy")
except Exception as e:
    print(f"Error: {e}")
    print("\nUse the manual steps above to deploy")