"""
NMAP Optimizer - Flask Backend API
Main application with RESTful endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Asset, Scan, Port, Note, DNSRecord
from nmap_executor import NmapExecutor
from ai_analyzer import AIAnalyzer
import fingerprinting
import os
from datetime import datetime
import threading

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/assets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize database
db.init_app(app)

# Initialize components
nmap_executor = NmapExecutor(output_dir='../scans')
ai_analyzer = AIAnalyzer()

# Create tables
with app.app_context():
    db.create_all()


# ==================== FRONTEND ROUTES ====================

@app.route('/')
def index():
    """Serve frontend"""
    return send_from_directory('../frontend', 'index.html')


# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'ai_enabled': bool(ai_analyzer.api_key)
    })


@app.route('/api/scan/request', methods=['POST'])
def scan_request():
    """
    Handle natural language scan request

    Body: {
        "target": "192.168.1.1",
        "request": "do a quick scan looking for web vulnerabilities"
    }
    """
    data = request.json
    target = data.get('target')
    user_request = data.get('request', 'quick scan')

    if not target:
        return jsonify({'error': 'Target is required'}), 400

    # Validate target format
    if not fingerprinting.validate_target(target):
        return jsonify({'error': 'Invalid target format'}), 400

    # Use AI to interpret request
    scan_params = ai_analyzer.interpret_scan_request(user_request, target)

    # Create or update asset
    asset = Asset.query.filter_by(ip_address=target).first()
    if not asset:
        asset = Asset(ip_address=target, status='scanning')
        db.session.add(asset)
        db.session.commit()

    # Create scan record
    scan = Scan(
        asset_id=asset.id,
        scan_type=scan_params.get('scan_type', 'custom'),
        user_request=user_request,
        status='queued'
    )
    db.session.add(scan)
    db.session.commit()

    # Execute scan in background thread
    thread = threading.Thread(
        target=execute_scan_background,
        args=(scan.id, target, scan_params)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        'message': 'Scan queued successfully',
        'scan_id': scan.id,
        'asset_id': asset.id,
        'scan_params': scan_params
    }), 202


def execute_scan_background(scan_id, target, scan_params):
    """Execute scan in background thread"""
    with app.app_context():
        scan = Scan.query.get(scan_id)
        if not scan:
            return

        # Update status
        scan.status = 'running'
        scan.started_at = datetime.utcnow()
        db.session.commit()

        try:
            # Execute NMAP scan
            results = nmap_executor.execute_scan(target, scan_params)

            # Store scan command and outputs
            scan.scan_command = results.get('command')
            scan.raw_output = results.get('raw_output', '')
            scan.completed_at = datetime.utcnow()
            scan.duration = int(results.get('duration', 0))

            if results.get('status') == 'completed':
                # Parse and store results
                if 'parsed_data' in results:
                    process_scan_results(scan.asset_id, results['parsed_data'])

                # AI analysis
                analysis = ai_analyzer.analyze_scan_results(results)
                scan.ai_analysis = str(analysis)

                # Update asset
                asset = Asset.query.get(scan.asset_id)
                asset.status = 'up' if results.get('parsed_data', {}).get('hosts') else 'down'
                asset.last_seen = datetime.utcnow()

                # Update OS info if available
                if 'parsed_data' in results and results['parsed_data'].get('hosts'):
                    host = results['parsed_data']['hosts'][0]
                    if 'os' in host and host['os']:
                        asset.os_guess = host['os'].get('name', '')
                        asset.os_accuracy = int(host['os'].get('accuracy', 0))

                    # Update MAC and vendor
                    if 'addresses' in host:
                        asset.mac_address = host['addresses'].get('mac', '')
                        asset.vendor = host.get('mac_vendor', '')

                # Set risk level based on AI analysis
                if isinstance(analysis, dict):
                    asset.risk_level = analysis.get('risk_level', 'unknown')

                scan.status = 'completed'
            else:
                scan.status = 'failed'

            db.session.commit()

        except Exception as e:
            scan.status = 'error'
            scan.raw_output = f"Error: {str(e)}"
            scan.completed_at = datetime.utcnow()
            db.session.commit()


def process_scan_results(asset_id, parsed_data):
    """Process and store parsed scan results"""
    if not parsed_data.get('hosts'):
        return

    host = parsed_data['hosts'][0]

    # Store/update ports
    for port_data in host.get('ports', []):
        port_num = port_data.get('port')
        if not port_num:
            continue

        # Check if port already exists
        port = Port.query.filter_by(
            asset_id=asset_id,
            port_number=port_num,
            protocol=port_data.get('protocol', 'tcp')
        ).first()

        if not port:
            port = Port(
                asset_id=asset_id,
                port_number=port_num,
                protocol=port_data.get('protocol', 'tcp')
            )
            db.session.add(port)

        # Update port info
        port.state = port_data.get('state', 'unknown')
        port.last_seen = datetime.utcnow()

        service = port_data.get('service', {})
        if service:
            port.service = service.get('name', '')
            port.product = service.get('product', '')
            port.version = service.get('version', '')
            port.extra_info = service.get('extrainfo', '')

            # Combine product and version for banner
            banner_parts = [service.get('product', ''), service.get('version', '')]
            port.banner = ' '.join(filter(None, banner_parts))

        # Store script results
        if port_data.get('scripts'):
            import json
            port.script_results = json.dumps(port_data['scripts'])

    db.session.commit()


@app.route('/api/scan/<int:scan_id>', methods=['GET'])
def get_scan(scan_id):
    """Get scan details and results"""
    scan = Scan.query.get(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404

    scan_data = scan.to_dict()

    # Add AI analysis if available
    if scan.ai_analysis:
        try:
            import ast
            scan_data['ai_analysis'] = ast.literal_eval(scan.ai_analysis)
        except:
            scan_data['ai_analysis'] = scan.ai_analysis

    return jsonify(scan_data)


@app.route('/api/assets', methods=['GET'])
def get_assets():
    """Get all assets"""
    assets = Asset.query.all()
    return jsonify([asset.to_dict() for asset in assets])


@app.route('/api/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Get asset details with ports and scans"""
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404

    asset_data = asset.to_dict()
    asset_data['ports'] = [port.to_dict() for port in asset.ports]
    asset_data['scans'] = [scan.to_dict() for scan in asset.scans]
    asset_data['notes'] = [note.to_dict() for note in asset.notes]

    return jsonify(asset_data)


@app.route('/api/assets/<int:asset_id>/notes', methods=['POST'])
def add_note(asset_id):
    """Add note to asset"""
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'error': 'Asset not found'}), 404

    data = request.json
    note = Note(
        asset_id=asset_id,
        title=data.get('title', 'Note'),
        content=data.get('content', ''),
        category=data.get('category', 'general')
    )
    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


@app.route('/api/assets/<int:asset_id>/notes/<int:note_id>', methods=['PUT', 'DELETE'])
def manage_note(asset_id, note_id):
    """Update or delete note"""
    note = Note.query.get(note_id)
    if not note or note.asset_id != asset_id:
        return jsonify({'error': 'Note not found'}), 404

    if request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted'}), 200

    # Update note
    data = request.json
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    if 'category' in data:
        note.category = data['category']

    db.session.commit()
    return jsonify(note.to_dict())


@app.route('/api/fingerprint/dns', methods=['POST'])
def fingerprint_dns():
    """Perform DNS enumeration"""
    data = request.json
    target = data.get('target')

    if not target:
        return jsonify({'error': 'Target required'}), 400

    results = fingerprinting.dns_enumeration(target)
    return jsonify(results)


@app.route('/api/fingerprint/banner', methods=['POST'])
def fingerprint_banner():
    """Grab banner from specific port"""
    data = request.json
    target = data.get('target')
    port = data.get('port', 80)

    if not target:
        return jsonify({'error': 'Target required'}), 400

    result = nmap_executor.banner_grab(target, int(port))
    return jsonify(result)


@app.route('/api/fingerprint/os', methods=['POST'])
def fingerprint_os():
    """Perform OS fingerprinting"""
    data = request.json
    target = data.get('target')

    if not target:
        return jsonify({'error': 'Target required'}), 400

    # Queue OS detection scan
    scan_params = {
        'scan_type': 'os',
        'ports': 'default',
        'timing': 3,
        'scripts': [],
        'additional_flags': ''
    }

    results = nmap_executor.execute_scan(target, scan_params)
    return jsonify(results)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    total_assets = Asset.query.count()
    total_scans = Scan.query.count()
    assets_up = Asset.query.filter_by(status='up').count()
    recent_scans = Scan.query.order_by(Scan.started_at.desc()).limit(10).all()

    # Risk distribution
    risk_counts = {
        'critical': Asset.query.filter_by(risk_level='critical').count(),
        'high': Asset.query.filter_by(risk_level='high').count(),
        'medium': Asset.query.filter_by(risk_level='medium').count(),
        'low': Asset.query.filter_by(risk_level='low').count(),
        'unknown': Asset.query.filter_by(risk_level='unknown').count()
    }

    return jsonify({
        'total_assets': total_assets,
        'total_scans': total_scans,
        'assets_up': assets_up,
        'assets_down': total_assets - assets_up,
        'risk_distribution': risk_counts,
        'recent_scans': [scan.to_dict() for scan in recent_scans]
    })


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('../database', exist_ok=True)
    os.makedirs('../scans', exist_ok=True)
    os.makedirs('../logs', exist_ok=True)

    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║         NMAP OPTIMIZER - AI-Powered Scanner          ║
    ║                                                       ║
    ║  Web Interface: http://localhost:5000                ║
    ║  API Docs: http://localhost:5000/api/health          ║
    ║                                                       ║
    ║  ⚠️  AUTHORIZED USE ONLY - Security Testing Tool    ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
