# NMAP OPTIMIZER

An AI-powered network reconnaissance and security auditing platform that combines NMAP's scanning capabilities with artificial intelligence to interpret natural language scan requests, analyze results, and maintain a comprehensive asset database.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![NMAP](https://img.shields.io/badge/nmap-required-green.svg)

## ⚠️ Legal Disclaimer

**AUTHORIZED USE ONLY**: This tool is designed exclusively for authorized security testing and network auditing purposes. Users must:

- Have explicit written permission to scan target systems
- Only scan networks and systems they own or are authorized to test
- Comply with all applicable local, state, and federal laws
- Use this tool responsibly and ethically

Unauthorized network scanning may be illegal in your jurisdiction. The developers assume no liability for misuse of this tool.

## Features

### 🤖 AI-Powered Scanning
- **Natural Language Interface**: Describe scans in plain English
- **Intelligent Interpretation**: AI converts requests to optimal NMAP commands
- **Automated Analysis**: AI interprets scan results and identifies security risks
- **Smart Recommendations**: Suggests next steps based on findings

### 🔍 Comprehensive Reconnaissance
- **Port Scanning**: All standard NMAP scan types (TCP, UDP, SYN, etc.)
- **Service Detection**: Version detection and banner grabbing
- **OS Fingerprinting**: Operating system identification
- **NSE Scripts**: Automated execution of NMAP scripts
- **DNS Enumeration**: Complete DNS record gathering
- **Web App Discovery**: HTTP/HTTPS service enumeration

### 📊 Asset Management
- **Persistent Database**: SQLite database for all discovered assets
- **Note-Taking**: Add custom notes and observations to hosts
- **Risk Assessment**: Automated risk level classification
- **Historical Tracking**: Track changes over time
- **Search & Filter**: Easy asset discovery and management

### 🎯 Web Interface
- **Modern Dashboard**: Clean, responsive web interface
- **Real-time Updates**: Live scan progress monitoring
- **Visual Analytics**: Statistics and risk distribution charts
- **Export Capabilities**: Download results in multiple formats

## Architecture

```
NMAP-OPTIMIZER/
├── backend/                    # Flask API server
│   ├── app.py                 # Main application & API endpoints
│   ├── models.py              # Database models (SQLAlchemy)
│   ├── nmap_executor.py       # NMAP wrapper & execution
│   ├── ai_analyzer.py         # OpenAI integration & analysis
│   └── fingerprinting.py      # DNS, banner grabbing, etc.
├── frontend/                   # Web interface
│   ├── index.html             # Main HTML
│   ├── css/style.css          # Styling
│   └── js/app.js              # Frontend logic
├── config/                     # Configuration files
│   ├── .env.example           # Environment variables template
│   └── config.yaml            # Application configuration
├── database/                   # SQLite database storage
├── scans/                      # Raw NMAP output files
├── logs/                       # Application logs
└── requirements.txt            # Python dependencies
```

## Installation

### Prerequisites

- **Python 3.8+**
- **NMAP**: Latest version installed and accessible via command line
- **OpenAI API Key**: For AI features (optional but recommended)

### Step 1: Install NMAP

#### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install nmap
```

#### Linux (CentOS/RHEL)
```bash
sudo yum install nmap
```

#### macOS
```bash
brew install nmap
```

#### Windows
Download from [nmap.org](https://nmap.org/download.html) and install

### Step 2: Clone Repository

```bash
git clone https://github.com/wonkastocks/NMAP-OPTIMIZER.git
cd NMAP-OPTIMIZER
```

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp config/.env.example config/.env

# Edit configuration (add your OpenAI API key)
nano config/.env
```

**Important**: Add your OpenAI API key to `config/.env`:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 5: Initialize Database

```bash
cd backend
python3 app.py
```

The database will be automatically created on first run.

## Usage

### Starting the Application

```bash
cd backend
python3 app.py
```

The web interface will be available at: **http://localhost:5000**

### Web Interface Usage

#### 1. **Scanner Tab**
- Enter target IP address or hostname
- Describe your scan in natural language
- Use quick templates or write custom requests
- Monitor scan progress in real-time
- View AI-analyzed results

**Example Requests:**
- "Do a quick scan looking for web servers"
- "Perform a comprehensive scan with OS detection"
- "Stealthy scan to avoid IDS detection"
- "Check for vulnerabilities on this web server"

#### 2. **Assets Tab**
- View all discovered hosts
- Click on assets for detailed information
- See open ports, services, and versions
- Add notes and observations

#### 3. **Fingerprinting Tab**
- **DNS Enumeration**: Lookup DNS records
- **Banner Grabbing**: Extract service banners
- **OS Fingerprinting**: Detect operating systems

#### 4. **Statistics Tab**
- View scan metrics
- Risk distribution
- Asset status overview

### API Usage

The platform provides a RESTful API for programmatic access:

#### Start a Scan
```bash
curl -X POST http://localhost:5000/api/scan/request \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.1",
    "request": "comprehensive scan with service detection"
  }'
```

#### Get Scan Results
```bash
curl http://localhost:5000/api/scan/<scan_id>
```

#### List Assets
```bash
curl http://localhost:5000/api/assets
```

#### Get Asset Details
```bash
curl http://localhost:5000/api/assets/<asset_id>
```

#### Add Note to Asset
```bash
curl -X POST http://localhost:5000/api/assets/<asset_id>/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Finding",
    "content": "Discovered outdated Apache version",
    "category": "vulnerability"
  }'
```

## Configuration

### Environment Variables (`config/.env`)

```bash
# AI Configuration
OPENAI_API_KEY=sk-your-key-here

# Flask Settings
FLASK_SECRET_KEY=random-secret-key
FLASK_ENV=production
FLASK_DEBUG=False

# Database
DATABASE_URI=sqlite:///../database/assets.db

# NMAP Settings
NMAP_TIMEOUT=3600
SCAN_OUTPUT_DIR=../scans
```

### Scan Profiles (`config/config.yaml`)

Customize default scan profiles:

```yaml
profiles:
  quick:
    timing: 4
    ports: "--top-ports 100"
    description: "Fast scan"

  full:
    timing: 3
    ports: "-p-"
    scripts: ["default"]
    description: "All ports"
```

## Examples

### Example 1: Quick Web Server Scan

**Request**: "Scan for web servers and check what's running"

**AI Interpretation**:
- Scan Type: webapp
- Ports: 80, 443, 8080, 8443
- Scripts: http-enum, http-headers, http-title
- Timing: Normal (T3)

**Result**: Discovers Apache 2.4.41 on port 80, identifies admin panel at /admin

### Example 2: Comprehensive Security Audit

**Request**: "Full security audit with vulnerability detection"

**AI Interpretation**:
- Scan Type: vuln
- Ports: All (1-65535)
- Scripts: vuln, vulners
- OS Detection: Enabled
- Timing: Normal (T3)

**Result**: Full port scan, OS detection, vulnerability scripts, risk assessment

### Example 3: Stealth Reconnaissance

**Request**: "Stealthy scan to avoid triggering alarms"

**AI Interpretation**:
- Scan Type: stealth
- Scan Method: SYN stealth (-sS)
- Timing: Paranoid (T1)
- Fragmentation: Enabled

**Result**: Slow, fragmented scan less likely to trigger IDS/IPS

## Database Schema

### Assets Table
- IP address, hostname, status
- OS detection results
- MAC address and vendor
- Risk level classification
- First/last seen timestamps

### Ports Table
- Port number and protocol
- Service name and version
- Banner information
- NSE script results

### Scans Table
- Scan parameters and commands
- Start/end times and duration
- Raw output and AI analysis
- Status tracking

### Notes Table
- User annotations
- Categories (vulnerability, configuration, etc.)
- Timestamps

## Security Considerations

1. **Run with Appropriate Privileges**: Some NMAP scans require root/sudo
2. **Protect API Keys**: Keep OpenAI API key secure in `.env`
3. **Network Authorization**: Only scan authorized networks
4. **Rate Limiting**: Configure scan delays to avoid overwhelming targets
5. **Firewall Rules**: Ensure outbound NMAP traffic is allowed

## Troubleshooting

### NMAP Not Found
```bash
# Verify NMAP installation
which nmap
nmap --version

# Add to PATH if needed
export PATH=$PATH:/usr/local/bin
```

### Permission Errors
```bash
# Some scans require root privileges
sudo python3 backend/app.py
```

### AI Features Not Working
- Verify OpenAI API key in `config/.env`
- Check API key has sufficient credits
- Review logs for error messages

### Database Issues
```bash
# Reset database
rm database/assets.db
python3 backend/app.py  # Will recreate
```

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python3 backend/app.py
```

### Adding Custom NSE Scripts

Edit `backend/nmap_executor.py` and add to `get_common_scripts()`:

```python
'custom': [
    'your-script-1',
    'your-script-2'
]
```

### Extending AI Analysis

Modify `backend/ai_analyzer.py` to customize AI prompts and analysis logic.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Author

**wonkastocks**

- GitHub: [@wonkastocks](https://github.com/wonkastocks)

## Acknowledgments

- Built on top of the powerful [NMAP](https://nmap.org) network scanner
- AI capabilities powered by [OpenAI](https://openai.com)
- Flask web framework
- SQLAlchemy ORM

## Roadmap

- [ ] Multi-target parallel scanning
- [ ] Scheduled/recurring scans
- [ ] Export to PDF/CSV/JSON
- [ ] Integration with vulnerability databases (CVE, NVD)
- [ ] Notification system (email, Slack, Discord)
- [ ] Docker containerization
- [ ] Multi-user support with authentication
- [ ] Advanced filtering and search
- [ ] Custom report templates

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Remember**: Always obtain proper authorization before scanning networks or systems. Unauthorized scanning may be illegal.
