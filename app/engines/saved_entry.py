'''(represents ONE saved item)'''
class SavedEntry:
    def __init__(self, entry_id, entry_type, content, is_locked, created_at):
        self.id = entry_id
        self.type = entry_type  # "vent" or "reflection"
        self.content = content
        self.is_locked = is_locked
        self.created_at = created_at

    def display(self):
        print("-----")
        print(self.content)
        print("-----")