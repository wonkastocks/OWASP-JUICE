#!/bin/bash

# Script to permanently change hostname in Ubuntu
# Usage: ./change_hostname_ubuntu.sh <new-hostname>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <new-hostname>"
    echo "Example: $0 my-server"
    exit 1
fi

NEW_HOSTNAME=$1
OLD_HOSTNAME=$(hostname)

echo "Changing hostname from '$OLD_HOSTNAME' to '$NEW_HOSTNAME'"

# 1. Update the current hostname (temporary until reboot)
sudo hostnamectl set-hostname $NEW_HOSTNAME

# 2. Update /etc/hostname file (persistent)
echo $NEW_HOSTNAME | sudo tee /etc/hostname

# 3. Update /etc/hosts file
sudo sed -i "s/127.0.1.1.*$/127.0.1.1\t$NEW_HOSTNAME/" /etc/hosts

# If the old hostname exists in /etc/hosts, replace it
if grep -q "$OLD_HOSTNAME" /etc/hosts; then
    sudo sed -i "s/$OLD_HOSTNAME/$NEW_HOSTNAME/g" /etc/hosts
else
    # Add the new hostname if not present
    if ! grep -q "127.0.1.1" /etc/hosts; then
        echo "127.0.1.1    $NEW_HOSTNAME" | sudo tee -a /etc/hosts
    fi
fi

# 4. For cloud instances, update cloud-init configuration
if [ -f /etc/cloud/cloud.cfg ]; then
    echo "Updating cloud-init configuration..."
    # Preserve hostname across reboots on cloud instances
    sudo sed -i 's/preserve_hostname: false/preserve_hostname: true/g' /etc/cloud/cloud.cfg
fi

# 5. Verify the changes
echo ""
echo "Hostname has been changed. Verification:"
echo "Current hostname: $(hostname)"
echo "Hostname from hostnamectl: $(hostnamectl | grep "Static hostname" | cut -d: -f2 | xargs)"
echo ""
echo "Contents of /etc/hostname:"
cat /etc/hostname
echo ""
echo "Relevant line in /etc/hosts:"
grep "127.0.1.1" /etc/hosts
echo ""
echo "✅ Hostname change complete. Reboot recommended for full effect."
echo "To apply immediately without reboot, run: exec bash"