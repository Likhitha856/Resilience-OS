-- ==========================
-- APP STATE TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS app_state (
    id INTEGER PRIMARY KEY,

    preferred_tone TEXT NOT NULL,
    preferred_grounding TEXT NOT NULL,
    support_preference TEXT NOT NULL,

    default_use_count INTEGER DEFAULT 0,
    prompt_shown INTEGER DEFAULT 0,
    personalized INTEGER DEFAULT 0,

    lock_enabled INTEGER DEFAULT 0,
    lock_hash TEXT
);

-- ==========================
-- ENTRIES TABLE
-- ==========================

CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    entry_type TEXT NOT NULL,               -- 'vent' or 'reflection'
    content TEXT NOT NULL,

    is_locked INTEGER DEFAULT 0,
    is_deleted INTEGER DEFAULT 0,

    created_at TEXT NOT NULL
);