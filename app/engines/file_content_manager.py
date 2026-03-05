from datetime import datetime


class FileContentManager:
    """
    MANAGES COLLECTION (Database-backed), not UI.
    """

    def __init__(self, db):
        self.conn = db.get_connection()

    # -------------------------
    # SAVE ENTRY
    # -------------------------
    def save_entry(self, content, entry_type, is_locked):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO entries (
                entry_type,
                content,
                is_locked,
                is_deleted,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            entry_type,
            content,
            int(is_locked),
            0,
            datetime.now().isoformat()
        ))

        self.conn.commit()
        return cursor.lastrowid


    # -------------------------
    # LIST ENTRIES
    # -------------------------
    def display_entries(self, entry_type):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT id, entry_type, created_at, is_locked
            FROM entries
            WHERE entry_type = ?
            AND is_deleted = 0
            ORDER BY created_at DESC
        """, (entry_type,))

        return cursor.fetchall()


    # -------------------------
    # OPEN ENTRY
    # -------------------------
    def open_entry(self, entry_id, state, password=None):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM entries
            WHERE id = ?
            AND is_deleted = 0
        """, (entry_id,))

        row = cursor.fetchone()

        if not row:
            return None

        if row["is_locked"]:

            if not password:
                return "PASSWORD_REQUIRED"

            if not state.feature_lock.verify_access(password):
                return "INVALID_PASSWORD"

        return row


    # -------------------------
    # SOFT DELETE
    # -------------------------
    def delete_entry(self, entry_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE entries
            SET is_deleted = 1
            WHERE id = ?
        """, (entry_id,))

        self.conn.commit()