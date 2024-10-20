from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

from settings_manager import SettingsManager
from event_manager import EventManager 

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.recordings_folder_input = QLineEdit()
        self.start_recording_input = QLineEdit()
        self.stop_recording_input = QLineEdit()
        self.start_playing_input = QLineEdit()
        self.stop_playing_input = QLineEdit()
        self.load_settings() 
        
        self.error_display = QLabel()
        self.error_display.setStyleSheet("color: red;")
        self.error_display.hide() 
 
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)

        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.clicked.connect(self.reset_settings)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(QLabel("Recordings Location:"))
        settings_layout.addWidget(self.recordings_folder_input)
        settings_layout.addWidget(QLabel("Start Recording Hotkey:"))
        settings_layout.addWidget(self.start_recording_input)
        settings_layout.addWidget(QLabel("Stop Recording Hotkey:"))
        settings_layout.addWidget(self.stop_recording_input)
        settings_layout.addWidget(QLabel("Start Playing Hotkey:"))
        settings_layout.addWidget(self.start_playing_input)
        settings_layout.addWidget(QLabel("Stop Playing Hotkey:"))
        settings_layout.addWidget(self.stop_playing_input)
        settings_layout.addWidget(self.error_display)
        settings_layout.addWidget(self.save_button)
        settings_layout.addWidget(self.reset_button)

        self.setLayout(settings_layout)

    def load_settings(self):
        recording_folder = SettingsManager.get_setting('recordings_location')
        start_recording = SettingsManager.get_setting('start_recording')
        stop_recording = SettingsManager.get_setting('stop_recording')
        start_playing = SettingsManager.get_setting('start_playing')
        stop_playing = SettingsManager.get_setting('stop_playing')

        self.recordings_folder_input.setText(recording_folder)
        self.start_recording_input.setText(str(start_recording).replace("Key.", ""))
        self.stop_recording_input.setText(str(stop_recording).replace("Key.", ""))
        self.start_playing_input.setText(str(start_playing).replace("Key.", ""))
        self.stop_playing_input.setText(str(stop_playing).replace("Key.", ""))

    def save_settings(self):
        recording_folder = self.recordings_folder_input.text()
        start_recording = self.start_recording_input.text()
        stop_recording = self.stop_recording_input.text() 
        start_playing = self.start_playing_input.text()
        stop_playing = self.stop_playing_input.text()

        if EventManager.is_special_key("Key." + start_recording):
            start_recording = "Key." + start_recording
        if EventManager.is_special_key("Key." + stop_recording):
            stop_recording = "Key." + stop_recording
        if EventManager.is_special_key("Key." + start_playing):
            start_playing = "Key." + start_playing
        if EventManager.is_special_key("Key." + stop_playing):
            stop_playing = "Key." + stop_playing

        settings = {
            'recordings_location': recording_folder,
            'start_recording': start_recording,
            'stop_recording': stop_recording,
            'start_playing': start_playing,
            'stop_playing': stop_playing
        }

        errors = SettingsManager.validate_settings(settings)
        if errors:
            self.show_errors(errors)
        else:
            self.error_display.hide() 
            SettingsManager.save_settings(settings)

    def show_errors(self, errors):
        self.error_display.setText("Error Saving Settings\n" + "\n".join(errors))
        self.error_display.show() 

    def reset_settings(self):
        SettingsManager.save_settings(SettingsManager.DEFAULT_SETTINGS)
        self.load_settings()