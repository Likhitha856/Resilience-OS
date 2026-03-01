import bcrypt

class FeatureLock:
    def __init__(self):
        self.lock_enabled=False
        self._hashed_pin=None
    
    # getter
    def is_enabled(self):
        return self.lock_enabled
                                          
    def set_lock(self, password:str):
        # password=input("Enter your password")
        self._hashed_pin=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.lock_enabled=True
        print("Password is successfully set") 
    
    def verify_access(self)->bool:
        
        if not self.lock_enabled:
            return True
        password=input("Enter your feature password")
        is_match=bcrypt.checkpw(password.encode('utf-8'), self._hashed_pin)
        if is_match:
            return True
        else:
            return False
    
    def reset_lock(self):
        if not self.lock_enabled:
            return
        password=input("Enter your password to confirm reset")
        if bcrypt.checkpw(password.encode("utf-8"), self._hashed_pin):
            new_pin = input("Enter new PIN: ")
            self.set_lock(new_pin)
            print("Feature lock reset.")
        else:
            print("Incorrect PIN.")
        
    def delete_lock(self):
        if not self.lock_enabled:
            return
        password=input("Enter your password to remove lock")
        if bcrypt.checkpw(password.encode("utf-8"), self._hashed_pin):
            self._hashed_pin = None
            self.lock_enabled = False
            print("Feature lock removed.")
        else:
            print("Incorrect PIN.")
        