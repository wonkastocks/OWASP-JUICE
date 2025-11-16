#!/usr/bin/env python3

import subprocess
import sys
import os

# Server details
SERVER = "155.138.197.128"
USER = "root"
PASSWORD = "$R00tbeer02"
LOCAL_FILE = "/Users/walterbarr_1/sql-injection-lab/clean_login.php"
REMOTE_TEMP = "/root/clean_login.php"
REMOTE_FINAL = "/var/www/html/login.php"

print("Deploying clean login page to server...")
print("=" * 50)

# Create expect script for deployment
expect_script = f'''#!/usr/bin/expect -f

set timeout 30
set password {{{PASSWORD}}}

# Copy file to server
spawn scp {LOCAL_FILE} {USER}@{SERVER}:{REMOTE_TEMP}
expect {{
    "password:" {{
        send "$password\\r"
        exp_continue
    }}
    "yes/no" {{
        send "yes\\r"
        exp_continue
    }}
    eof {{
        # File transfer complete
    }}
}}

# SSH and deploy
spawn ssh {USER}@{SERVER}
expect {{
    "password:" {{
        send "$password\\r"
    }}
    "yes/no" {{
        send "yes\\r"
        expect "password:"
        send "$password\\r"
    }}
}}

expect "# "
send "cp {REMOTE_FINAL} {REMOTE_FINAL}.backup\\r"
expect "# "
send "mv {REMOTE_TEMP} {REMOTE_FINAL}\\r"
expect "# "
send "chown www-data:www-data {REMOTE_FINAL}\\r"
expect "# "
send "chmod 644 {REMOTE_FINAL}\\r"
expect "# "
send "systemctl restart apache2\\r"
expect "# "
send "echo 'Deployment complete!'\\r"
expect "# "
send "exit\\r"
expect eof
'''

# Write expect script to temp file
temp_script = "/tmp/deploy_temp.exp"
with open(temp_script, 'w') as f:
    f.write(expect_script)

# Make it executable
os.chmod(temp_script, 0o755)

# Run the expect script
try:
    result = subprocess.run(['expect', temp_script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    if result.returncode == 0:
        print("\n✅ Clean login page deployed successfully!")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        
except Exception as e:
    print(f"Error running deployment: {e}")
finally:
    # Clean up temp script
    if os.path.exists(temp_script):
        os.remove(temp_script)

print("=" * 50)