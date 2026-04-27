-- AI Content Generator Database Schema
-- PostgreSQL (Supabase)
-- Run this script in Supabase SQL Editor

-- ============================================
-- 1. USERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    avatar_url TEXT,
    plan VARCHAR(20) DEFAULT 'free',
    daily_message_count INTEGER DEFAULT 0,
    last_message_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for users table
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- ============================================
-- 2. CHAT SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content_type VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for chat_sessions table
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at ON chat_sessions(updated_at DESC);

-- ============================================
-- 3. CHAT MESSAGES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    model_used VARCHAR(100),
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for chat_messages table
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);

-- ============================================
-- 4. TRIGGER: Auto-update updated_at timestamp
-- ============================================

-- Function to update updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for users table
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for chat_sessions table
CREATE TRIGGER update_chat_sessions_updated_at
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 5. SAMPLE DATA (Optional - for testing)
-- ============================================

-- Uncomment below to insert sample data for testing

/*
-- Sample user (password: "password123" - hashed with BCrypt)
INSERT INTO users (email, username, password_hash, full_name, plan)
VALUES (
    'demo@example.com',
    'demouser',
    '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy',
    'Demo User',
    'free'
);

-- Sample chat session
INSERT INTO chat_sessions (user_id, title, content_type)
SELECT id, 'My First Chat', 'general'
FROM users WHERE email = 'demo@example.com';

-- Sample messages
INSERT INTO chat_messages (session_id, user_id, role, content)
SELECT 
    cs.id,
    u.id,
    'user',
    'Hello! Can you help me write a blog post?'
FROM users u
JOIN chat_sessions cs ON cs.user_id = u.id
WHERE u.email = 'demo@example.com';

INSERT INTO chat_messages (session_id, user_id, role, content, model_used, tokens_used)
SELECT 
    cs.id,
    u.id,
    'assistant',
    'Of course! I''d be happy to help you write a blog post. What topic would you like to write about?',
    'nvidia/llama-3.1-nemotron-70b-instruct:free',
    45
FROM users u
JOIN chat_sessions cs ON cs.user_id = u.id
WHERE u.email = 'demo@example.com';
*/

-- ============================================
-- 6. USEFUL QUERIES FOR MONITORING
-- ============================================

-- View all users
-- SELECT * FROM users ORDER BY created_at DESC;

-- View user with session count
-- SELECT 
--     u.id,
--     u.email,
--     u.username,
--     u.plan,
--     u.daily_message_count,
--     COUNT(DISTINCT cs.id) as total_sessions,
--     COUNT(cm.id) as total_messages
-- FROM users u
-- LEFT JOIN chat_sessions cs ON cs.user_id = u.id
-- LEFT JOIN chat_messages cm ON cm.user_id = u.id
-- GROUP BY u.id;

-- View recent chat sessions
-- SELECT 
--     cs.id,
--     cs.title,
--     cs.content_type,
--     u.username,
--     cs.created_at,
--     COUNT(cm.id) as message_count
-- FROM chat_sessions cs
-- JOIN users u ON u.id = cs.user_id
-- LEFT JOIN chat_messages cm ON cm.session_id = cs.id
-- GROUP BY cs.id, u.username
-- ORDER BY cs.updated_at DESC
-- LIMIT 10;

-- View messages in a session
-- SELECT 
--     cm.role,
--     cm.content,
--     cm.model_used,
--     cm.tokens_used,
--     cm.created_at
-- FROM chat_messages cm
-- WHERE cm.session_id = '<session-id-here>'
-- ORDER BY cm.created_at ASC;

-- ============================================
-- SCHEMA CREATION COMPLETE
-- ============================================

-- Verify tables created
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    AND table_name IN ('users', 'chat_sessions', 'chat_messages')
ORDER BY table_name;
