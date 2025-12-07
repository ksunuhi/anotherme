# Email Setup Guide

This guide will help you configure Gmail SMTP for the AnotherMe platform's email features.

## Features Requiring Email

1. **Contact Form** - Users can send messages to site admin
2. **Forgot Password** - Users can request password reset links via email

## Gmail SMTP Configuration

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to **Security**
3. Enable **2-Step Verification** if not already enabled

### Step 2: Create App Password

1. Visit: https://myaccount.google.com/apppasswords
2. Select **Mail** as the app
3. Select **Other (Custom name)** as the device
4. Enter a name like "AnotherMe Platform"
5. Click **Generate**
6. Google will display a 16-character password - **copy this immediately** (you won't see it again)

### Step 3: Configure Environment Variables

Edit your `.env` file and add/update these values:

```env
# Email Configuration (SMTP)
ADMIN_EMAIL=your-admin-email@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password-here
SMTP_FROM_NAME=AnotherMe
SMTP_FROM_EMAIL=noreply@anotherme.com

# Frontend URL (for password reset links)
FRONTEND_URL=http://localhost:8080
```

**Important Notes:**
- `SMTP_USER`: Your full Gmail address (e.g., myemail@gmail.com)
- `SMTP_PASSWORD`: The 16-character app password (remove spaces)
- `ADMIN_EMAIL`: Where contact form submissions will be sent
- `SMTP_FROM_EMAIL`: Can be different from SMTP_USER (shown as sender)
- `FRONTEND_URL`: Your frontend URL for generating password reset links

### Example Configuration

```env
ADMIN_EMAIL=admin@example.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=myproject@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_FROM_NAME=AnotherMe
SMTP_FROM_EMAIL=noreply@anotherme.com
FRONTEND_URL=http://localhost:8080
```

## Testing Email Functionality

### 1. Test Contact Form

```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Contact",
    "message": "This is a test message from the contact form."
  }'
```

You should receive an email at your `ADMIN_EMAIL` address.

### 2. Test Forgot Password

```bash
curl -X POST http://localhost:8000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "existing-user@example.com"
  }'
```

The user should receive an email with a password reset link.

### 3. Test from Frontend

1. Start the backend: `uvicorn main:app --reload`
2. Start the frontend: `cd frontend && python -m http.server 8080`
3. Visit: http://localhost:8080/pages/contact.html
4. Fill out and submit the contact form
5. Visit: http://localhost:8080/pages/forgot-password.html
6. Request a password reset

## Gmail Sending Limits

Gmail App Passwords have sending limits:
- **Free Gmail accounts:** 500 emails per day
- **Google Workspace accounts:** 2,000 emails per day

This is sufficient for development and small-scale production use.

## Production Recommendations

For production deployment, consider:

1. **SendGrid** - 100 emails/day free, then paid plans
2. **Mailgun** - 5,000 emails/month free
3. **Amazon SES** - Very cheap ($0.10 per 1,000 emails)
4. **Postmark** - Excellent deliverability, starts at $15/month

## Troubleshooting

### "Authentication failed" error

**Cause:** Incorrect app password or 2FA not enabled

**Solution:**
1. Verify 2-Factor Authentication is enabled
2. Generate a new app password
3. Double-check SMTP_USER and SMTP_PASSWORD in .env
4. Make sure there are no spaces in the app password

### Emails not being received

**Cause:** Email in spam folder or incorrect ADMIN_EMAIL

**Solution:**
1. Check spam/junk folder
2. Verify ADMIN_EMAIL is correct in .env
3. Add SMTP_FROM_EMAIL to your contacts to avoid spam
4. Check backend logs for error messages

### "Connection timed out" error

**Cause:** Firewall blocking SMTP port

**Solution:**
1. Check if port 587 is open
2. Try using port 465 with SSL (update code if needed)
3. Check if corporate/school network blocks SMTP

### Reset link doesn't work

**Cause:** Incorrect FRONTEND_URL

**Solution:**
1. Verify FRONTEND_URL in .env matches your frontend address
2. Make sure it doesn't have a trailing slash
3. Example: `http://localhost:8080` (not `http://localhost:8080/`)

## Security Notes

- **Never commit** your `.env` file to version control
- **App passwords** are as sensitive as your main password
- **Rotate app passwords** periodically
- **Use environment variables** for all sensitive data
- **Enable 2FA** on all admin/developer Google accounts

## Email Templates

The platform includes professional HTML email templates for:

1. **Contact Form Submissions**
   - Shows sender name, email, subject, and message
   - Reply-to header set to sender's email
   - Professional styling with AnotherMe branding

2. **Password Reset Emails**
   - Clickable reset button
   - Copy-paste link fallback
   - 1-hour expiration warning
   - Security notice about ignoring if not requested

Both templates include plain text alternatives for email clients that don't support HTML.

## Next Steps

After configuring email:
1. Restart your backend server to load new .env values
2. Test both contact form and password reset
3. Verify emails are received and formatted correctly
4. Check spam folder if emails don't arrive
5. Bookmark this guide for future reference

---

For more information, see:
- Backend email code: `backend/app/core/email.py`
- Password reset model: `backend/app/models/password_reset.py`
- API endpoints: `backend/app/api/contact.py` and `backend/app/api/auth.py`
