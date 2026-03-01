from engines.feature_lock import FeatureLock
class AppState:
    
    PREFERRED_TONE_OPTIONS = {
    "a": "Gentle and reassuring",
    "b": "Straightforward and grounding",
    "c": "Very minimal, just a few words",
    "d": "No preference"
    }
    PREFERRED_GROUNDING_OPTIONS={
    "a": "Breathing or slowing down",
    "b": "Small physical movement",
    "c": "Sensory grounding (seeing, touching, hearing)",
    "d": "Just sitting quietly",
    "e": "I'm not sure"
}
    SUPPORT_PREFERENCE_OPTIONS = {
    "a": "Gently remind me I'm not alone",
    "b": "Suggest reaching out to someone",
    "c": "Only if I choose",
    "d": "Skip this completely"
    }
    
    
    def __init__(self):
        self.user_state=None
        self.default_use_count=0
        self.prompt_shown=False
        self.personalized=False
        self.preferred_tone=AppState.PREFERRED_TONE_OPTIONS["a"]

        self.preferred_grounding=[AppState.PREFERRED_GROUNDING_OPTIONS["b"],AppState.PREFERRED_GROUNDING_OPTIONS["c"]]

        self.feature_lock=FeatureLock()
        self.lock_needed=True
        self.support_preference=AppState.SUPPORT_PREFERENCE_OPTIONS["b"]