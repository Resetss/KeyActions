import os
import json

class SettingsManager:
    SETTINGS_FILE_PATH = os.path.join(os.path.expanduser('~'), 'Documents', 'LuminaAction', 'settings.json')
    RECORDINGS_FILE_PATH = os.path.join(os.path.expanduser('~'), 'Documents', 'LuminaAction', 'recordings')
    
    START_RECORDING = "F9"
    STOP_RECORDING = "F10"
    START_PLAYING = "F11"
    STOP_PLAYING = "F12"

    INITIAL_DELAY = {"start": 0, "end": 60}
    INTERMEDIATE_DELAY = {"start": 0, "end": 300}

    NUMBER_OF_PLAYS = {"start": 1, "end": 100} 

    DEFAULT_WINDOW_SIZE = {"width": 600, "height": 400}

    DEFAULT_SETTINGS = {
        "recordings_location": RECORDINGS_FILE_PATH,
        "start_recording": START_RECORDING,
        "stop_recording": STOP_RECORDING,
        "start_playing": START_PLAYING,
        "stop_playing": STOP_PLAYING,
        "initial_delay": INITIAL_DELAY,
        "intermediate_delay": INTERMEDIATE_DELAY, 
        "number_of_plays": NUMBER_OF_PLAYS,
        "last_window_size": DEFAULT_WINDOW_SIZE  
    }

    @classmethod
    def initialize_settings(cls):
        """Initialize the settings file if it doesn't exist."""
        if not os.path.exists(cls.SETTINGS_FILE_PATH):
            os.makedirs(os.path.dirname(cls.SETTINGS_FILE_PATH), exist_ok=True)
            cls.save_settings(cls.DEFAULT_SETTINGS)
        else:
            # Ensure all default settings are present
            settings = cls.load_settings()
            for key, value in cls.DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
            cls.save_settings(settings)

    @classmethod
    def load_settings(cls):
        """Load settings from the JSON file."""
        if os.path.exists(cls.SETTINGS_FILE_PATH):
            with open(cls.SETTINGS_FILE_PATH, 'r') as f:
                return json.load(f)
        return cls.DEFAULT_SETTINGS

    @classmethod
    def save_settings(cls, settings):
        """Save settings to the JSON file."""
        with open(cls.SETTINGS_FILE_PATH, 'w') as f:
            json.dump(settings, f, indent=4)

    @classmethod
    def get_setting(cls, key):
        """Get a specific setting by key."""
        settings = cls.load_settings()
        return settings.get(key, cls.DEFAULT_SETTINGS.get(key))

    @classmethod
    def set_setting(cls, key, value):
        """Set a specific setting and save it."""
        settings = cls.load_settings()
        settings[key] = value
        cls.save_settings(settings)

    @classmethod
    def get_window_sizes(cls):
        return cls.get_setting("last_window_size")

    @classmethod
    def get_recordings_folder(cls):
        """Get the recordings folder path."""
        return cls.get_setting('recordings_location')