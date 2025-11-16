# Leaked Access Logs Challenge

## 🎯 Challenge Overview
**Objective**: Gain access to any access log file of the server
**Difficulty**: ⭐⭐⭐ (3/6)
**Status**: 📝 **SCRIPT READY** - Needs testing

## 📁 Files in this Directory

### **Scripts:**
- `leaked_logs_solver.py` - Automated log file discovery and enumeration

### **Documentation:**
- `Leaked-Access-Logs-Challenge.md` - Complete challenge writeup with manual solution

## 🔑 Key Concepts

**Vulnerability**: Information disclosure through accessible log files
**Attack Method**: Directory enumeration and path traversal
**Impact**: Sensitive information exposure (IPs, user agents, attack patterns)

## 🚀 Quick Start

```bash
# Run automated solver
python3 leaked_logs_solver.py

# Manual approach:
# 1. Try common log paths: /access.log, /logs/access.log
# 2. Test directory traversal: ../access.log
# 3. Check backup files: access.log.bak, access.log.old
# 4. Look for development logs: debug.log, error.log
```

## 🔍 Common Log Locations

```
Direct paths:
/access.log
/logs/access.log
/var/log/apache2/access.log

Backup files:
/access.log.bak
/access.log.old
/logs.txt

Hidden locations:
/.logs/access.log
/_logs/access.log
/admin/logs
```

---
**Status**: Ready for testing
**Last Updated**: 2025-10-10