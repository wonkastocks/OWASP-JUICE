# Single Page Applications (SPAs) vs Traditional Websites

## What is a Single Page Application (SPA)?

A **Single Page Application (SPA)** is a web application that loads a single HTML page and dynamically updates content as users interact with it, without requiring full page reloads. SPAs use JavaScript frameworks to manipulate the DOM and handle routing client-side, creating a more fluid, app-like user experience.

### Key Characteristics of SPAs:
- **Single HTML Page**: Only one initial HTML document is loaded
- **Client-Side Routing**: Navigation happens via JavaScript without server requests
- **Dynamic Content Updates**: Page sections update without full refresh
- **AJAX/API Calls**: Data fetched asynchronously from backend APIs
- **State Management**: Application state managed in browser memory
- **Fast User Experience**: After initial load, interactions are instant

## Traditional Websites (Multi-Page Applications)

Traditional websites follow a **Multi-Page Application (MPA)** architecture where each page is a separate HTML document served by the server.

### Key Characteristics of Traditional Sites:
- **Multiple HTML Pages**: Each route/URL has its own HTML file
- **Server-Side Routing**: Server handles all navigation requests
- **Full Page Reloads**: Browser refreshes entire page on navigation
- **Synchronous Requests**: User waits for server response
- **Stateless by Default**: Each request is independent
- **SEO-Friendly**: Search engines easily crawl pre-rendered HTML

---

## Popular Examples

### Traditional Multi-Page Websites:
- **Wikipedia** - Server-rendered pages, full reloads on navigation
- **Amazon** (most pages) - Product listings use traditional page loads
- **WordPress sites** - Default WordPress uses server-side rendering
- **Craigslist** - Classic HTML pages with full refreshes
- **Government websites** - Usually traditional for accessibility/compatibility
- **News sites** (many) - BBC News, NY Times articles often use traditional architecture

### Popular Single Page Applications:
- **Gmail** - Entire email interface in one app
- **Facebook** - News feed updates without page reloads
- **Twitter/X** - Infinite scroll and dynamic updates
- **Netflix** - Browse and watch without leaving the app
- **Trello** - Drag-and-drop board interface
- **Spotify Web Player** - Music streaming interface
- **Google Maps** - Pan, zoom, search without reloading
- **Slack** - Real-time messaging interface
- **Airbnb** - Search and booking flow
- **Juice Shop** (https://juice3.wonkatech.org) - OWASP's intentionally vulnerable web app built with Angular

---

## Technical Differences

| Aspect | Traditional Website | Single Page Application |
|--------|-------------------|------------------------|
| **Initial Load** | Fast (smaller HTML) | Slower (large JS bundle) |
| **Navigation** | Full page reload | Instant (no reload) |
| **SEO** | Excellent (native) | Challenging (requires SSR/pre-rendering) |
| **Browser History** | Native support | Requires History API |
| **Offline Support** | None | Possible with service workers |
| **Development Complexity** | Lower | Higher |
| **Server Load** | Higher (each navigation) | Lower (API calls only) |
| **User Experience** | Slower, more traditional | Faster, app-like |

---

## How to Identify an SPA Using Chrome DevTools

### Method 1: Network Tab Analysis

1. **Open Chrome DevTools**: `F12` or `Right-click → Inspect`
2. **Go to Network Tab**: Click on "Network" panel
3. **Enable "Preserve log"**: Check the box to keep requests across navigation
4. **Clear network log**: Click the 🚫 icon
5. **Navigate through the site**: Click different links/sections

**What to look for:**
- **SPA**: Only AJAX/XHR/Fetch requests appear after initial load
- **Traditional**: Full `document` type requests (HTML pages) on each navigation

**Example with Juice Shop:**
```
Initial Load:
  ✓ index.html (document) - 200 OK
  ✓ main.js (javascript) - 200 OK (large bundle)
  ✓ vendor.js (javascript) - 200 OK

After clicking "Login":
  ✓ /rest/user/login (xhr) - 200 OK (JSON response)
  ✗ NO new index.html request! ← This confirms SPA
```

### Method 2: URL and Browser Behavior

1. **Watch the URL bar** while navigating
2. **Look for hash (#) routing** or **clean URLs without page reloads**

**SPA Patterns:**
```
https://juice3.wonkatech.org/#/login
https://juice3.wonkatech.org/#/search
https://juice3.wonkatech.org/#/basket
```
Notice the `#` (hash) - this is client-side routing!

Modern SPAs may use HTML5 History API without hashes:
```
https://gmail.com/mail/u/0/#inbox  (hash-based)
https://netflix.com/browse/genre/  (History API)
```

**Traditional Pattern:**
```
https://wikipedia.org/wiki/Article_1
https://wikipedia.org/wiki/Article_2
(Full page reload, different HTML documents)
```

### Method 3: Console Inspection

Open **Console** tab and type:

```javascript
// Check for SPA frameworks
window.ng !== undefined      // Angular (like Juice Shop)
window.React !== undefined   // React
window.Vue !== undefined     // Vue.js
window.__NEXT_DATA__        // Next.js

// Check routing mechanism
console.log(window.location.hash);  // Hash-based routing?
console.log(history.length);        // Many entries = SPA likely

// Monitor navigation events
window.addEventListener('popstate', (e) => {
  console.log('SPA navigation detected!', e);
});
```

**For Juice Shop specifically:**
```javascript
// Juice Shop uses Angular
console.log(window.ng);  // Should show Angular framework object

// Check for Angular router
console.log(document.querySelector('app-root'));  // Angular root component
```

### Method 4: Sources Tab - Application Structure

1. **Go to Sources Tab**
2. **Expand the domain folder**

**SPA Structure (like Juice Shop):**
```
juice3.wonkatech.org/
  ├── index.html (single file)
  ├── main.js (application code - LARGE)
  ├── vendor.js (framework code)
  ├── runtime.js
  └── assets/ (images, styles)
```

**Traditional Structure:**
```
example.com/
  ├── index.html
  ├── about.html
  ├── contact.html
  ├── products.html
  ├── small-scripts.js
  └── style.css
```

### Method 5: Elements Tab - DOM Observation

1. **Go to Elements Tab**
2. **Click around the site**
3. **Watch the DOM tree**

**SPA Behavior:**
- DOM elements change dynamically
- No full HTML replacement
- Single root element (e.g., `<app-root>`, `<div id="root">`)

**Traditional Behavior:**
- Entire `<html>` structure reloads
- Console clears on navigation

---

## Discovering Application Paths in an SPA

### Finding Routes/Endpoints

**Method 1: Network Tab Filtering**
1. Open Network tab
2. Filter by `Fetch/XHR` or `JS`
3. Click around the application
4. Look at API endpoints being called

**Juice Shop Example:**
```
GET /rest/products/search
GET /rest/basket/{id}
POST /rest/user/login
GET /rest/admin/application-version
```

**Method 2: JavaScript Bundle Analysis**
1. Go to **Sources** tab
2. Find `main.js` or bundle files
3. Search (`Ctrl+F`) for keywords:
   - `"route"`, `"path"`, `"api"`
   - `"/admin"`, `"/api/"`, `"/rest/"`

**Method 3: Router Configuration**
```javascript
// In Console, for Angular apps like Juice Shop:
getAllAngularRootElements()[0].injector.get('Router').config
```

**Method 4: Application Tab**
1. Go to **Application** tab
2. Check **Local Storage** and **Session Storage**
   - May contain route info, tokens, user data
3. Check **Service Workers** (if offline-capable SPA)

---

## Practical Example: Analyzing Juice Shop

### Step-by-Step Analysis:

**1. Confirm it's an SPA:**
```bash
# Open https://juice3.wonkatech.org/#/
# Notice the '#' in URL - hash-based routing
```

**2. Network Analysis:**
```
DevTools → Network → Click "Login"
Result: Only XHR request to /rest/user/login (no HTML reload)
```

**3. Framework Detection:**
```javascript
// Console
console.log(window.ng);
// Output: {probe: ƒ, coreTokens: {…}} ← Angular detected!
```

**4. Find API Endpoints:**
```
Network Tab filtered by XHR:
- /rest/products/search
- /rest/basket/
- /rest/user/whoami
- /rest/admin/application-configuration
```

**5. Discover Hidden Routes:**
```javascript
// Search in main.js for "path:"
{path: 'administration', component: AdministrationComponent}
{path: 'score-board', component: ScoreBoardComponent}
{path: 'about', component: AboutComponent}
```

---

## Security Implications for SPAs

### Why This Matters for Security Testing:

1. **Client-Side Code Exposure**: All routes/logic visible in JavaScript bundles
2. **API Discovery**: Network tab reveals all backend endpoints
3. **Hidden Routes**: Developers may forget to secure admin routes
4. **Token Storage**: Often stored in localStorage (vulnerable to XSS)
5. **CORS Misconfigurations**: SPAs require CORS, often misconfigured

### Testing SPAs vs Traditional Sites:

**Traditional Sites:**
- Test each URL individually
- Focus on server-side validation
- Session management via cookies

**SPAs:**
- Test API endpoints directly
- Bypass client-side validation (it's in JS!)
- Check for insecure token storage
- Look for unprotected routes in bundle code
- Test WebSocket connections (if used)

---

## Summary

**SPAs like Juice Shop:**
- Load once, update dynamically
- Use JavaScript frameworks (Angular, React, Vue)
- Route with `#` or History API
- Communicate via REST APIs
- Visible in Chrome DevTools through bundle analysis

**Traditional sites:**
- Load new HTML on each navigation
- Rely on server-side rendering
- Use standard links and forms
- Easier to test with traditional tools

**Detection Tools:**
- Network tab (look for XHR-only navigation)
- URL patterns (hash-based or History API)
- Console framework checks (`window.ng`, `window.React`)
- DOM observation (dynamic updates)

---

## Resources

- [MDN: Single Page Applications](https://developer.mozilla.org/en-US/docs/Glossary/SPA)
- [Chrome DevTools Documentation](https://developer.chrome.com/docs/devtools/)
- [OWASP Juice Shop (Example SPA)](https://owasp.org/www-project-juice-shop/)