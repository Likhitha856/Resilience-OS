
class UserSettings:
    def display(self,state):
        print("Tone:" ,state.preferred_tone)
        print("Grounding",state.preferred_grounding)
        print("Support:",state.support_preference)
        if state.personalized:
            is_reset=input("Do you want to reset settings to default?  yes/no").lower()
            if is_reset=="yes":
                self.reset(state)
        if state.feature_lock.is_enabled():
            lock_reset = input("Manage feature lock? reset/delete/skip: ").lower()
            if lock_reset == "reset":
                state.feature_lock.reset_lock()
            elif lock_reset == "delete":
                state.feature_lock.delete_lock()
                
    
    def reset(self,state):
        state.preferred_tone=state.PREFERRED_TONE_OPTIONS["a"]

        state.preferred_grounding=[state.PREFERRED_GROUNDING_OPTIONS["b"],
                                   state.PREFERRED_GROUNDING_OPTIONS["c"]]

        state.support_preference=state.SUPPORT_PREFERENCE_OPTIONS["b"]
        state.personalized = False