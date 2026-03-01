import time
USER_STATE=None
HAS_USED_DEFAULT_WHEN_DISTRESSED = False
PREFERRED_TONE="gentle and reassuring"
PREFERRED_GROUNDING_OPTIONS={
    "a": "Breathing or slowing down",
    "b": "Small physical movement",
    "c": "Sensory grounding (seeing, touching, hearing)",
    "d": "Just sitting quietly",
    "e": "I'm not sure"
}

PREFERRED_GROUNDING=[PREFERRED_GROUNDING_OPTIONS["b"],PREFERRED_GROUNDING_OPTIONS["c"]]
SUPPORT_PREFERENCE="Suggest reaching out to someone"
def start_app(user_in):
    global USER_STATE
    user_in=input("Are you going through a hard moment right now?: yes/no").lower()
    if user_in=="yes":
        USER_STATE="DISTRESSED"
        default_os()
    else:
        USER_STATE="OK"
        app_default_screen()

def exit_app():
    # app_default_screen()
    display_ending_message()
    
def display_ending_message():
    print("a comforting message when exit")
        
def app_default_screen(user_in):
    global HAS_USED_DEFAULT_WHEN_DISTRESSED, USER_STATE
    if HAS_USED_DEFAULT_WHEN_DISTRESSED:
        if USER_STATE=="OK":
            user_in=input("Would you like to personalize the calming flow you used earlier? yes/no").lower()
            if user_in=="yes":
                personalize_os()
    user_in=input("The deafult app screen. choose \
        a-Run default os\
        b-practice mode\
        c-reflection board\
        d-vent board\
        e-personalize OS\
        f-User settings")
    match user_in:
        case "a":default_os()
        case "b":run_practice_mode()
        case "c":run_reflection_board()
        case "d":run_vent_board()
        case "e":personalize_os()
        case "f":user_settings()
        case "_":exit_app()

def run_practice_mode():
    pass

def run_personalized_os():
    pass
def user_settings():
    pass      
def default_os(user_in):
    if USER_STATE=="DISTRESSED":
        HAS_USED_DEFAULT_WHEN_DISTRESSED = True
    start_breathing()
    show_comforting_message()
    show_grounding_action()
    user_in=input("Do you feel a bit more okay now?: yes/no").lower()
    handle_check_stable(user_in)

# default os functions
def start_breathing():
    pass

def show_comforting_message():
    pass

def show_grounding_action():
    pass

def handle_check_stable(user_in):
    if user_in=="yes":
        run_post_stable_engine()
    else:
        run_rumination_engine()
#-----------------------------------    
def personalize_os():
    global PREFERRED_TONE,PREFERRED_GROUNDING
    print("Display importance of breathing step, We’ll always start by calming the body with breathing")
    tone_in=input("When things feel heavy, what kind of words help you most?\
        Options (tap one)\
	a-Gentle and reassuring\
	b-Straightforward and grounding\
	c-Very minimal, just a few words\
    d-No preference\
    e-Skip")
    match tone_in:
        case "a":PREFERRED_TONE="gentle and reassuring"
        case "b":PREFERRED_TONE="Straightforward and grounding"
        case "c":PREFERRED_TONE="Very minimal, just a few words"
        case "d":PREFERRED_TONE="gentle and reassuring"
        case "e":PREFERRED_TONE="gentle and reassuring"
    grounding_in=input("When your mind is stuck, what helps you most?\
        a-Breathing or slowing down\
        b-Small physical movement\
        c-Sensory grounding (seeing, touching, hearing)\
        d-Just sitting quietly\
        e-I’m not sure\
            ").lower()
    grounding_opts=grounding_in.split()
    PREFERRED_GROUNDING[0]=PREFERRED_GROUNDING_OPTIONS[grounding_opts[0]]
    if len(grounding_opts)>1:
        PREFERRED_GROUNDING[1]=PREFERRED_GROUNDING_OPTIONS[grounding_opts[1]]
    
    support_in=input("When things get hard, how should we handle support from others?\
        a-“Gently remind me I'm not alone”\
        b-“Suggest reaching out to someone”\
        c-“Only if I choose”\
        d-“Skip this completely”")
    match support_in:
        case "a":"Gently remind me I'm not alone"
        case "b":"Suggest reaching out to someone"
        case "c":"Only if I choose"
        case "d":"Skip this completely"
    
    print("Your calming flow is ready.You can change this anytime.")
    app_default_screen()
            
    

def run_rumination_engine():
    start_90_sec_animation()
    choose_sensory_interruption()
    choose_physical_micro_action()
    user_in=input("Do you feel a bit more okay now? yes/no").lower()
    if user_in=="yes":
        run_post_stable_engine()
    else:
        user_in=input("Would you like to run the calming flow again? yes/no").lower()
        if user_in=="yes":
            default_os()
        else:
            exit_app()

#rumination engine functions 
def start_90_sec_animation():
    pass

def choose_sensory_interruption():
    pass

def choose_physical_micro_action():
    pass
#-------------------------------------
def run_post_stable_engine():
    value=input("choose one of the below options:\
                a-Vent it out\
                b-Reach out / Social support\
                c-Continue with app\
                d-Exit").lower()
    match value:
        case "a":
            run_vent_board()
        case "b":
            reach_out()
        case "c":
            app_default_screen()
        case "d":
            exit_app()
        case "_":
            exit_app()

def run_vent_board(voice_rec=False):
    # opens blank notepad like by defualt 
    open_writing_pad()
    # if user selects the option to voice rec
    if voice_rec==True:
        record_voice()
    # no time limit
    user_in=input("Would you like us to remember a small part of this to support you later? yes/no").lower()
    if user_in=="yes":
        save_doc()
        extract_content()
        store_context_tag()
    else:
        delete_doc()
    
#vent_board functions      
def reach_out():
    pass
def open_writing_pad():
    pass
def record_voice():
    pass
def save_doc():
    pass
def delete_doc():
    pass
def extract_content():
    pass
def store_context_tag():
    pass

def run_reflection_board(voice_rec=False):
    # opens blank notepad like by defualt 
    open_writing_pad()
    # if user selects the option to voice rec
    if voice_rec==True:
        record_voice()
    # no time limit
    user_in=input("Would you like to save this file to revisit later? yes/no").lower()
    if user_in=="yes":
        save_doc()
        extract_content()
        store_context_tag()
    else:
        delete_doc()


    