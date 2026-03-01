class RuminationEngine():

    def run_rumination_engine(self,state):
        ''' state: AppState object
            returns: user state property'''
        self.start_90_sec_pause()
        self.sensory_interruption()
        self.physical_action()
        user_in=input("Do you feel a bit more okay now? yes/no").lower()
        # print(user_in)
        if user_in=="yes":
            state.user_state="OK"
            # run_post_stable_engine()
            return state
            
        else:
            user_in=input("Would you like to run the calming flow again? yes/no\n").lower()
            # print(user_in)
            if user_in=="yes":
                # default_os()
                state.user_state="DISTRESSED"
                return state
                
            else:
                # app_defualt_screen
                return None
                

#rumination engine functions 
    def start_90_sec_pause(self):
        print("90 sec pause")
        pass

    def sensory_interruption(self):
        print("sensory interruption")
        pass

    def physical_action(self):
        print("physical action")
        pass