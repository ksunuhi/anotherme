-- Migration: Verify existing users who registered before email verification was implemented
-- Date: 2025-12-16
-- Purpose: Mark all existing users as email_verified=true since they registered before
--          the email verification feature was added on Day 9 (2025-12-12)

-- Update all users created before 2025-12-12 to have email_verified = true
-- These users registered before email verification was implemented
UPDATE users
SET email_verified = 1
WHERE created_at < '2025-12-12 00:00:00'
  AND email_verified = 0;

-- Show updated users
SELECT id, email, full_name, email_verified, created_at
FROM users
WHERE email_verified = 1
ORDER BY created_at;
