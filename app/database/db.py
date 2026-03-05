import sqlite3
import os
class Database:
    def __init__(self):
        # Go from app/database → app
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, "data")

        os.makedirs(data_dir, exist_ok=True)

        db_path = os.path.join(data_dir, "resilience.db")

        print("Creating/Using DB at:", db_path)

        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
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
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT NOT NULL,
            content TEXT NOT NULL,
            is_locked INTEGER DEFAULT 0,
            is_deleted INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );
        """)
        cursor.execute("""CREATE INDEX IF NOT EXISTS idx_entries_type ON entries(entry_type);""")
        cursor.execute("""CREATE INDEX IF NOT EXISTS idx_entries_deleted ON entries(is_deleted);""")

        self.connection.commit()

    def get_connection(self):
        return self.connection
    def close(self):
        self.connection.close()





    