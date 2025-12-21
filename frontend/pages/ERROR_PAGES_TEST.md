# Error Pages Testing Guide

This document explains how to test the custom error pages (404 and 500).

## Error Pages Created

1. **404.html** - Page Not Found
2. **500.html** - Internal Server Error

## How to Test

### Method 1: Direct Access (Frontend Server)

If using a simple HTTP server for the frontend:

```bash
cd frontend
python -m http.server 8080
```

Then visit:
- **404 Page**: http://localhost:8080/pages/404.html
- **500 Page**: http://localhost:8080/pages/500.html

### Method 2: Testing 404 Errors (Real Scenario)

1. Start your backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Try accessing a non-existent API endpoint:
   ```
   http://localhost:8000/api/nonexistent-endpoint
   ```
   - API requests will return JSON errors (as expected)

3. Try accessing a non-existent page:
   ```
   http://localhost:8000/nonexistent-page
   ```
   - Should show the custom 404 page

### Method 3: Testing 500 Errors

To test the 500 error page, you would need to trigger a server error. This is harder to test in development, but the page is ready for production use.

## Features of Error Pages

### 404 Page Features:
- ✅ Large, clear "404" error code
- ✅ Friendly error message
- ✅ "Go to Homepage" button
- ✅ "Go Back" button
- ✅ Quick links to important pages (Dashboard, Friends, Messages, Contact)
- ✅ Fun fact about HTTP 404 errors
- ✅ Floating animation on icon
- ✅ Responsive design (works on mobile)

### 500 Page Features:
- ✅ Large, clear "500" error code
- ✅ Helpful error message
- ✅ "Try Again" button (reloads page)
- ✅ "Go to Homepage" button
- ✅ Checklist of what users can do
- ✅ Status message explaining the error
- ✅ Unique error reference ID for debugging
- ✅ Pulse animation on icon
- ✅ Responsive design (works on mobile)

## Design Consistency

Both error pages:
- Match the AnotherMe color scheme (primary color: #6366F1)
- Use Tailwind CSS (same as rest of the site)
- Include custom animations
- Are fully responsive (mobile-friendly)
- Have clear call-to-action buttons
- Provide helpful navigation options

## Backend Configuration

The FastAPI backend (`main.py`) has been configured with custom exception handlers:

1. **API Requests** (`/api/*`):
   - Return JSON error responses
   - Preserves API functionality

2. **Page Requests** (everything else):
   - Return custom HTML error pages
   - Better user experience

## Testing Checklist

- [✅] 404 page displays correctly
- [✅] 500 page displays correctly
- [✅] "Go to Homepage" button works
- [✅] "Go Back" button works (404 page)
- [✅] "Try Again" button works (500 page)
- [✅] All quick links work
- [✅] Pages are responsive on mobile
- [✅] Animations work smoothly
- [✅] Error reference ID is generated (500 page)

## Production Notes

In production:
- These pages will automatically be shown for 404/500 errors
- API endpoints will still return JSON (not affected)
- Error logs will be generated server-side for debugging
- Consider adding analytics tracking to error pages
