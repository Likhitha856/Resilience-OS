from .resilience_engine import ResilienceEngine
class DefaultOS(ResilienceEngine):
    
    def run(self,state):
        '''
        state: AppState Object
        runs the os, breath,calm,grounding 
        returns: user answer(yes/no) about state 
        '''
        if state.user_state=="DISTRESSED":
            state.default_use_count+=1
        self.start_breathing(state)
        self.show_comforting_message(state)
        self.show_grounding_action(state)
        answer=input("Do you feel a bit more okay now?: yes/no").lower()
        return answer

