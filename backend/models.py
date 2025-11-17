"""
Database models for NMAP Optimizer
Stores assets, scan results, notes, and host information
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class Asset(db.Model):
    """Stores discovered assets/hosts"""
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), unique=True, nullable=False)  # IPv4/IPv6
    hostname = db.Column(db.String(255))
    status = db.Column(db.String(20), default='unknown')  # up, down, filtered
    os_guess = db.Column(db.String(255))
    os_accuracy = db.Column(db.Integer)
    mac_address = db.Column(db.String(17))
    vendor = db.Column(db.String(255))
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    risk_level = db.Column(db.String(20), default='unknown')  # low, medium, high, critical

    # Relationships
    scans = db.relationship('Scan', back_populates='asset', cascade='all, delete-orphan')
    ports = db.relationship('Port', back_populates='asset', cascade='all, delete-orphan')
    notes = db.relationship('Note', back_populates='asset', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'hostname': self.hostname,
            'status': self.status,
            'os_guess': self.os_guess,
            'os_accuracy': self.os_accuracy,
            'mac_address': self.mac_address,
            'vendor': self.vendor,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'risk_level': self.risk_level,
            'open_ports': len([p for p in self.ports if p.state == 'open']),
            'total_scans': len(self.scans)
        }


class Scan(db.Model):
    """Stores individual scan results"""
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    scan_type = db.Column(db.String(50), nullable=False)  # quick, full, stealth, custom
    scan_command = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # seconds
    status = db.Column(db.String(20), default='running')  # running, completed, failed
    raw_output = db.Column(db.Text)
    xml_output = db.Column(db.Text)
    ai_analysis = db.Column(db.Text)  # AI interpretation of results
    user_request = db.Column(db.Text)  # Original user request

    # Relationships
    asset = db.relationship('Asset', back_populates='scans')

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'scan_type': self.scan_type,
            'scan_command': self.scan_command,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration': self.duration,
            'status': self.status,
            'ai_analysis': self.ai_analysis,
            'user_request': self.user_request
        }


class Port(db.Model):
    """Stores discovered ports and services"""
    __tablename__ = 'ports'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    port_number = db.Column(db.Integer, nullable=False)
    protocol = db.Column(db.String(10), default='tcp')
    state = db.Column(db.String(20))  # open, closed, filtered
    service = db.Column(db.String(100))
    version = db.Column(db.String(255))
    banner = db.Column(db.Text)
    product = db.Column(db.String(255))
    extra_info = db.Column(db.Text)
    script_results = db.Column(db.Text)  # JSON string of NSE script results
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    asset = db.relationship('Asset', back_populates='ports')

    def to_dict(self):
        return {
            'id': self.id,
            'port_number': self.port_number,
            'protocol': self.protocol,
            'state': self.state,
            'service': self.service,
            'version': self.version,
            'banner': self.banner,
            'product': self.product,
            'extra_info': self.extra_info,
            'script_results': json.loads(self.script_results) if self.script_results else {},
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }


class Note(db.Model):
    """User notes about assets"""
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    title = db.Column(db.String(255))
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # vulnerability, configuration, credentials, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    asset = db.relationship('Asset', back_populates='notes')

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class DNSRecord(db.Model):
    """DNS resolution records"""
    __tablename__ = 'dns_records'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    record_type = db.Column(db.String(10))  # A, AAAA, MX, TXT, etc.
    value = db.Column(db.String(255))
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'record_type': self.record_type,
            'value': self.value,
            'discovered_at': self.discovered_at.isoformat() if self.discovered_at else None
        }
