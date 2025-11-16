# Unsigned JWT Challenge

## 🎯 Challenge Overview
**Objective**: Forge an essentially unsigned JSON Web Token that impersonates the (non-existing) user jwtn3d@juice-sh.op
**Difficulty**: ⭐⭐⭐⭐⭐ (5/6)
**Status**: 📝 **SCRIPT READY** - Needs testing

## 📁 Files in this Directory

### **Scripts:**
- `unsigned_jwt_solver.py` - JWT manipulation and algorithm confusion attacks

### **Documentation:**
- `Unsigned-JWT-Challenge.md` - Complete challenge writeup with manual solution

## 🔑 Key Concepts

**Vulnerability**: JWT algorithm confusion (accepting "alg": "none")
**Attack Method**: Modify JWT header to remove signature requirement
**Impact**: Complete authentication bypass and privilege escalation

## 🚀 Quick Start

```bash
# Run automated solver
python3 unsigned_jwt_solver.py

# Manual approach:
# 1. Get any valid JWT token
# 2. Modify header: {"alg":"none","typ":"JWT"}
# 3. Modify payload: {"email":"jwtn3d@juice-sh.op","role":"admin"}
# 4. Remove signature (end with just a dot: header.payload.)
```

---
**Status**: Ready for testing
**Last Updated**: 2025-10-10