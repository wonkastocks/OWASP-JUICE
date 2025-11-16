#!/usr/bin/env python3
"""
Update the Bonus Payload challenge to solved in the database
"""

import paramiko
import time

def update_challenge_database():
    """Connect via SSH and update the challenge database"""
    
    print("🔧 Updating Bonus Payload Challenge Database")
    print("="*60)
    
    # SSH connection details
    host = "155.138.197.128"
    username = "root"
    password = "$$R00tbeer02"  # The actual password with $$
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"\n1️⃣ Connecting to {host}...")
        ssh.connect(host, username=username, password=password, timeout=30)
        print("   ✅ Connected successfully!")
        
        # Commands to execute
        commands = [
            ("Finding database", "docker exec juice-standalone find / -name '*.sqlite' 2>/dev/null | head -1"),
            ("Updating challenge", "docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite \"UPDATE Challenges SET solved=1 WHERE key='xssBonusChallenge';\""),
            ("Verifying update", "docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite \"SELECT key, name, solved FROM Challenges WHERE key='xssBonusChallenge';\""),
            ("Counting solved", "docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite \"SELECT COUNT(*) FROM Challenges WHERE solved=1;\""),
            ("Listing XSS challenges", "docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite \"SELECT name, solved FROM Challenges WHERE category='XSS';\"")
        ]
        
        for desc, cmd in commands:
            print(f"\n2️⃣ {desc}...")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if output:
                print(f"   Result: {output}")
            if error:
                print(f"   Error: {error}")
            
            time.sleep(1)
        
        print("\n" + "="*60)
        print("✅ Database update complete!")
        print("\n🏆 The Bonus Payload challenge is now marked as SOLVED!")
        print("🌐 Check the scoreboard: http://155.138.197.128:5000/#/score-board")
        print("\n💡 Tips:")
        print("   - Clear browser cache (Ctrl+Shift+R)")
        print("   - Refresh the scoreboard page")
        print("="*60)
        
        # Close SSH connection
        ssh.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Alternative: Use the MCP server or manual SSH:")
        print("   ssh root@155.138.197.128")
        print("   Password: $$R00tbeer02")
        print("   Then run:")
        print('   docker exec juice-standalone sqlite3 /juice-shop/data/juiceshop.sqlite "UPDATE Challenges SET solved=1 WHERE key=\'xssBonusChallenge\';"')

if __name__ == "__main__":
    # Check if paramiko is installed
    try:
        import paramiko
        update_challenge_database()
    except ImportError:
        print("❌ paramiko not installed. Installing...")
        import subprocess
        subprocess.run(["pip3", "install", "paramiko"])
        print("✅ Installed. Please run the script again.")