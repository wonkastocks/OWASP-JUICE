# Forged Feedback Challenge - Instructions

## Challenge Overview
**Name:** Forged Feedback
**Category:** Broken Access Control / IDOR (Insecure Direct Object Reference)
**Difficulty:** ⭐⭐⭐ (3 stars)
**Points:** 250

## Objective
Submit feedback on behalf of another user by manipulating the feedback submission process to forge their identity.

## Background
The feedback system allows users to submit comments and ratings about products or services. However, there's a vulnerability in how the system handles user identification during feedback submission. Your goal is to exploit this vulnerability to submit feedback that appears to come from a different user.

## Prerequisites
- Basic understanding of HTTP requests
- Familiarity with browser developer tools
- Knowledge of JSON/form data manipulation
- Understanding of authentication tokens and user IDs

## Instructions

### Step 1: Reconnaissance
1. **Create your own account** on the platform if you haven't already
2. **Navigate to the feedback section** (usually found at `/feedback` or similar)
3. **Submit legitimate feedback** first to understand the normal flow
4. **Open browser developer tools** (F12) and go to the Network tab

### Step 2: Analyze the Request
1. Submit another feedback while monitoring the Network tab
2. Look for the POST request to the feedback endpoint (e.g., `/api/feedback` or `/submit-feedback`)
3. Examine the request payload. You'll typically see:
   ```json
   {
     "comment": "Your feedback text",
     "rating": 5,
     "userId": "your-user-id",
     "email": "your-email@example.com"
   }
   ```

### Step 3: Identify the Vulnerability
The vulnerability exists because:
- The server trusts the `userId` or `email` field from the client
- No server-side validation confirms the authenticated user matches the submitted userId
- The feedback is associated with whatever userId is provided in the request

### Step 4: Exploit the Vulnerability

#### Method 1: Using Browser Developer Tools
1. **Intercept the feedback submission**:
   - Fill out the feedback form normally
   - Before clicking submit, open Developer Tools
   - Go to Network tab and enable request interception

2. **Modify the request**:
   - Find another user's ID (often visible in URLs, comments, or profiles)
   - Common target usernames: `admin`, `administrator`, `support`
   - Replace your userId/email with the target user's information

3. **Submit the forged feedback**:
   ```javascript
   // Example using fetch API in console
   fetch('/api/feedback', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
       'Authorization': 'Bearer ' + localStorage.getItem('token')
     },
     body: JSON.stringify({
       comment: "This feedback is forged!",
       rating: 5,
       userId: "admin-user-id",  // Target user's ID
       email: "admin@juice-shop.com"
     })
   });
   ```

#### Method 2: Using Burp Suite or OWASP ZAP
1. **Configure proxy** to intercept HTTP traffic
2. **Submit feedback normally** through the UI
3. **Intercept the request** in your proxy tool
4. **Modify the userId/email fields** to target user's information
5. **Forward the modified request**

#### Method 3: Using cURL
```bash
curl -X POST https://target-site.com/api/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "comment": "Forged feedback from admin",
    "rating": 1,
    "userId": "1",
    "email": "admin@site.com"
  }'
```

### Step 5: Verify Success
1. Check if the feedback appears in the feedback list
2. Verify it shows as submitted by the target user
3. The challenge should be marked as completed
4. You might receive a flag or success message

## Common Pitfalls
- **Wrong user ID format**: Some systems use numeric IDs, others use UUIDs
- **Missing authentication**: Ensure your session token is included
- **Rate limiting**: Some systems limit feedback submissions
- **Input validation**: The comment might need to meet certain criteria

## Security Implications
This vulnerability demonstrates:
- **Never trust client-side data** for user identification
- **Always validate on the server** that actions match the authenticated user
- **Implement proper access controls** for all user actions
- **Log suspicious activities** for security monitoring

## Mitigation (For Developers)
To fix this vulnerability:
```python
# Bad (vulnerable) code
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    user_id = data['userId']  # Trusting client input!
    save_feedback(user_id, data['comment'], data['rating'])

# Good (secure) code
@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_feedback():
    data = request.json
    user_id = current_user.id  # Get from session, not client!
    save_feedback(user_id, data['comment'], data['rating'])
```

## Additional Challenges
Once you've completed this challenge, try:
- Submit feedback as multiple different users
- Find if you can modify existing feedback
- Check if you can delete other users' feedback
- Test for SQL injection in the feedback fields

## Learning Resources
- [OWASP Top 10 - Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [IDOR Vulnerability Explained](https://portswigger.net/web-security/access-control/idor)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)

## Flag Format
The flag will typically be in one of these formats:
- `FLAG{forged_feedback_success}`
- `{admin_feedback_forged}`
- A success message in the response
- An achievement unlocked notification

---

**Note:** This challenge is for educational purposes only. Never attempt these techniques on systems you don't own or have explicit permission to test.