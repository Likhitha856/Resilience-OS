from datetime import datetime


class FileContentManager:
    """
    MANAGES COLLECTION (Database-backed), not UI.
    """

    def __init__(self, db):
        self.conn = db.get_connection()
    def get_connection(self):
        return self.conn
    # -------------------------
    # SAVE ENTRY
    # -------------------------
    def save_entry(self, content, entry_type, is_locked, user_id=None, anonymous_id=None):

        conn = self.get_connection()
        cursor = conn.cursor()

        created_at = datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO entries (user_id, anonymous_id, entry_type, content, created_at, is_locked)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, anonymous_id, entry_type, content, created_at, int(is_locked))
        )

        conn.commit()

        return cursor.lastrowid


    # -------------------------
    # LIST ENTRIES
    # -------------------------
    def display_entries(self, entry_type, user_id=None, anonymous_id=None):

        conn = self.get_connection()
        cursor = conn.cursor()

        if user_id:

            cursor.execute(
                """
                SELECT id, created_at, is_locked
                FROM entries
                WHERE entry_type = ?
                AND user_id = ?
                AND is_deleted = 0
                ORDER BY id DESC
                """,
                (entry_type, user_id)
            )

        else:

            cursor.execute(
                """
                SELECT id, created_at, is_locked
                FROM entries
                WHERE entry_type = ?
                AND anonymous_id = ?
                AND is_deleted = 0
                ORDER BY id DESC
                """,
                (entry_type, anonymous_id)
            )

        rows = cursor.fetchall()

        return [
            {
                "id": r[0],
                "created_at": r[1],
                "is_locked": r[2]
            }
            for r in rows
        ]

    # -------------------------
    # OPEN ENTRY
    # -------------------------
    def open_entry(self, entry_id, state, password, owner):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, entry_type, content, created_at, is_locked
            FROM entries
            WHERE id = ?
            AND (user_id = ? OR anonymous_id = ?)
            AND is_deleted = 0
            """,
            (entry_id, owner, owner)
        )

        row = cursor.fetchone()

        if not row:
            return None

        if row["is_locked"]:

            if not password:
                return "PASSWORD_REQUIRED"

            if not state.feature_lock.verify_password(password):
                return "INVALID_PASSWORD"

        return {
            "id": row["id"],
            "entry_type": row["entry_type"],
            "content": row["content"],
            "created_at": row["created_at"],
            "is_locked": row["is_locked"]
        }
    # -------------------------
    # SOFT DELETE
    # -------------------------
    def delete_entry(self, entry_id, owner):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE entries
            SET is_deleted = 1
            WHERE id = ?
            AND (user_id = ? OR anonymous_id = ?)
            """,
            (entry_id, owner, owner)
        )

        conn.commit()