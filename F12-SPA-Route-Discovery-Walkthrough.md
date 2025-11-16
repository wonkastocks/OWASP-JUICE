# F12 DevTools: SPA Route Discovery Walkthrough

## Complete Guide to Discovering SPA Routes for Airbnb & Juice Shop

This hands-on walkthrough teaches you how to use Chrome F12 Developer Tools to map out Single Page Application routes and API endpoints.

---

## Prerequisites

- **Chrome Browser** (or Chromium-based browser)
- **Internet connection** for Airbnb
- **Access to Juice Shop**: https://juice3.wonkatech.org/#/

---

# Part 1: Juice Shop Route Discovery

Juice Shop is an intentionally vulnerable web application built with Angular, making it perfect for learning SPA route discovery.

## Step 1: Initial Setup

1. **Open Juice Shop**: Navigate to `https://juice3.wonkatech.org/#/`
2. **Open DevTools**: Press `F12` (or `Ctrl+Shift+I` on Windows, `Cmd+Option+I` on Mac)
3. **Dock DevTools**: Click the `⋮` menu in DevTools → Dock side → Choose "Dock to bottom" or "Dock to right"

Your screen should now show the Juice Shop website on one side and DevTools on the other.

## Step 2: Network Tab - Basic Route Discovery

### Configure Network Tab

1. Click the **Network** tab in DevTools
2. Enable **Preserve log** (checkbox at top) - keeps requests across navigation
3. **Clear** the network log (🚫 icon)
4. **Disable cache** (checkbox) - ensures fresh requests

### Initial Page Load Analysis

1. **Refresh the page** (`Ctrl+R` or `Cmd+R`)
2. **Observe the waterfall** of requests

**What you'll see:**
```
Name                Type        Status  Size
────────────────────────────────────────────
index.html         document    200     2.3 KB
runtime.js         script      200     3.2 KB
polyfills.js       script      200     89 KB
main.js            script      200     2.1 MB  ← Angular app bundle
vendor.js          script      200     1.8 MB  ← Framework code
styles.css         stylesheet  200     45 KB
```

**Key Observation**: Notice the large `main.js` file - this contains all the application code and routes!

### Filter by XHR/Fetch (API Calls)

1. Click the **XHR** filter button (or **Fetch/XHR**)
2. **Clear** the log again
3. **Click around** Juice Shop:
   - Click "Account" → "Login"
   - Click "Search" icon
   - Click on a product

**What you'll see:**
```
Name                                Method  Status  Type
─────────────────────────────────────────────────────────
rest/products/search?q=             GET     200     xhr
rest/basket/1                       GET     200     xhr
rest/user/whoami                    GET     200     xhr
```

**Discovery #1**: The API base path is `/rest/`

### Detailed Request Inspection

1. **Click on** `rest/products/search?q=`
2. **Tabs appear**: Headers, Preview, Response, Initiator, Timing

**Headers Tab:**
```
Request URL: https://juice3.wonkatech.org/rest/products/search?q=
Request Method: GET
Status Code: 200 OK
```

**Preview Tab:**
Shows JSON response:
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Apple Juice",
      "description": "Fresh squeezed...",
      "price": 1.99
    }
  ]
}
```

**Response Tab:**
Raw JSON response data

**Initiator Tab:**
Shows which JavaScript file made this request (helps trace code flow)

## Step 3: Console - Framework Detection

1. Click the **Console** tab
2. Type the following commands:

### Detect Angular Framework

```javascript
// Check if Angular is present
console.log(window.ng);
```

**Expected Output:**
```
{probe: ƒ, coreTokens: {…}, ɵsetProfiler: ƒ, ...}
```

**✅ Confirmation**: Juice Shop uses Angular!

### Find Angular Root Component

```javascript
// Get the main Angular component
document.querySelector('app-root');
```

**Expected Output:**
```html
<app-root ng-version="...">...</app-root>
```

### Check Router Configuration

```javascript
// Access Angular router (may not work in production builds)
try {
  const rootElement = document.querySelector('app-root');
  console.log('Angular app detected:', rootElement);
} catch(e) {
  console.log('Cannot access router directly');
}
```

### Check for Hash-Based Routing

```javascript
// Current route
console.log('Current hash:', window.location.hash);

// Monitor route changes
let lastHash = window.location.hash;
setInterval(() => {
  if (window.location.hash !== lastHash) {
    console.log('Route changed from', lastHash, 'to', window.location.hash);
    lastHash = window.location.hash;
  }
}, 500);
```

**Now click around** and watch the console log route changes!

## Step 4: Sources Tab - JavaScript Bundle Analysis

This is where we find hidden routes not visible in the UI!

### Navigate to Sources

1. Click **Sources** tab
2. Expand the domain tree: `juice3.wonkatech.org` → `(index)`
3. Find `main.js` (the large application bundle)

### Search for Routes

1. With `main.js` open, press `Ctrl+F` (or `Cmd+F`)
2. **Search for**: `path:`

**You'll find Angular route definitions:**
```javascript
{path: 'administration', component: AdministrationComponent}
{path: 'login', component: LoginComponent}
{path: 'register', component: RegisterComponent}
{path: 'basket', component: BasketComponent}
{path: 'score-board', component: ScoreBoardComponent}  // Hidden!
{path: 'about', component: AboutComponent}
{path: 'contact', component: ContactComponent}
{path: 'photo-wall', component: PhotoWallComponent}
{path: 'complain', component: ComplainComponent}
{path: 'chatbot', component: ChatbotComponent}
{path: '2fa/enter', component: TwoFactorAuthEnterComponent}
{path: 'address/select', component: AddressSelectComponent}
{path: 'address/saved', component: SavedAddressComponent}
{path: 'address/create', component: AddressCreateComponent}
{path: 'address/edit/:addressId', component: AddressEditComponent}
{path: 'delivery-method', component: DeliveryMethodComponent}
{path: 'deluxe-membership', component: DeluxeUserComponent}
{path: 'saved-payment-methods', component: SavedPaymentMethodsComponent}
{path: 'order-completion/:id', component: OrderCompletionComponent}
{path: 'order-summary', component: OrderSummaryComponent}
{path: 'order-history', component: PurchaseBasketComponent}
{path: 'payment/:entity', component: PaymentComponent}
{path: 'wallet', component: WalletComponent}
{path: 'privacy-security', component: PrivacySecurityComponent}
{path: 'privacy-security/change-password', component: ChangePasswordComponent}
{path: 'privacy-security/two-factor-authentication', component: TwoFactorAuthComponent}
{path: 'privacy-security/data-export', component: DataExportComponent}
{path: 'privacy-security/last-login-ip', component: LastLoginIpComponent}
{path: 'search', component: SearchResultComponent}
{path: 'hacking-instructor', component: SearchResultComponent}
```

### Search for API Endpoints

**Search for**: `/rest/`

**You'll find API endpoint strings:**
```javascript
"/rest/user/login"
"/rest/user/register"
"/rest/products/search"
"/rest/basket/"
"/rest/basket/:id"
"/rest/admin/application-configuration"
"/rest/admin/application-version"
"/rest/products/:id/reviews"
"/rest/captcha/"
"/rest/image/captcha/:id"
"/rest/track-order/:id"
"/rest/continue-code/apply/:continueCode"
"/rest/memories"
"/rest/saveLoginIp"
"/rest/user/data-export"
"/rest/user/whoami"
"/rest/deluxe-membership"
"/rest/2fa/status"
"/rest/2fa/setup"
"/rest/2fa/verify"
```

### Advanced: Search for Hidden Admin Routes

**Search for**: `admin`

**You might find:**
```javascript
{path: 'administration', component: AdministrationComponent, canActivate: [AdminGuard]}
"/rest/admin/application-configuration"
"/rest/admin/application-version"
```

**Discovery #2**: There's an admin panel at `/#/administration`!

**Try it**: Navigate to `https://juice3.wonkatech.org/#/administration`

(You'll need admin credentials, but you've discovered a hidden route!)

## Step 5: Application Tab - Storage Investigation

1. Click **Application** tab
2. Expand **Local Storage** → `https://juice3.wonkatech.org`

**You'll see stored data:**
```
token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
bid: 1
email: user@juice-sh.op
```

**Security Note**: The JWT token is stored in localStorage (vulnerable to XSS attacks)!

### Session Storage

1. Expand **Session Storage**
2. Look for temporary session data

### Cookies

1. Click **Cookies** → `https://juice3.wonkatech.org`
2. Check for authentication cookies

## Step 6: Network Tab - Advanced Filtering

### Filter by Domain

1. In Network tab, type in filter: `juice3.wonkatech.org`
2. Shows only requests to this domain

### Filter by Status Code

```
status-code:200    # Successful requests
status-code:404    # Not found
status-code:401    # Unauthorized
status-code:500    # Server errors
```

### Filter by Method

```
method:POST    # Only POST requests
method:GET     # Only GET requests
```

### Export HAR File (HTTP Archive)

1. Right-click in Network tab
2. **Save all as HAR with content**
3. Opens JSON file with all requests/responses

**Use case**: Analyze offline, share with team, import into other tools

## Step 7: Complete Route Map for Juice Shop

### Frontend Routes (Hash-based)

```
Base URL: https://juice3.wonkatech.org/#/

Public Routes:
├── /                          # Home/Products
├── /login                     # Login page
├── /register                  # Registration
├── /search                    # Search results
├── /basket                    # Shopping cart
├── /contact                   # Contact form
├── /about                     # About page
├── /photo-wall                # Photo gallery
├── /complain                  # Complaint form
├── /chatbot                   # AI chatbot
└── /track-order               # Order tracking

Protected Routes (require auth):
├── /order-history             # Past orders
├── /wallet                    # Digital wallet
├── /saved-payment-methods     # Payment cards
├── /address/saved             # Saved addresses
├── /address/create            # Add new address
├── /address/edit/:id          # Edit address
├── /privacy-security          # Privacy settings
├── /privacy-security/change-password
├── /privacy-security/two-factor-authentication
├── /privacy-security/data-export
├── /privacy-security/last-login-ip
├── /deluxe-membership         # Premium subscription
├── /2fa/enter                 # 2FA verification
├── /delivery-method           # Shipping options
├── /payment/:entity           # Payment page
├── /order-summary             # Order review
└── /order-completion/:id      # Order confirmation

Admin Routes (require admin role):
├── /administration            # Admin panel
└── /score-board               # Challenge tracker (hidden!)

Special Routes:
└── /hacking-instructor        # Tutorial system
```

### API Endpoints

```
Base URL: https://juice3.wonkatech.org/rest/

Authentication:
├── POST /user/login           # Login
├── POST /user/register        # Registration
├── GET  /user/whoami          # Get current user
└── GET  /user/authentication-details

Products:
├── GET  /products/search      # Search products
├── GET  /products/:id         # Get product details
├── GET  /products/:id/reviews # Get reviews
└── POST /products/:id/reviews # Add review

Basket/Cart:
├── GET    /basket/:id         # Get basket
├── POST   /basket/:id/checkout # Checkout
├── PUT    /basket/:id         # Update basket
└── DELETE /basket/:id         # Clear basket

Orders:
├── GET  /order-history        # Get past orders
├── GET  /track-order/:id      # Track order
└── POST /continue-code/apply/:continueCode

User Management:
├── GET  /user/data-export     # Export user data
├── GET  /saveLoginIp          # Log IP address
├── GET  /privacy-security/change-password
├── GET  /2fa/status           # 2FA status
├── POST /2fa/setup            # Enable 2FA
└── POST /2fa/verify           # Verify 2FA code

Payment:
├── GET  /wallet               # Get wallet balance
├── GET  /saved-payment-methods
├── GET  /deluxe-membership    # Premium status
└── POST /payment              # Process payment

Admin:
├── GET  /admin/application-configuration
├── GET  /admin/application-version
└── GET  /administration       # Admin data

Misc:
├── GET  /captcha              # Generate CAPTCHA
├── GET  /image/captcha/:id    # CAPTCHA image
├── GET  /memories             # Photo wall
└── POST /feedback             # Submit feedback
```

---

# Part 2: Airbnb Route Discovery

Airbnb is a production React-based SPA with more sophisticated obfuscation and optimization.

## Step 1: Initial Setup

1. **Open Airbnb**: Navigate to `https://www.airbnb.com/`
2. **Open DevTools**: Press `F12`
3. **Dock DevTools**: Bottom or right side

## Step 2: Network Tab - Initial Analysis

### Configure and Load

1. **Network** tab
2. Enable **Preserve log**
3. **Disable cache**
4. **Refresh page** (`Ctrl+R` or `Cmd+R`)

### Initial Load Waterfall

**What you'll see (simplified):**
```
Name                              Type        Status  Size
──────────────────────────────────────────────────────────
www.airbnb.com                    document    200     ~50 KB
common-[hash].js                  script      200     ~800 KB
vendors-[hash].js                 script      200     ~1.2 MB
core-guest-[hash].js              script      200     ~1.5 MB
dls-[hash].css                    stylesheet  200     ~200 KB
```

**Key Observation**: Multiple JavaScript bundles with hashed names (cache-busting strategy)

### Filter by XHR/Fetch

1. Click **XHR** or **Fetch/XHR** filter
2. **Clear** the log
3. **Interact with the site**:
   - Type a destination in search
   - Click "Search"
   - Click on a listing
   - Change dates

**What you'll see:**
```
Name                                    Method  Status  Type
───────────────────────────────────────────────────────────────
/api/v3/StaysSearch                     POST    200     fetch
/api/v3/StaysPdpSections                POST    200     fetch
/api/v3/HomesDetailsCardView            POST    200     fetch
/api/v2/pdp_listing_details/:id         GET     200     xhr
/api/v2/explore_tabs                    GET     200     xhr
```

**Discovery #1**: Airbnb uses `/api/v3/` and `/api/v2/` as API base paths

### Detailed Request Inspection - Search Example

1. **Type** "Tokyo" in search bar
2. **Click on** the `StaysSearch` request in Network tab

**Headers Tab:**
```
Request URL: https://www.airbnb.com/api/v3/StaysSearch
Request Method: POST
Status Code: 200
```

**Payload Tab (Request body):**
```json
{
  "operationName": "StaysSearch",
  "variables": {
    "request": {
      "query": "Tokyo",
      "searchType": "UNKNOWN_SEARCH_TYPE",
      "checkin": "2025-02-01",
      "checkout": "2025-02-05",
      "adults": 2,
      "children": 0,
      "infants": 0,
      "pets": 0
    }
  },
  "extensions": {}
}
```

**Preview Tab (Response):**
```json
{
  "data": {
    "presentation": {
      "staysSearch": {
        "results": [
          {
            "listing": {
              "id": "12345678",
              "name": "Cozy Tokyo Apartment",
              "city": "Tokyo",
              "avgRating": 4.89,
              "pricing": {
                "price": "$85",
                "total": "$425"
              }
            }
          }
        ]
      }
    }
  }
}
```

**Discovery #2**: Airbnb uses GraphQL-like API structure with `operationName` and `variables`

## Step 3: Console - Framework Detection

1. Click **Console** tab

### Detect React Framework

```javascript
// Check for React
console.log(typeof React);
```

**If output is "undefined"**, React is bundled privately (common in production)

**Alternative detection:**
```javascript
// Check for React fiber (internal structure)
const rootElement = document.getElementById('root') || document.querySelector('[data-reactroot]');
console.log('React root element:', rootElement);

// Check for React DevTools
console.log('React DevTools:', window.__REACT_DEVTOOLS_GLOBAL_HOOK__);
```

**Expected Output:**
```
React root element: <div id="root">...</div>
React DevTools: {inject: ƒ, ...}
```

**✅ Confirmation**: Airbnb uses React!

### Check URL Routing

```javascript
// Airbnb uses HTML5 History API (no hash)
console.log('Current path:', window.location.pathname);

// Monitor route changes
let lastPath = window.location.pathname;
setInterval(() => {
  if (window.location.pathname !== lastPath) {
    console.log('Route changed from', lastPath, 'to', window.location.pathname);
    lastPath = window.location.pathname;
  }
}, 500);
```

**Now navigate** around Airbnb and watch route changes!

### Inspect Redux State (if accessible)

```javascript
// Try to access Redux store
console.log(window.__REDUX_DEVTOOLS_EXTENSION__);
```

## Step 4: Sources Tab - Bundle Analysis

### Navigate to Sources

1. Click **Sources** tab
2. Expand `www.airbnb.com` → `(webpack)`
3. Look for bundle files like `core-guest-[hash].js`

### Search for Routes

**Search for**: `/rooms/`

**You'll find route patterns:**
```javascript
"/rooms/:id"
"/rooms/:id/reviews"
"/s/:location/homes"
"/host/homes"
"/hosting/listings"
"/wishlists"
"/trips"
"/account-settings"
```

**Search for**: `api/v3`

**You'll find API operation names:**
```javascript
"StaysSearch"
"StaysPdpSections"
"HomesDetailsCardView"
"ReviewsListForListing"
"PdpAvailabilityCalendar"
"UserProfileBasicInfo"
"ExperiencesSearch"
"WishlistsForUser"
```

### Prettify Minified Code

1. **Click on** a bundle file like `core-guest-[hash].js`
2. Notice it's minified (one long line)
3. **Click the `{}`** icon at bottom-left (Pretty print)
4. Now the code is readable with proper indentation!

**Search again** for routes in prettified code

## Step 5: Application Tab - Storage

1. Click **Application** tab
2. Expand **Local Storage** → `https://www.airbnb.com`

**You'll see data like:**
```
_airbed_session_id: abc123...
jitney_client_session_id: xyz789...
previousTab: StaysSearchPage
searchSessionId: 550e8400-e29b-41d4-a716-446655440000
```

### Cookies

1. Click **Cookies** → `https://www.airbnb.com`

**You'll see authentication cookies:**
```
Name                   Value               HttpOnly  Secure
──────────────────────────────────────────────────────────
_airbed_session_id     abc123def456...     Yes       Yes
csrf_token             xyz789abc123...     No        Yes
```

**Security Note**: HttpOnly cookies are safer (not accessible via JavaScript)

## Step 6: Network Tab - Advanced Analysis

### Copy as cURL

1. **Right-click** on a request (e.g., `StaysSearch`)
2. **Copy** → **Copy as cURL**

**You get:**
```bash
curl 'https://www.airbnb.com/api/v3/StaysSearch' \
  -H 'authority: www.airbnb.com' \
  -H 'accept: application/json' \
  -H 'content-type: application/json' \
  -H 'cookie: _airbed_session_id=abc123...' \
  -H 'x-csrf-token: xyz789...' \
  --data-raw '{"operationName":"StaysSearch","variables":{...}}'
```

**Use case**: Replay the request in terminal, Postman, or scripts!

### Copy as Fetch

1. **Right-click** on a request
2. **Copy** → **Copy as fetch**

**You get JavaScript code:**
```javascript
fetch("https://www.airbnb.com/api/v3/StaysSearch", {
  "headers": {
    "accept": "application/json",
    "content-type": "application/json",
    "x-csrf-token": "xyz789..."
  },
  "body": "{\"operationName\":\"StaysSearch\",\"variables\":{...}}",
  "method": "POST"
});
```

**Use case**: Replay in Console, automate in scripts!

## Step 7: Performance Tab - Route Timing

1. Click **Performance** tab
2. **Click record** (circle icon)
3. **Navigate** through Airbnb (e.g., search → listing → back)
4. **Stop recording**

**You'll see a flame graph showing:**
- JavaScript execution time
- Rendering time
- API call timing
- Route transition performance

**Zoom in** on specific transitions to see which functions were called during route changes

## Step 8: React DevTools (Advanced)

If you have React DevTools extension installed:

1. Click **React** tab (⚛️ icon)
2. **Components** tree shows entire React component hierarchy
3. **Profiler** shows render performance

**Explore the component tree:**
```
<AirbnbApp>
  <Router>
    <StaysSearchPage>
      <SearchBar />
      <SearchResults>
        <ListingCard id="123" />
        <ListingCard id="456" />
      </SearchResults>
    </StaysSearchPage>
  </Router>
</AirbnbApp>
```

**Click on components** to see their props, state, and hooks!

## Step 9: Complete Route Map for Airbnb

### Frontend Routes (History API)

```
Base URL: https://www.airbnb.com

Public Routes:
├── /                          # Homepage
├── /s/:location/homes         # Search results
├── /rooms/:id                 # Listing details (PDP)
├── /rooms/:id/reviews         # Listing reviews
├── /experiences               # Experiences homepage
├── /experiences/:location     # Experiences by location
├── /help                      # Help center
└── /signup                    # Registration

Protected Routes (require auth):
├── /trips                     # Your trips
├── /wishlists                 # Saved listings
├── /wishlists/:id             # Specific wishlist
├── /account-settings          # Account settings
├── /account-settings/security # Security settings
├── /account-settings/payments # Payment methods
├── /user/show/:id             # User profile
└── /users/show/:id/reviews    # User reviews

Host Routes:
├── /host/homes                # Your listings
├── /hosting/listings          # Manage listings
├── /hosting/listings/:id      # Edit listing
├── /hosting/reservations      # Reservations
├── /hosting/calendar          # Calendar
└── /hosting/earnings          # Earnings

Booking Flow:
├── /book/stays/:id            # Booking page
├── /book/stays/:id/payment    # Payment page
└── /book/stays/:id/confirm    # Confirmation
```

### API Endpoints (GraphQL-like)

```
Base URL: https://www.airbnb.com/api/v3/

Search & Discovery:
├── POST /StaysSearch          # Search listings
├── POST /ExperiencesSearch    # Search experiences
├── POST /ExploreTabs          # Category tabs
└── POST /MapSearch            # Map-based search

Listing Details:
├── POST /StaysPdpSections     # PDP sections
├── POST /HomesDetailsCardView # Listing details
├── GET  /pdp_listing_details/:id
├── POST /PdpAvailabilityCalendar
├── POST /ReviewsListForListing
└── POST /PdpPoliciesSection

User & Account:
├── POST /UserProfileBasicInfo # User info
├── POST /WishlistsForUser     # Get wishlists
├── POST /TripsForUser         # Get trips
└── POST /AccountSettings      # Settings

Booking:
├── POST /CheckAvailability    # Check dates
├── POST /PriceBreakdown       # Get pricing
├── POST /SubmitReservation    # Book
└── POST /PaymentMethods       # Payment info

Host:
├── POST /HostListings         # Get listings
├── POST /ReservationsForHost  # Reservations
├── POST /CalendarAvailability # Calendar
└── POST /HostEarnings         # Earnings

V2 API (Legacy):
├── GET /api/v2/explore_tabs
├── GET /api/v2/pdp_listing_details/:id
└── GET /api/v2/reviews
```

---

# Part 3: Comparison & Key Differences

## Routing Mechanisms

| Aspect | Juice Shop | Airbnb |
|--------|-----------|---------|
| **Framework** | Angular | React |
| **Routing Type** | Hash-based (`#/`) | History API |
| **Route Pattern** | `/#/basket` | `/rooms/123` |
| **Browser History** | Hash doesn't reload | Clean URLs |
| **SEO** | Poor (hash routes) | Better (real URLs) |

## API Architecture

| Aspect | Juice Shop | Airbnb |
|--------|-----------|---------|
| **API Type** | RESTful | GraphQL-like |
| **Base Path** | `/rest/` | `/api/v3/` |
| **Endpoints** | `/rest/products/search` | `POST /StaysSearch` |
| **Request Format** | Query params/JSON | GraphQL operations |
| **Discoverability** | Easy (clear paths) | Harder (operation names) |

## Bundle Complexity

| Aspect | Juice Shop | Airbnb |
|--------|-----------|---------|
| **Minification** | Moderate | Heavy |
| **Obfuscation** | Low | High |
| **Bundle Naming** | `main.js` | `core-guest-[hash].js` |
| **Bundle Size** | ~2 MB | ~3+ MB |
| **Route Discovery** | Easy (search "path:") | Harder (minified) |

## Security & Privacy

| Aspect | Juice Shop | Airbnb |
|--------|-----------|---------|
| **Purpose** | Intentionally vulnerable | Production app |
| **Token Storage** | localStorage | HttpOnly cookies |
| **CSRF Protection** | Minimal | Strong (tokens) |
| **API Exposure** | Fully visible | Partially hidden |
| **Admin Routes** | Easy to find | Well-protected |

---

# Part 4: Advanced Techniques

## Technique 1: Automated Route Extraction Script

Run this in Console to auto-extract all routes:

### For Juice Shop (Hash-based):

```javascript
// Extract all unique hash routes from JavaScript bundles
const extractHashRoutes = () => {
  const routes = new Set();

  // Method 1: Check all script tags
  const scripts = document.querySelectorAll('script');
  scripts.forEach(script => {
    if (script.src) {
      fetch(script.src)
        .then(r => r.text())
        .then(code => {
          // Find Angular route definitions
          const routePattern = /path:\s*['"]([^'"]+)['"]/g;
          let match;
          while ((match = routePattern.exec(code)) !== null) {
            routes.add('/#/' + match[1]);
          }
        });
    }
  });

  // Method 2: Monitor navigation
  let lastHash = location.hash;
  routes.add(lastHash || '/#/');

  const observer = new MutationObserver(() => {
    if (location.hash !== lastHash) {
      routes.add(location.hash);
      lastHash = location.hash;
      console.log('New route discovered:', location.hash);
    }
  });

  observer.observe(document, { subtree: true, childList: true });

  // Return current routes
  setTimeout(() => {
    console.log('Discovered routes:', Array.from(routes).sort());
  }, 5000);
};

extractHashRoutes();
```

### For Airbnb (History API):

```javascript
// Monitor History API route changes
const extractHistoryRoutes = () => {
  const routes = new Set();
  routes.add(location.pathname);

  // Override pushState and replaceState
  const originalPushState = history.pushState;
  const originalReplaceState = history.replaceState;

  history.pushState = function(...args) {
    routes.add(args[2]);
    console.log('Route pushed:', args[2]);
    return originalPushState.apply(this, args);
  };

  history.replaceState = function(...args) {
    routes.add(args[2]);
    console.log('Route replaced:', args[2]);
    return originalReplaceState.apply(this, args);
  };

  // Listen for popstate (back/forward buttons)
  window.addEventListener('popstate', () => {
    routes.add(location.pathname);
    console.log('Route popped:', location.pathname);
  });

  // Log all routes after navigation
  setTimeout(() => {
    console.table(Array.from(routes).sort());
  }, 10000);
};

extractHistoryRoutes();
```

## Technique 2: API Endpoint Interceptor

Intercept and log all API calls automatically:

```javascript
// Intercept fetch API
const originalFetch = window.fetch;
const apiCalls = new Map();

window.fetch = async function(...args) {
  const url = args[0];
  const options = args[1] || {};

  console.log('🔵 API Call:', {
    url: url,
    method: options.method || 'GET',
    headers: options.headers,
    body: options.body
  });

  const response = await originalFetch.apply(this, args);

  // Clone response to read it without consuming
  const clone = response.clone();
  const data = await clone.json().catch(() => 'Not JSON');

  console.log('🟢 API Response:', {
    url: url,
    status: response.status,
    data: data
  });

  // Store for later analysis
  apiCalls.set(url, {
    method: options.method || 'GET',
    status: response.status,
    timestamp: new Date().toISOString()
  });

  return response;
};

// Export API call log
window.getApiLog = () => {
  console.table(Array.from(apiCalls.entries()).map(([url, data]) => ({
    URL: url,
    Method: data.method,
    Status: data.status,
    Time: data.timestamp
  })));
};

// After navigating around, run:
// getApiLog();
```

## Technique 3: Performance Monitoring

Track route change performance:

```javascript
// Monitor route performance
const routePerformance = [];

const trackRouteChange = () => {
  let lastRoute = location.pathname + location.hash;
  let startTime = performance.now();

  const checkChange = () => {
    const currentRoute = location.pathname + location.hash;
    if (currentRoute !== lastRoute) {
      const endTime = performance.now();
      const duration = endTime - startTime;

      routePerformance.push({
        from: lastRoute,
        to: currentRoute,
        duration: Math.round(duration) + 'ms',
        timestamp: new Date().toLocaleTimeString()
      });

      console.log(`⚡ Route change: ${lastRoute} → ${currentRoute} (${Math.round(duration)}ms)`);

      lastRoute = currentRoute;
      startTime = performance.now();
    }
  };

  setInterval(checkChange, 100);
};

trackRouteChange();

// View performance data
window.getRoutePerformance = () => {
  console.table(routePerformance);
};
```

## Technique 4: Webpack Bundle Analyzer

For React apps with source maps:

```javascript
// Find webpack modules
if (window.webpackJsonp || window.webpackChunk) {
  console.log('Webpack detected! Modules:', window.webpackJsonp || window.webpackChunk);
}

// List all loaded modules
const getWebpackModules = () => {
  if (!window.webpackJsonp) return [];

  const modules = [];
  window.webpackJsonp.forEach(chunk => {
    if (chunk[1]) {
      Object.keys(chunk[1]).forEach(id => {
        modules.push({
          id: id,
          code: chunk[1][id].toString().substring(0, 200) + '...'
        });
      });
    }
  });

  return modules;
};

console.table(getWebpackModules());
```

---

# Part 5: Practical Security Testing Scenarios

## Scenario 1: Finding Hidden Admin Routes (Juice Shop)

**Goal**: Discover and access the admin panel

### Step-by-step:

1. **Open Juice Shop**: `https://juice3.wonkatech.org/#/`
2. **F12** → **Sources** → `main.js`
3. **Search**: `admin`
4. **Find**: `{path: 'administration', component: AdministrationComponent}`
5. **Navigate**: `https://juice3.wonkatech.org/#/administration`
6. **Observe**: Login required or access denied
7. **Goal achieved**: Found hidden admin route!

### Exploitation (educational):

- Try default credentials
- Check for authentication bypass
- Look for API endpoints without auth checks

## Scenario 2: API Parameter Tampering (Airbnb)

**Goal**: Modify search parameters to discover hidden features

### Step-by-step:

1. **Perform normal search** on Airbnb
2. **F12** → **Network** → Find `StaysSearch` POST request
3. **Right-click** → **Copy as fetch**
4. **Paste in Console**
5. **Modify parameters**:

```javascript
fetch("https://www.airbnb.com/api/v3/StaysSearch", {
  "headers": {
    "accept": "application/json",
    "content-type": "application/json"
  },
  "body": JSON.stringify({
    "operationName": "StaysSearch",
    "variables": {
      "request": {
        "query": "Tokyo",
        "adults": 999,  // Modified!
        "priceMax": 1,  // Modified!
        "checkin": "2030-01-01"  // Far future
      }
    }
  }),
  "method": "POST"
}).then(r => r.json()).then(console.log);
```

6. **Observe**: How does the API handle invalid parameters?
7. **Security insight**: Test for input validation, error messages, rate limiting

## Scenario 3: JWT Token Analysis (Juice Shop)

**Goal**: Analyze authentication token structure

### Step-by-step:

1. **Login** to Juice Shop
2. **F12** → **Application** → **Local Storage**
3. **Copy token** value
4. **Go to** [jwt.io](https://jwt.io/)
5. **Paste token** in debugger

**You'll see decoded payload:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "username": "",
    "email": "admin@juice-sh.op",
    "password": "admin123",  // Password in token?!
    "isAdmin": true,
    "role": "admin"
  },
  "iat": 1612345678,
  "exp": 1612349278
}
```

**Security insights**:
- Password stored in JWT? (bad practice)
- `isAdmin` claim could be tampered
- Check signature algorithm (HS256 vs RS256)

---

# Part 6: Tools & Extensions

## Essential Browser Extensions

### 1. **React Developer Tools**
- **Purpose**: Inspect React component tree
- **Install**: Chrome Web Store → "React Developer Tools"
- **Usage**: Adds "React" tab to DevTools

### 2. **Redux DevTools**
- **Purpose**: Inspect Redux state management
- **Install**: Chrome Web Store → "Redux DevTools"
- **Usage**: View application state and actions

### 3. **Wappalyzer**
- **Purpose**: Identify technologies used on websites
- **Install**: Chrome Web Store → "Wappalyzer"
- **Usage**: Click icon to see tech stack

### 4. **EditThisCookie**
- **Purpose**: Edit cookies easily
- **Install**: Chrome Web Store → "EditThisCookie"
- **Usage**: Modify authentication cookies

### 5. **JSON Formatter**
- **Purpose**: Pretty-print JSON responses
- **Install**: Chrome Web Store → "JSON Formatter"
- **Usage**: Automatic when viewing JSON URLs

## External Tools

### Burp Suite
- **Purpose**: Intercept and modify HTTP traffic
- **Use case**: Advanced API testing, parameter tampering
- **Integration**: Configure browser proxy → Burp

### Postman
- **Purpose**: Test API endpoints
- **Use case**: Import cURL commands from DevTools
- **Integration**: Copy as cURL → Import to Postman

### curl (Command Line)
- **Purpose**: Make HTTP requests from terminal
- **Use case**: Automate API testing
- **Integration**: Copy as cURL from DevTools

---

# Summary & Cheat Sheet

## Quick Route Discovery Checklist

### ✅ Initial Setup
- [ ] Open target website
- [ ] Press F12 (DevTools)
- [ ] Enable "Preserve log" in Network tab
- [ ] Disable cache

### ✅ Framework Detection (Console)
- [ ] `console.log(window.ng)` (Angular)
- [ ] `console.log(typeof React)` (React)
- [ ] `console.log(window.Vue)` (Vue)

### ✅ Route Discovery (Sources)
- [ ] Find `main.js` or bundle files
- [ ] Search for `path:`, `route`, `/api/`
- [ ] Pretty-print minified code (`{}` icon)
- [ ] Note route patterns

### ✅ API Discovery (Network)
- [ ] Filter by XHR/Fetch
- [ ] Click around application
- [ ] Note all API endpoints
- [ ] Copy as cURL/Fetch for testing

### ✅ Storage Investigation (Application)
- [ ] Check Local Storage
- [ ] Check Session Storage
- [ ] Check Cookies
- [ ] Note authentication tokens

### ✅ Documentation
- [ ] Create route map
- [ ] List API endpoints
- [ ] Note authentication methods
- [ ] Document findings

## Key Keyboard Shortcuts

| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Open DevTools | `F12` or `Ctrl+Shift+I` | `Cmd+Option+I` |
| Search in file | `Ctrl+F` | `Cmd+F` |
| Search all files | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Pretty-print | Click `{}` | Click `{}` |
| Go to line | `Ctrl+G` | `Cmd+L` |
| Console | `Ctrl+Shift+J` | `Cmd+Option+J` |
| Network | `Ctrl+Shift+E` | `Cmd+Option+E` |

---

# Conclusion

You now have a complete methodology for discovering SPA routes using F12 DevTools:

1. **Juice Shop**: Hash-based routing, easy to discover, RESTful API
2. **Airbnb**: History API routing, production-grade, GraphQL-like API

**Key Skills Learned**:
- Network tab filtering and inspection
- Console framework detection
- Sources tab bundle analysis
- Application tab storage investigation
- Route monitoring scripts
- API endpoint discovery
- Security testing foundations

**Practice Exercise**: Apply these techniques to other popular SPAs:
- Gmail (`mail.google.com`)
- Twitter/X (`twitter.com`)
- LinkedIn (`linkedin.com`)
- Trello (`trello.com`)
- GitHub (`github.com`)

Happy hunting! 🔍