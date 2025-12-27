-- ============================================
-- Clear All Data from AnotherMe Database
-- Use this to clean up test data before production
-- ============================================

-- IMPORTANT: This will permanently delete ALL data from all tables!
-- Make sure you have a backup if needed.

-- Disable foreign key constraints temporarily for easier cleanup
PRAGMA foreign_keys = OFF;

-- Delete data from all tables
-- Order doesn't matter with foreign keys disabled, but listed logically

-- Delete child tables first (good practice even with FK off)
DELETE FROM comment_likes;
DELETE FROM post_likes;
DELETE FROM comments;
DELETE FROM posts;
DELETE FROM messages;
DELETE FROM friendships;
DELETE FROM password_reset_tokens;
DELETE FROM email_verification_tokens;

-- Delete parent table last
DELETE FROM users;

-- Re-enable foreign key constraints
PRAGMA foreign_keys = ON;

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
