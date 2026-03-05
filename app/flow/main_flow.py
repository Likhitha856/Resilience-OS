'''MainFlow is ONLY a traffic controller.
It should:
ask questions
route to engines
receive return signals

never do:
saving
locking
password handling
content handling'''
from app.engines.default_os import DefaultOS
from app.engines.rumination import RuminationEngine
from app.engines.file_content_manager import FileContentManager
from app.engines.personalization import PersonalizationEngine
from app.engines.reflection import ReflectionEngine
from app.engines.vent import VentEngine
from app.engines.practice import PracticeEngine
from app.engines.social_support import SocialSupport
from app.engines.user_settings import UserSettings

class MainFlow:
    def __init__(self, state):
        self.state = state
        self.default_os = DefaultOS()
        self.rumination = RuminationEngine()
        self.personalization = PersonalizationEngine()
        self.file_manager=FileContentManager(state.db)
        self.reflection = ReflectionEngine(self.file_manager)
        self.vent = VentEngine(self.file_manager)
        self.practice = PracticeEngine()
        self.social_support = SocialSupport()
        self.user_settings=UserSettings()

    def start_app(self):
        loop = True

        # ---- personalization prompt (shown only once) ----
        if not self.state.prompt_shown and self.state.default_use_count >= 1:
                user_in = input(
                    "Would you like to personalize the calming flow you used earlier? yes/no\n"
                ).lower()
                if user_in == "yes":
                    self.personalization.personalize_os(self.state)
                self.state.prompt_shown = True
                self.state.save()
                

        # ---- main loop ----
        while loop:
            user_in = input(
                "Are you going through a hard moment right now?: yes/no\n"
            ).lower()

            if user_in == "quit":
                loop = False
                continue

            # -------- DISTRESSED FLOW --------
            if user_in == "yes":
                self.state.user_state = "DISTRESSED"

                answer = self.default_os.run(self.state)
                user_needs = self.handle_check_stable(answer)

                while True:
                    if user_needs == "RUN_POST_STABLE_ENGINE":
                        intent = self.run_post_stable_engine()

                        if intent == "a":
                            self.vent.run_vent_board(self.state)
                        elif intent == "b":
                            self.social_support.reach_out()

                        break  # return to main loop

                    elif user_needs == "NEEDS_RUMINATION":
                        user_state = self.rumination.run_rumination_engine(self.state)
                        user_needs = self.post_rumination_decision(user_state)

                        if user_needs == "GO_TO_APP_SCREEN":
                            break
                        elif user_needs == "RUN_POST_STABLE_ENGINE":
                            intent = self.run_post_stable_engine()

                            if intent == "a":
                                self.vent.run_vent_board(self.state)
                            elif intent == "b":
                                self.social_support.reach_out()

                            break
                        elif user_needs == "RETRY_DEFAULT_OS":
                            answer = self.default_os.run(self.state)
                            user_needs = self.handle_check_stable(answer)

            # -------- OK FLOW --------
            else:
                self.state.user_state = "OK"

                choice = self.app_default_screen()

                match choice:
                    case "a":
                        answer = self.default_os.run(self.state)
                        self.handle_check_stable(answer)
                    case "b":
                        self.practice.run(self.state)
                    case "c":
                        self.reflection.run_reflection_board(self.state)
                    case "d":
                        self.vent.run_vent_board(self.state)
                    case "e":
                        self.personalization.personalize_os(self.state)
                    case "f":
                        self.user_settings.display(self.state)
                    case "g":
                        self.view_saved("reflection")
                    case "h":
                        self.view_saved("vent")   
                    case _:
                        self.exit_app()

    # -------- decision helpers --------

    def handle_check_stable(self, answer):
        if answer == "yes":
            self.state.user_state = "OK"
            self.state.save()
            return "RUN_POST_STABLE_ENGINE"
        else:
            return "NEEDS_RUMINATION"

    def post_rumination_decision(self, user_state):
        if user_state is None:
            return "GO_TO_APP_SCREEN"
        if user_state.user_state == "OK":
            return "RUN_POST_STABLE_ENGINE"
        else:
            return "RETRY_DEFAULT_OS"

    # -------- screens / menus --------

    def app_default_screen(self):
        print(self.state.default_use_count)
        print(self.state.user_state)

        return input(
            "The default app screen. choose\n"
            "a-Run resilience os\n"
            "b-practice mode\n"
            "c-reflection board\n"
            "d-vent board\n"
            "e-personalize OS\n"
            "f-User settings\n"
            "g-view saved reflections\n"
            "h-view saved vents\n"
        ).lower()

    def run_post_stable_engine(self):
        return input(
            "choose one of the below options:\n"
            "a-Vent it out\n"
            "b-Reach out / Social support\n"
        ).lower()

# -------- 🆕 VIEW SAVED CONTENT FLOW --------

    def view_saved(self, entry_type):
        """
        MainFlow responsibility:
        - ask intent
        - route to manager via engine
        - never handle content or locks
        """
        if entry_type == "reflection":
            manager = self.reflection.file_manager
        else:
            manager = self.vent.file_manager

        entries = manager.display_entries(entry_type)

        if not entries:
            print("No saved entries found.")
            return

        print("Saved entries:")
        for entry in entries:
            print(f"{entry['id']} - {entry['created_at']}")

        try:
            entry_id = int(input("Enter the ID to open (or 0 to cancel): "))
        except ValueError:
            return

        if entry_id == 0:
            return

        entry = manager.open_entry(entry_id, self.state)
        if entry:
            print("-----")
            print(entry["content"])
            print("-----")
    # -------- misc --------

    def exit_app(self):
        self.state.db.close()
        self.display_ending_message()

    def display_ending_message(self):
        print("a comforting message when exit")

