import bcrypt


class FeatureLock:
    def __init__(self):
        self.lock_enabled = False
        self._hashed_pin = None

    # -------------------------
    # getter
    # -------------------------
    def is_enabled(self):
        return self.lock_enabled

    # -------------------------
    # set lock
    # -------------------------
    def set_lock(self, password: str):
        self._hashed_pin = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.lock_enabled = True

    # -------------------------
    # verify password
    # -------------------------
    def verify_access(self, password: str) -> bool:

        if not self.lock_enabled:
            return True

        return bcrypt.checkpw(password.encode("utf-8"), self._hashed_pin)

    # -------------------------
    # reset password
    # -------------------------
    def reset_lock(self, old_password: str, new_password: str):

        if not self.lock_enabled:
            return False

        if bcrypt.checkpw(old_password.encode("utf-8"), self._hashed_pin):
            self.set_lock(new_password)
            return True

        return False

    # -------------------------
    # remove lock
    # -------------------------
    def delete_lock(self, password: str):

        if not self.lock_enabled:
            return False

        if bcrypt.checkpw(password.encode("utf-8"), self._hashed_pin):
            self._hashed_pin = None
            self.lock_enabled = False
            return True

        return False