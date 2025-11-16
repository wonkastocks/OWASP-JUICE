#!/bin/bash

# Fix script to update user dashboard to use HTTPS URLs

echo "🔧 Fixing user dashboard to use HTTPS URLs..."

# Create PHP patch to update dashboard.php
cat > /tmp/dashboard_https_fix.php << 'EOF'
<?php
// Function to get HTTPS URL for container
function getContainerHTTPSUrl($port) {
    if ($port >= 3001 && $port <= 3020) {
        $instanceNum = $port - 3000;
        return "https://juice{$instanceNum}.wonkatech.org";
    }
    return null;
}

// Function to update container launch links
function updateContainerLinks() {
    ?>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Find all launch instance links
        var links = document.querySelectorAll('a[href*="155.138.197.128:30"]');
        links.forEach(function(link) {
            var href = link.href;
            var portMatch = href.match(/:(\d{4})/);
            if (portMatch) {
                var port = parseInt(portMatch[1]);
                if (port >= 3001 && port <= 3020) {
                    var instanceNum = port - 3000;
                    var httpsUrl = 'https://juice' + instanceNum + '.wonkatech.org';
                    link.href = httpsUrl;
                    link.innerHTML = link.innerHTML.replace(/http:\/\/[^<]+/, httpsUrl);
                }
            }
        });
        
        // Also update any buttons or onclick handlers
        var buttons = document.querySelectorAll('button[onclick*="155.138.197.128:30"]');
        buttons.forEach(function(button) {
            var onclick = button.getAttribute('onclick');
            var portMatch = onclick.match(/:(\d{4})/);
            if (portMatch) {
                var port = parseInt(portMatch[1]);
                if (port >= 3001 && port <= 3020) {
                    var instanceNum = port - 3000;
                    var httpsUrl = 'https://juice' + instanceNum + '.wonkatech.org';
                    button.setAttribute('onclick', onclick.replace(/http:\/\/[^'"]+/, httpsUrl));
                }
            }
        });
    });
    </script>
    <?php
}
?>
EOF

echo "✅ Dashboard HTTPS fix created"