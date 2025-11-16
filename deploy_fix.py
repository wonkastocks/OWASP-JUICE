#!/usr/bin/env python3
"""
Deploy fix to server using paramiko
"""

import paramiko
import os
import time

# Server details
HOST = "155.138.197.128"
USER = "root"
PASSWORD = "$Hg5sD&8Lp@9"  # Password with $ at start
PORT = 22

# Files to copy
LOCAL_SCRIPT = "/Users/walterbarr_1/sql-injection-lab/fix_ctf_platform.sh"
REMOTE_SCRIPT = "/tmp/fix_ctf_platform.sh"

def deploy_fix():
    """Deploy and execute the fix script"""
    
    print("🔧 Connecting to server...")
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect
        ssh.connect(HOST, PORT, USER, PASSWORD)
        print("✅ Connected successfully!")
        
        # Copy script using SFTP
        print("📤 Copying fix script...")
        sftp = ssh.open_sftp()
        sftp.put(LOCAL_SCRIPT, REMOTE_SCRIPT)
        sftp.chmod(REMOTE_SCRIPT, 0o755)
        sftp.close()
        print("✅ Script copied!")
        
        # Execute the script
        print("🚀 Executing fix script...")
        stdin, stdout, stderr = ssh.exec_command(f"bash {REMOTE_SCRIPT}")
        
        # Print output in real-time
        for line in stdout:
            print(line.strip())
        
        # Check for errors
        errors = stderr.read().decode()
        if errors:
            print(f"⚠️ Errors: {errors}")
        
        # Close connection
        ssh.close()
        print("\n✅ Fix deployment complete!")
        
        print("\n📝 Next steps:")
        print("1. Check https://wonkatech.org - CTF platform")
        print("2. Check https://juice3.wonkatech.org - Juice Shop Docker")
        print("3. Check http://155.138.197.128:4000 - Juice Shop Standalone")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nManual steps:")
        print(f"1. SSH to server: ssh root@{HOST}")
        print(f"2. Password: {PASSWORD}")
        print(f"3. Run: bash {REMOTE_SCRIPT}")

if __name__ == "__main__":
    # Check if paramiko is installed
    try:
        import paramiko
        deploy_fix()
    except ImportError:
        print("❌ paramiko not installed!")
        print("Install with: pip3 install paramiko")
        print("\nManual deployment steps:")
        print(f"1. scp {LOCAL_SCRIPT} root@{HOST}:{REMOTE_SCRIPT}")
        print(f"2. ssh root@{HOST}")
        print(f"3. bash {REMOTE_SCRIPT}")
        print(f"\nPassword: {PASSWORD}")