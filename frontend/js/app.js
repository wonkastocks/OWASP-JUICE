/**
 * NMAP Optimizer Frontend Application
 * Handles UI interactions and API calls
 */

const API_BASE = '/api';

// State management
let currentScanId = null;
let scanInterval = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initScannerForm();
    initTemplateButtons();
    initFingerprintingTools();
    checkHealth();
    loadAssets();
    loadStats();
});

// Health check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();

        const statusEl = document.getElementById('healthStatus');
        if (data.status === 'healthy') {
            statusEl.querySelector('.status-text').textContent =
                `System Healthy ${data.ai_enabled ? '| AI Enabled' : '| AI Disabled'}`;
            statusEl.querySelector('.status-dot').style.background = '#10b981';
        }
    } catch (error) {
        const statusEl = document.getElementById('healthStatus');
        statusEl.querySelector('.status-text').textContent = 'System Offline';
        statusEl.querySelector('.status-dot').style.background = '#ef4444';
    }
}

// Navigation
function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active button
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Show corresponding section
            const sectionId = btn.dataset.section + '-section';
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');

            // Load section data
            if (btn.dataset.section === 'assets') {
                loadAssets();
            } else if (btn.dataset.section === 'stats') {
                loadStats();
            }
        });
    });
}

// Scanner Form
function initScannerForm() {
    const startBtn = document.getElementById('startScanBtn');
    const targetInput = document.getElementById('target');
    const requestInput = document.getElementById('scanRequest');

    startBtn.addEventListener('click', async () => {
        const target = targetInput.value.trim();
        const request = requestInput.value.trim() || 'quick scan';

        if (!target) {
            alert('Please enter a target IP or hostname');
            return;
        }

        await startScan(target, request);
    });
}

// Template buttons
function initTemplateButtons() {
    const templates = {
        'quick': 'Do a quick scan of the most common ports',
        'full': 'Perform a comprehensive scan with OS detection and service enumeration on all ports',
        'stealth': 'Execute a stealthy scan to avoid detection by IDS/IPS systems',
        'webapp': 'Scan for web applications and enumerate HTTP services with vulnerability scripts',
        'vuln': 'Run vulnerability detection scripts and check for known exploits'
    };

    document.querySelectorAll('.template-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const template = btn.dataset.template;
            document.getElementById('scanRequest').value = templates[template];
        });
    });
}

// Start Scan
async function startScan(target, request) {
    const progressEl = document.getElementById('scanProgress');
    const resultsEl = document.getElementById('scanResults');
    const detailsEl = document.getElementById('scanDetails');

    // Show progress, hide results
    progressEl.classList.remove('hidden');
    resultsEl.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE}/scan/request`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target, request })
        });

        const data = await response.json();

        if (response.ok) {
            currentScanId = data.scan_id;

            // Display scan parameters
            detailsEl.innerHTML = `
                <p><strong>Scan ID:</strong> ${data.scan_id}</p>
                <p><strong>Target:</strong> ${target}</p>
                <p><strong>Scan Type:</strong> ${data.scan_params.scan_type}</p>
                <p><strong>Ports:</strong> ${data.scan_params.ports}</p>
                <p><strong>Reasoning:</strong> ${data.scan_params.reasoning || 'N/A'}</p>
            `;

            // Poll for results
            scanInterval = setInterval(() => pollScanStatus(currentScanId), 3000);
        } else {
            throw new Error(data.error || 'Scan failed to start');
        }
    } catch (error) {
        progressEl.classList.add('hidden');
        alert(`Error: ${error.message}`);
    }
}

// Poll Scan Status
async function pollScanStatus(scanId) {
    try {
        const response = await fetch(`${API_BASE}/scan/${scanId}`);
        const data = await response.json();

        if (data.status === 'completed' || data.status === 'failed' || data.status === 'error') {
            clearInterval(scanInterval);
            displayScanResults(data);
        }
    } catch (error) {
        console.error('Error polling scan status:', error);
    }
}

// Display Scan Results
function displayScanResults(scan) {
    const progressEl = document.getElementById('scanProgress');
    const resultsEl = document.getElementById('scanResults');
    const contentEl = document.getElementById('resultsContent');

    progressEl.classList.add('hidden');
    resultsEl.classList.remove('hidden');

    let html = `
        <div class="result-header">
            <p><strong>Status:</strong> <span class="text-${scan.status === 'completed' ? 'success' : 'danger'}">${scan.status}</span></p>
            <p><strong>Duration:</strong> ${scan.duration}s</p>
        </div>
    `;

    // AI Analysis
    if (scan.ai_analysis) {
        const analysis = typeof scan.ai_analysis === 'string' ?
            JSON.parse(scan.ai_analysis) : scan.ai_analysis;

        html += `
            <div class="ai-analysis">
                <h4>🤖 AI Analysis</h4>
                <p><strong>Summary:</strong> ${analysis.summary}</p>
                <p><strong>Risk Level:</strong> <span class="risk-badge risk-${analysis.risk_level}">${analysis.risk_level}</span></p>

                ${analysis.risks && analysis.risks.length > 0 ? `
                    <div class="risks">
                        <strong>Security Risks:</strong>
                        <ul>
                            ${analysis.risks.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${analysis.notable_services && analysis.notable_services.length > 0 ? `
                    <div class="services">
                        <strong>Notable Services:</strong>
                        <ul>
                            ${analysis.notable_services.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}

                ${analysis.recommendations && analysis.recommendations.length > 0 ? `
                    <div class="recommendations">
                        <strong>Recommendations:</strong>
                        <ul>
                            ${analysis.recommendations.map(r => `<li>${r}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }

    // Raw output
    html += `
        <details>
            <summary>View Raw Output</summary>
            <pre>${escapeHtml(scan.raw_output || 'No output available')}</pre>
        </details>
    `;

    contentEl.innerHTML = html;

    // Reload assets to show new data
    loadAssets();
}

// Load Assets
async function loadAssets() {
    try {
        const response = await fetch(`${API_BASE}/assets`);
        const assets = await response.json();

        const container = document.getElementById('assetsList');

        if (assets.length === 0) {
            container.innerHTML = '<p class="text-secondary">No assets discovered yet. Run a scan to get started.</p>';
            return;
        }

        container.innerHTML = assets.map(asset => `
            <div class="asset-card" onclick="viewAsset(${asset.id})">
                <div class="asset-header">
                    <span class="asset-ip">${asset.ip_address}</span>
                    <span class="status-badge status-${asset.status}">${asset.status}</span>
                </div>
                <p class="text-secondary">${asset.hostname || 'No hostname'}</p>
                <p class="text-secondary">${asset.os_guess || 'OS unknown'}</p>
                <div style="margin-top: 1rem;">
                    <span class="risk-badge risk-${asset.risk_level}">${asset.risk_level} risk</span>
                </div>
                <div style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-secondary);">
                    <p>Open Ports: ${asset.open_ports || 0}</p>
                    <p>Scans: ${asset.total_scans || 0}</p>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading assets:', error);
    }
}

// View Asset Details
async function viewAsset(assetId) {
    try {
        const response = await fetch(`${API_BASE}/assets/${assetId}`);
        const asset = await response.json();

        const modal = document.getElementById('assetModal');
        const detailsEl = document.getElementById('assetDetails');

        let html = `
            <h2>${asset.ip_address}</h2>
            <p class="text-secondary">${asset.hostname || 'No hostname'}</p>

            <div style="margin: 1.5rem 0;">
                <span class="status-badge status-${asset.status}">${asset.status}</span>
                <span class="risk-badge risk-${asset.risk_level}">${asset.risk_level} risk</span>
            </div>

            <div class="asset-info">
                <p><strong>OS:</strong> ${asset.os_guess || 'Unknown'} ${asset.os_accuracy ? `(${asset.os_accuracy}% confidence)` : ''}</p>
                <p><strong>MAC:</strong> ${asset.mac_address || 'Unknown'}</p>
                <p><strong>Vendor:</strong> ${asset.vendor || 'Unknown'}</p>
                <p><strong>First Seen:</strong> ${new Date(asset.first_seen).toLocaleString()}</p>
                <p><strong>Last Seen:</strong> ${new Date(asset.last_seen).toLocaleString()}</p>
            </div>
        `;

        // Open Ports
        if (asset.ports && asset.ports.length > 0) {
            html += `
                <h3 style="margin-top: 2rem;">Open Ports</h3>
                <table style="width: 100%; margin-top: 1rem;">
                    <thead>
                        <tr>
                            <th>Port</th>
                            <th>Service</th>
                            <th>Version</th>
                            <th>State</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${asset.ports.map(port => `
                            <tr>
                                <td>${port.port_number}/${port.protocol}</td>
                                <td>${port.service || 'unknown'}</td>
                                <td>${port.version || '-'}</td>
                                <td><span class="status-badge status-${port.state === 'open' ? 'up' : 'down'}">${port.state}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }

        // Notes
        html += `
            <h3 style="margin-top: 2rem;">Notes</h3>
            <div id="notesList">
                ${asset.notes && asset.notes.length > 0 ?
                    asset.notes.map(note => `
                        <div class="note-item" style="background: var(--dark-bg); padding: 1rem; margin: 0.5rem 0; border-radius: 6px;">
                            <strong>${note.title}</strong>
                            <p style="margin-top: 0.5rem;">${note.content}</p>
                            <small class="text-secondary">${new Date(note.created_at).toLocaleString()}</small>
                        </div>
                    `).join('') :
                    '<p class="text-secondary">No notes yet</p>'
                }
            </div>
            <button class="btn btn-secondary" style="margin-top: 1rem;" onclick="addNote(${assetId})">Add Note</button>
        `;

        detailsEl.innerHTML = html;
        modal.classList.remove('hidden');
    } catch (error) {
        console.error('Error viewing asset:', error);
    }
}

// Close modal
document.querySelector('.close-btn')?.addEventListener('click', () => {
    document.getElementById('assetModal').classList.add('hidden');
});

// Add Note
async function addNote(assetId) {
    const title = prompt('Note title:');
    if (!title) return;

    const content = prompt('Note content:');
    if (!content) return;

    try {
        const response = await fetch(`${API_BASE}/assets/${assetId}/notes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content, category: 'general' })
        });

        if (response.ok) {
            viewAsset(assetId); // Refresh
        }
    } catch (error) {
        console.error('Error adding note:', error);
    }
}

// Fingerprinting Tools
function initFingerprintingTools() {
    // DNS
    document.getElementById('dnsBtn')?.addEventListener('click', async () => {
        const target = document.getElementById('dnsTarget').value.trim();
        if (!target) return;

        const resultsEl = document.getElementById('dnsResults');
        resultsEl.textContent = 'Loading...';

        try {
            const response = await fetch(`${API_BASE}/fingerprint/dns`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target })
            });
            const data = await response.json();
            resultsEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            resultsEl.textContent = `Error: ${error.message}`;
        }
    });

    // Banner
    document.getElementById('bannerBtn')?.addEventListener('click', async () => {
        const target = document.getElementById('bannerTarget').value.trim();
        const port = document.getElementById('bannerPort').value.trim();
        if (!target || !port) return;

        const resultsEl = document.getElementById('bannerResults');
        resultsEl.textContent = 'Grabbing banner...';

        try {
            const response = await fetch(`${API_BASE}/fingerprint/banner`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target, port: parseInt(port) })
            });
            const data = await response.json();
            resultsEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            resultsEl.textContent = `Error: ${error.message}`;
        }
    });

    // OS
    document.getElementById('osBtn')?.addEventListener('click', async () => {
        const target = document.getElementById('osTarget').value.trim();
        if (!target) return;

        const resultsEl = document.getElementById('osResults');
        resultsEl.textContent = 'Detecting OS... (this may take a while)';

        try {
            const response = await fetch(`${API_BASE}/fingerprint/os`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target })
            });
            const data = await response.json();
            resultsEl.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            resultsEl.textContent = `Error: ${error.message}`;
        }
    });
}

// Load Stats
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();

        const container = document.getElementById('statsContent');
        container.innerHTML = `
            <div class="stat-card">
                <div class="stat-value">${stats.total_assets}</div>
                <div class="stat-label">Total Assets</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.assets_up}</div>
                <div class="stat-label">Assets Up</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.total_scans}</div>
                <div class="stat-label">Total Scans</div>
            </div>
            <div class="stat-card">
                <div class="stat-value text-danger">${stats.risk_distribution.critical + stats.risk_distribution.high}</div>
                <div class="stat-label">High Risk Assets</div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Utility Functions
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
