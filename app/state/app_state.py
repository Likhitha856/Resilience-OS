import json
from app.engines.feature_lock import FeatureLock


class AppState:

    # --------------------------
    # Static Option Dictionaries
    # --------------------------

    PREFERRED_TONE_OPTIONS = {
        "a": "Gentle and reassuring",
        "b": "Straightforward and grounding",
        "c": "Very minimal, just a few words",
        "d": "No preference"
    }

    PREFERRED_GROUNDING_OPTIONS = {
        "a": "Breathing or slowing down",
        "b": "Small physical movement",
        "c": "Sensory grounding (seeing, touching, hearing)",
        "d": "Just sitting quietly",
        "e": "I'm not sure"
    }

    SUPPORT_PREFERENCE_OPTIONS = {
        "a": "Gently remind me I'm not alone",
        "b": "Suggest reaching out to someone",
        "c": "Only if I choose",
        "d": "Skip this completely"
    }

    # --------------------------
    # Initialization
    # --------------------------

    def __init__(self, db):
        self.db = db
        self.conn = db.get_connection()

        # Session-only state (not persisted)
        self.user_state = None

        # Runtime lock wrapper
        self.feature_lock = FeatureLock()

        self._ensure_row_exists()
        self._load_state()

    # --------------------------
    # Ensure default DB row exists
    # --------------------------

    def _ensure_row_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM app_state")
        result = cursor.fetchone()

        if result["count"] == 0:
            cursor.execute("""
                INSERT INTO app_state (
                    id,
                    preferred_tone,
                    preferred_grounding,
                    support_preference,
                    default_use_count,
                    prompt_shown,
                    lock_enabled,
                    lock_hash
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                1,
                self.PREFERRED_TONE_OPTIONS["a"],
                json.dumps([
                    self.PREFERRED_GROUNDING_OPTIONS["b"],
                    self.PREFERRED_GROUNDING_OPTIONS["c"]
                ]),
                self.SUPPORT_PREFERENCE_OPTIONS["b"],
                0,
                0,
                0,
                None
            ))
            self.conn.commit()

    # --------------------------
    # Load persisted state
    # --------------------------

    def _load_state(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM app_state WHERE id = 1")
        row = cursor.fetchone()

        self.default_use_count = row["default_use_count"]
        self.prompt_shown = bool(row["prompt_shown"])
        self.personalized = bool(row["personalized"])
        self.preferred_tone = row["preferred_tone"]
        self.preferred_grounding = json.loads(row["preferred_grounding"])
        self.support_preference = row["support_preference"]

        # Restore feature lock state
        self.feature_lock.lock_enabled = bool(row["lock_enabled"])
        self.feature_lock._hashed_pin = (
            row["lock_hash"].encode("utf-8")
            if row["lock_hash"]
            else None
        )

    # --------------------------
    # Persist changes
    # --------------------------

    def save(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE app_state
            SET preferred_tone = ?,
                preferred_grounding = ?,
                support_preference = ?,
                default_use_count = ?,
                prompt_shown = ?,
                personalized = ?,
                lock_enabled = ?,
                lock_hash = ?
            WHERE id = 1
        """, (
            self.preferred_tone,
            json.dumps(self.preferred_grounding),
            self.support_preference,
            self.default_use_count,
            int(self.prompt_shown),
            int(self.personalized),
            int(self.feature_lock.lock_enabled),
            self.feature_lock._hashed_pin.decode("utf-8")
            if self.feature_lock._hashed_pin
            else None
        ))
        self.conn.commit()