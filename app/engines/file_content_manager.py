from datetime import datetime
from .saved_entry import SavedEntry
'''(MANAGES COLLECTION, not UI)'''
class FileContentManager:
    def __init__(self):
        self._storage=[] # replace with SQLite later
        self._id_counter=1
        
    def save_entry(self,content,entry_type,is_locked):
        entry=SavedEntry(
            entry_id=self._id_counter,
            entry_type=entry_type,
            content=content,
            is_locked=is_locked,
            created_at=datetime.now()
        )
        self._storage.append(entry)
        self._id_counter+=1
    
    def open_entry(self,entry_id,state) :
        for entry in self._storage:
            if entry.id == entry_id:
                if entry.is_locked:
                    if not state.feature_lock.verify_access():
                        print("Access denied.")
                        return None
                return entry
        return None
          
    

    def display_entries(self,entry_type):
        return [e for e in self._storage if e.type==entry_type]

    
    def delete_entry(self,entry_id):
        self._storage=[e for e in self._storage if e.id!=entry_id]
    # def extract_content(self):
    #     print("extracting content")
        
    # def store_context_tag(self):
    #     print("store context tag")
            