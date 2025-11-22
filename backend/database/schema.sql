-- AnotherMe Database Schema
-- Birthday Social Network Platform
-- SQLite Version

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ============================================
-- Users Table
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,  -- UUID as TEXT in SQLite
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    display_name TEXT,
    birth_date DATE NOT NULL,  -- Format: YYYY-MM-DD
    gender TEXT NOT NULL CHECK(gender IN ('Male', 'Female', 'Other', 'Prefer not to say')),
    city TEXT NOT NULL,
    region TEXT NOT NULL,
    profile_picture_url TEXT,
    bio TEXT CHECK(length(bio) <= 500),
    is_discoverable BOOLEAN DEFAULT 1,
    email_verified BOOLEAN DEFAULT 0,
    oauth_provider TEXT,  -- 'google', 'facebook', or NULL
    oauth_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Indexes for users
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_birth_date ON users(birth_date);
CREATE INDEX IF NOT EXISTS idx_users_city ON users(city);
CREATE INDEX IF NOT EXISTS idx_users_is_discoverable ON users(is_discoverable);

-- ============================================
-- Posts Table
-- ============================================
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL,
    title TEXT CHECK(length(title) <= 200),
    content TEXT NOT NULL CHECK(length(content) <= 2000),
    visibility TEXT NOT NULL CHECK(visibility IN ('public', 'birthday_twins', 'friends', 'group')),
    group_id TEXT,  -- NULL if not a group post
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

-- Indexes for posts
CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_visibility ON posts(visibility);
CREATE INDEX IF NOT EXISTS idx_posts_group_id ON posts(group_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);

-- ============================================
-- Comments Table
-- ============================================
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    author_id TEXT NOT NULL,
    parent_comment_id TEXT,  -- NULL for top-level comments, set for replies
    content TEXT NOT NULL CHECK(length(content) <= 500),
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- Indexes for comments
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_author_id ON comments(author_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent_id ON comments(parent_comment_id);
CREATE INDEX IF NOT EXISTS idx_comments_created_at ON comments(created_at);

-- ============================================
-- Messages Table
-- ============================================
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    sender_id TEXT NOT NULL,
    recipient_id TEXT NOT NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for messages
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX IF NOT EXISTS idx_messages_is_read ON messages(is_read);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);
-- Composite index for conversations
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(sender_id, recipient_id, created_at);

-- ============================================
-- Friendships Table (One-way)
-- ============================================
CREATE TABLE IF NOT EXISTS friendships (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,      -- The person who added the friend
    friend_id TEXT NOT NULL,    -- The person being added as friend
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, friend_id)  -- Prevent duplicate friendships
);

-- Indexes for friendships
CREATE INDEX IF NOT EXISTS idx_friendships_user_id ON friendships(user_id);
CREATE INDEX IF NOT EXISTS idx_friendships_friend_id ON friendships(friend_id);

-- ============================================
-- Groups Table (Birthday-based)
-- ============================================
CREATE TABLE IF NOT EXISTS groups (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    group_type TEXT NOT NULL CHECK(group_type IN ('birthday', 'custom')),
    birth_year INTEGER,   -- For birthday groups
    birth_month INTEGER CHECK(birth_month BETWEEN 1 AND 12),  -- For birthday groups
    birth_day INTEGER CHECK(birth_day BETWEEN 1 AND 31),      -- For birthday groups
    member_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for groups
CREATE INDEX IF NOT EXISTS idx_groups_type ON groups(group_type);
CREATE INDEX IF NOT EXISTS idx_groups_birthday ON groups(birth_year, birth_month, birth_day);

-- ============================================
-- Group Memberships Table
-- ============================================
CREATE TABLE IF NOT EXISTS group_memberships (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    group_id TEXT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    UNIQUE(user_id, group_id)  -- User can only join a group once
);

-- Indexes for group memberships
CREATE INDEX IF NOT EXISTS idx_group_memberships_user_id ON group_memberships(user_id);
CREATE INDEX IF NOT EXISTS idx_group_memberships_group_id ON group_memberships(group_id);
CREATE INDEX IF NOT EXISTS idx_group_memberships_is_active ON group_memberships(is_active);

-- ============================================
-- Post Likes Table
-- ============================================
CREATE TABLE IF NOT EXISTS post_likes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    post_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    UNIQUE(user_id, post_id)  -- User can only like a post once
);

-- Indexes for post likes
CREATE INDEX IF NOT EXISTS idx_post_likes_user_id ON post_likes(user_id);
CREATE INDEX IF NOT EXISTS idx_post_likes_post_id ON post_likes(post_id);

-- ============================================
-- Comment Likes Table
-- ============================================
CREATE TABLE IF NOT EXISTS comment_likes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    comment_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
    UNIQUE(user_id, comment_id)  -- User can only like a comment once
);

-- Indexes for comment likes
CREATE INDEX IF NOT EXISTS idx_comment_likes_user_id ON comment_likes(user_id);
CREATE INDEX IF NOT EXISTS idx_comment_likes_comment_id ON comment_likes(comment_id);

-- ============================================
-- Triggers for maintaining counts
-- ============================================

-- Update post like_count when post_likes changes
CREATE TRIGGER IF NOT EXISTS update_post_like_count_insert
AFTER INSERT ON post_likes
BEGIN
    UPDATE posts SET like_count = like_count + 1 WHERE id = NEW.post_id;
END;

CREATE TRIGGER IF NOT EXISTS update_post_like_count_delete
AFTER DELETE ON post_likes
BEGIN
    UPDATE posts SET like_count = like_count - 1 WHERE id = OLD.post_id;
END;

-- Update comment like_count when comment_likes changes
CREATE TRIGGER IF NOT EXISTS update_comment_like_count_insert
AFTER INSERT ON comment_likes
BEGIN
    UPDATE comments SET like_count = like_count + 1 WHERE id = NEW.comment_id;
END;

CREATE TRIGGER IF NOT EXISTS update_comment_like_count_delete
AFTER DELETE ON comment_likes
BEGIN
    UPDATE comments SET like_count = like_count - 1 WHERE id = OLD.comment_id;
END;

-- Update post comment_count when comments changes
CREATE TRIGGER IF NOT EXISTS update_post_comment_count_insert
AFTER INSERT ON comments
BEGIN
    UPDATE posts SET comment_count = comment_count + 1 WHERE id = NEW.post_id;
END;

CREATE TRIGGER IF NOT EXISTS update_post_comment_count_delete
AFTER DELETE ON comments
BEGIN
    UPDATE posts SET comment_count = comment_count - 1 WHERE id = OLD.post_id;
END;

-- Update group member_count when memberships change
CREATE TRIGGER IF NOT EXISTS update_group_member_count_insert
AFTER INSERT ON group_memberships
WHEN NEW.is_active = 1
BEGIN
    UPDATE groups SET member_count = member_count + 1 WHERE id = NEW.group_id;
END;

CREATE TRIGGER IF NOT EXISTS update_group_member_count_delete
AFTER DELETE ON group_memberships
WHEN OLD.is_active = 1
BEGIN
    UPDATE groups SET member_count = member_count - 1 WHERE id = OLD.group_id;
END;

CREATE TRIGGER IF NOT EXISTS update_group_member_count_update
AFTER UPDATE OF is_active ON group_memberships
WHEN OLD.is_active != NEW.is_active
BEGIN
    UPDATE groups
    SET member_count = member_count + CASE WHEN NEW.is_active = 1 THEN 1 ELSE -1 END
    WHERE id = NEW.group_id;
END;

-- Update timestamps
CREATE TRIGGER IF NOT EXISTS update_users_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_posts_timestamp
AFTER UPDATE ON posts
BEGIN
    UPDATE posts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_comments_timestamp
AFTER UPDATE ON comments
BEGIN
    UPDATE comments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_groups_timestamp
AFTER UPDATE ON groups
BEGIN
    UPDATE groups SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
