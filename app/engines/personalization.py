class PersonalizationEngine:

    def personalize_os(self,state):
        
        print("Display importance of breathing step, We'll always start by calming the body with breathing")
        tone_in=input("When things feel heavy, what kind of words help you most?\
            enter option(one)\
        a-Gentle and reassuring\
        b-Straightforward and grounding\
        c-Very minimal, just a few words\
        d-No preference\
        ").lower()
        
        if tone_in in state.PREFERRED_TONE_OPTIONS:
            state.preferred_tone = state.PREFERRED_TONE_OPTIONS[tone_in]
        else:
            print("Invalid option. Defaulting to 'No preference'")

        # match tone_in:
        #     case "a":state.preferred_tone["a"]
        #     case "b":state.preferred_tone["b"]
        #     case "c":state.preferred_tone["c"]
        #     case "d":state.preferred_tone["d"]

        grounding_in=input("When your mind is stuck, what helps you most? (can choose any 2)\
            a-Breathing or slowing down\
            b-Small physical movement\
            c-Sensory grounding (seeing, touching, hearing)\
            d-Just sitting quietly\
            e-I'm not sure\
                ").lower()
        grounding_opts=grounding_in.split()
        if grounding_opts[0] in state.PREFERRED_GROUNDING_OPTIONS :
            state.preferred_grounding[0]=state.PREFERRED_GROUNDING_OPTIONS[grounding_opts[0]]
        else:
            print("Invalid option. Defaulting to 'No preference'")
            
        if len(grounding_opts)>1 and grounding_in[0] in state.PREFERRED_GROUNDING_OPTIONS:
            state.preferred_grounding[1]=state.PREFERRED_GROUNDING_OPTIONS[grounding_opts[1]]
            print("Invalid option. Defaulting to 'No preference'")
        
        support_in=input("When things get hard, how should we handle support from others?\
            a-Gently remind me I'm not alone\
            b-Suggest reaching out to someone\
            c-Only if I choose\
            d-Skip this completely").lower()
        if support_in in state.SUPPORT_PREFERENCE_OPTIONS:
            state.support_preference= state.SUPPORT_PREFERENCE_OPTIONS[support_in]
        else:
            print("Invalid option. Defaulting to 'No preference'")
        # match support_in:
        #     case "a":state.support_preference="Gently remind me I'm not alone"
        #     case "b":state.support_preference="Suggest reaching out to someone"
        #     case "c":state.support_preference="Only if I choose"
        #     case "d":state.support_preference="Skip this completely"
        
        print("Your calming flow is ready.You can change this anytime.")
        state.personalized=True
        state.save()
        


