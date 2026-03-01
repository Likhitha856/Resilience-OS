from .board import Board
from .file_content_manager import FileContentManager
class ReflectionEngine:

    def __init__(self):
        super().__init__()
        self.board=Board()
        self.file_manager=FileContentManager()

    def run_reflection_board(self,state,mode="write"):
        # opens blank notepad like by defualt 
        self.board.open_pad()
        # if user selects the option to voice rec
        if mode=="voice":
            self.board.record_voice()
        # no time limit
        content = input("Write your reflection here:\n")

        save = input("Would you like to save this reflection? yes/no: ").lower()
        if save != "yes":
            print("Reflection discarded.")
            return

        if not state.feature_lock.is_enabled():
            ask_lock = input(
                "Would you like to protect saved reflections with a lock? yes/no: "
            ).lower()
            if ask_lock == "yes":
                pin = input("Set a PIN: ")
                state.feature_lock.set_lock(pin)

        self.file_manager.save_entry(
            content=content,
            entry_type="reflection",
            is_locked=state.feature_lock.is_enabled()
        )

        print("Reflection saved.")
