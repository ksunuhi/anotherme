# 🔒 Security Testing Plan - AnotherMe

## 📋 Pre-Test Setup

### Step 1: Install New Libraries
```bash
cd backend
pip install slowapi==0.1.9 bleach==6.1.0
```

**Expected Output:**
```
Successfully installed slowapi-0.1.9 bleach-6.1.0
```

### Step 2: Restart Backend Server
```bash
# Stop the current server (Ctrl+C if running)
cd backend
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Ensure Frontend is Running
```bash
cd frontend
python -m http.server 8080
```

**Expected Output:**
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

---

## 🧪 Test Suite

## Test 1: Login Rate Limiting (5 attempts per 15 minutes)

**Purpose:** Prevent brute force password attacks

### Steps:
1. **Open login page:** `http://localhost:8080/pages/login.html`
2. **Attempt 1:** Enter wrong password → Click "Sign In"
   - ✅ Expected: "Incorrect email or password"
3. **Attempt 2:** Enter wrong password → Click "Sign In"
   - ✅ Expected: "Incorrect email or password"
4. **Attempt 3:** Enter wrong password → Click "Sign In"
   - ✅ Expected: "Incorrect email or password"
5. **Attempt 4:** Enter wrong password → Click "Sign In"
   - ✅ Expected: "Incorrect email or password"
6. **Attempt 5:** Enter wrong password → Click "Sign In"
   - ✅ Expected: "Incorrect email or password"
7. **Attempt 6:** Enter wrong password → Click "Sign In"
   - ✅ **Expected: "Rate limit exceeded: 5 per 15 minute"**
   - ✅ **HTTP 429 (Too Many Requests)**

8. **Wait 15 minutes** OR **restart server** to reset
9. **Attempt 7:** Enter **correct** password → Click "Sign In"
   - ✅ Expected: Login successful

**Result:** ☐ PASS / ☐ FAIL

---

## Test 2: Registration Rate Limiting (3 per hour)

**Purpose:** Prevent fake account spam

### Steps:
1. **Clear browser cache** (to get a new IP tracking)
2. **Register Account 1:**
   - Go to: `http://localhost:8080/pages/register.html`
   - Fill form with test data (use email: `test1@test.com`)
   - Click "Create Account"
   - ✅ Expected: Success message

3. **Register Account 2:**
   - Use email: `test2@test.com`
   - ✅ Expected: Success message

4. **Register Account 3:**
   - Use email: `test3@test.com`
   - ✅ Expected: Success message

5. **Register Account 4:**
   - Use email: `test4@test.com`
   - ✅ **Expected: "Rate limit exceeded: 3 per 1 hour"**
   - ✅ **HTTP 429 (Too Many Requests)**

**Result:** ☐ PASS / ☐ FAIL

---

## Test 3: Post Creation Rate Limiting (10 per 5 minutes)

**Purpose:** Prevent content spam

### Steps:
1. **Login** to your account
2. **Go to Dashboard:** `http://localhost:8080/pages/dashboard.html`
3. **Create Post 1:** Type "Test post 1" → Click "Post"
   - ✅ Expected: Post created successfully
4. **Create Posts 2-10:** Repeat rapidly
   - ✅ Expected: All succeed (total 10 posts)
5. **Create Post 11:** Type "Test post 11" → Click "Post"
   - ✅ **Expected: Red toast notification appears at top-right**
   - ✅ **Message: "Rate limit exceeded: 10 per 5 minute"**
   - ✅ **Post does NOT appear in feed**

6. **Wait 5 minutes** OR **restart server**
7. **Create Post 12:** Type "Test post 12" → Click "Post"
   - ✅ Expected: Success (limit reset)

**Result:** ☐ PASS / ☐ FAIL

---

## Test 4: Comment Rate Limiting (20 per 5 minutes)

**Purpose:** Prevent comment spam

### Steps:
1. **Login** to your account
2. **Go to Dashboard**
3. **Find any post** → Click "Comment" to open comments
4. **Create 20 comments rapidly:**
   - Comment 1: "Test 1" → Ctrl+Enter
   - Comment 2: "Test 2" → Ctrl+Enter
   - ... (repeat 20 times)
   - ✅ Expected: All 20 succeed
5. **Create Comment 21:** "Test 21" → Ctrl+Enter
   - ✅ **Expected: Red toast notification**
   - ✅ **Message: "Rate limit exceeded: 20 per 5 minute"**
   - ✅ **Comment does NOT appear**

**Result:** ☐ PASS / ☐ FAIL

---

## Test 5: XSS Protection - Posts

**Purpose:** Prevent script injection attacks

### Test 5a: Script Tag Injection
1. **Login** and go to **Dashboard**
2. **Create a post** with this content:
   ```
   Hello! <script>alert('XSS Attack!')</script>
   ```
3. **Click "Post"**
4. **Check the displayed post:**
   - ✅ **Expected:** Text shows literally as:
     ```
     Hello! <script>alert('XSS Attack!')</script>
     ```
   - ❌ **NOT Expected:** Alert popup appears
   - ✅ **No JavaScript execution**

5. **Verify in database:**
   ```bash
   cd backend
   sqlite3 database/anotherme.db
   SELECT content FROM posts ORDER BY created_at DESC LIMIT 1;
   ```
   - ✅ **Expected:** Script tags are converted to safe text

**Result:** ☐ PASS / ☐ FAIL

---

### Test 5b: Image XSS Injection
1. **Create a post** with:
   ```
   Check this: <img src=x onerror=alert('Hacked!')>
   ```
2. **Click "Post"**
3. **Check displayed post:**
   - ✅ **Expected:** Shows as plain text (no broken image, no alert)
   - ✅ **Script doesn't execute**

**Result:** ☐ PASS / ☐ FAIL

---

### Test 5c: Iframe Injection
1. **Create a post** with:
   ```
   <iframe src="https://evil.com"></iframe> Click here!
   ```
2. **Click "Post"**
3. **Check displayed post:**
   - ✅ **Expected:** Shows as plain text
   - ✅ **No iframe embedded**

**Result:** ☐ PASS / ☐ FAIL

---

## Test 6: XSS Protection - Comments

**Purpose:** Ensure comments are also sanitized

### Steps:
1. **Login** and go to **Dashboard**
2. **Find any post** → Click "Comment"
3. **Add comment:**
   ```
   Nice post! <script>alert('Comment XSS')</script>
   ```
4. **Press Ctrl+Enter** to submit
5. **Check displayed comment:**
   - ✅ **Expected:** Script tags show as plain text
   - ❌ **NOT Expected:** Alert popup

**Result:** ☐ PASS / ☐ FAIL

---

## Test 7: XSS Protection - Messages

**Purpose:** Ensure messages are sanitized

### Steps:
1. **Login** to account A
2. **Go to Messages** (or send via dashboard)
3. **Send message to another user:**
   ```
   Hello! <b>Bold text</b> <script>alert('Message XSS')</script>
   ```
4. **Login as recipient** (account B)
5. **Check received message:**
   - ✅ **Expected:** Script tags show as plain text
   - ✅ **No bold text** (HTML stripped)
   - ❌ **NOT Expected:** Alert popup

**Result:** ☐ PASS / ☐ FAIL

---

## Test 8: XSS Protection - User Bio

**Purpose:** Ensure bio is sanitized

### Steps:
1. **Login** and go to **Profile**
2. **Click "Edit Profile"**
3. **Edit Bio field:**
   ```
   Web developer from NYC. <script>alert('Bio XSS')</script>
   Visit my site: <a href="javascript:alert('XSS')">Click here</a>
   ```
4. **Click "Save Changes"**
5. **Reload profile page**
6. **Check displayed bio:**
   - ✅ **Expected:** Script tags show as plain text
   - ✅ **No clickable link**
   - ❌ **NOT Expected:** Alert popup

**Result:** ☐ PASS / ☐ FAIL

---

## Test 9: Security Headers

**Purpose:** Verify browser security headers are present

### Steps:
1. **Open any page** (e.g., Dashboard)
2. **Open DevTools:** Press F12
3. **Go to Network tab**
4. **Reload page:** F5
5. **Click on the first request** (usually the HTML page)
6. **Go to "Headers" section** → Scroll to "Response Headers"

**Check for these headers:**
- ✅ `X-Content-Type-Options: nosniff`
- ✅ `X-Frame-Options: DENY`
- ✅ `X-XSS-Protection: 1; mode=block`
- ✅ `Referrer-Policy: strict-origin-when-cross-origin`
- ✅ `Content-Security-Policy: ...` (should exist)

**Screenshot location for verification:**
DevTools → Network → (select request) → Headers → Response Headers

**Result:** ☐ PASS / ☐ FAIL

---

## Test 10: Normal Usage Still Works

**Purpose:** Ensure security doesn't break normal functionality

### Test 10a: Normal Login
1. **Go to login page**
2. **Enter correct credentials**
3. **Click "Sign In"**
   - ✅ Expected: Login successful

**Result:** ☐ PASS / ☐ FAIL

---

### Test 10b: Normal Post Creation
1. **Create a normal post:**
   ```
   Just had a great day celebrating my birthday with my twin! 🎂
   ```
2. **Click "Post"**
   - ✅ Expected: Post created successfully
   - ✅ Content displays correctly

**Result:** ☐ PASS / ☐ FAIL

---

### Test 10c: Normal Comment
1. **Comment on a post:**
   ```
   Happy birthday! Hope you had fun!
   ```
2. **Press Ctrl+Enter**
   - ✅ Expected: Comment appears
   - ✅ Text displays correctly

**Result:** ☐ PASS / ☐ FAIL

---

### Test 10d: Normal Message
1. **Send a normal message:**
   ```
   Hey! We share the same birthday! Want to be friends?
   ```
2. **Send**
   - ✅ Expected: Message sent successfully
   - ✅ Text displays correctly

**Result:** ☐ PASS / ☐ FAIL

---

### Test 10e: Profile Bio Update
1. **Edit profile bio:**
   ```
   Software engineer from San Francisco. Love meeting birthday twins!
   ```
2. **Save**
   - ✅ Expected: Bio updated
   - ✅ Text displays correctly

**Result:** ☐ PASS / ☐ FAIL

---

## Test 11: Password Reset Rate Limiting (3 per hour)

**Purpose:** Prevent password reset email spam

### Steps:
1. **Go to:** `http://localhost:8080/pages/forgot-password.html`
2. **Request 1:** Enter your email → Click "Reset Password"
   - ✅ Expected: Success message
3. **Request 2:** Enter email again → Click "Reset Password"
   - ✅ Expected: Success message
4. **Request 3:** Enter email again → Click "Reset Password"
   - ✅ Expected: Success message
5. **Request 4:** Enter email again → Click "Reset Password"
   - ✅ **Expected: "Rate limit exceeded: 3 per 1 hour"**

**Result:** ☐ PASS / ☐ FAIL

---

## 📊 Test Summary

### Results Table

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Login Rate Limiting | ☐ PASS / ☐ FAIL | |
| 2 | Registration Rate Limiting | ☐ PASS / ☐ FAIL | |
| 3 | Post Rate Limiting | ☐ PASS / ☐ FAIL | |
| 4 | Comment Rate Limiting | ☐ PASS / ☐ FAIL | |
| 5a | XSS - Script Tag in Post | ☐ PASS / ☐ FAIL | |
| 5b | XSS - Image Tag in Post | ☐ PASS / ☐ FAIL | |
| 5c | XSS - Iframe in Post | ☐ PASS / ☐ FAIL | |
| 6 | XSS - Comments | ☐ PASS / ☐ FAIL | |
| 7 | XSS - Messages | ☐ PASS / ☐ FAIL | |
| 8 | XSS - Bio | ☐ PASS / ☐ FAIL | |
| 9 | Security Headers | ☐ PASS / ☐ FAIL | |
| 10a | Normal Login | ☐ PASS / ☐ FAIL | |
| 10b | Normal Post | ☐ PASS / ☐ FAIL | |
| 10c | Normal Comment | ☐ PASS / ☐ FAIL | |
| 10d | Normal Message | ☐ PASS / ☐ FAIL | |
| 10e | Normal Bio | ☐ PASS / ☐ FAIL | |
| 11 | Password Reset Limiting | ☐ PASS / ☐ FAIL | |

---

## 🚨 If Tests Fail

### Login Rate Limiting Not Working?
- Check: Backend server restarted after installing slowapi?
- Check: No errors in terminal?
- Try: Clear browser cache

### XSS Protection Not Working?
- Check: Backend restarted after installing bleach?
- Check: Posts/comments being saved to database correctly?
- Try: Check backend terminal for errors

### Security Headers Missing?
- Check: DevTools → Network → Response Headers
- Check: Looking at the HTML page request (not API requests)
- Try: Hard refresh (Ctrl+Shift+R)

---

## ✅ Success Criteria

**All tests should PASS for security to be complete:**
- ☑ All rate limits working (prevents abuse)
- ☑ All XSS tests blocked (prevents attacks)
- ☑ All security headers present (browser protection)
- ☑ Normal usage unaffected (no broken features)

---

## 📝 Notes

- **Rate limits reset:** Either wait the time period OR restart server
- **IP tracking:** Uses client IP address (same computer = same IP)
- **Production:** In production with multiple users, each user has different IP
- **XSS tests:** NEVER run on production - only on local test environment

---

Last Updated: 2025-12-16
