from .resilience_engine import ResilienceEngine
class PracticeEngine(ResilienceEngine):
    # Practice mode does not change user_state or counts
    def run(self,state):
        self.start_breathing(state)
        self.show_comforting_message(state)
        self.show_grounding_action(state)
        self.display_ending_message()
        

    def display_ending_message(self):
        print("Well done on nourishing yourself with peace.\
            You just practiced calm. That matters.")