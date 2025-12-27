-- ============================================
-- Clear All Data from AnotherMe Database (Safe Version)
-- This version keeps foreign key constraints enabled
-- Deletes in the correct order to respect constraints
-- ============================================

-- IMPORTANT: This will permanently delete ALL data from all tables!
-- Make sure you have a backup if needed.

-- Ensure foreign key constraints are enabled
PRAGMA foreign_keys = ON;

-- Delete data in order that respects foreign key constraints
-- Child tables first, parent tables last

-- 1. Delete likes (depend on comments/posts and users)
DELETE FROM comment_likes;
DELETE FROM post_likes;

-- 2. Delete comments (depend on posts and users)
DELETE FROM comments;

-- 3. Delete posts (depend on users)
DELETE FROM posts;

-- 4. Delete messages (depend on users)
DELETE FROM messages;

-- 5. Delete friendships (depend on users)
DELETE FROM friendships;

-- 6. Delete password reset tokens (depend on users)
DELETE FROM password_reset_tokens;

-- 7. Delete email verification tokens (depend on users)
DELETE FROM email_verification_tokens;

-- 8. Finally, delete users (parent table)
DELETE FROM users;

-- Verify all tables are empty
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'posts', COUNT(*) FROM posts
UNION ALL
SELECT 'comments', COUNT(*) FROM comments
UNION ALL
SELECT 'messages', COUNT(*) FROM messages
UNION ALL
SELECT 'friendships', COUNT(*) FROM friendships
UNION ALL
SELECT 'post_likes', COUNT(*) FROM post_likes
UNION ALL
SELECT 'comment_likes', COUNT(*) FROM comment_likes
UNION ALL
SELECT 'password_reset_tokens', COUNT(*) FROM password_reset_tokens
UNION ALL
SELECT 'email_verification_tokens', COUNT(*) FROM email_verification_tokens;
