from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from settings_manager import SettingsManager

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.recordings_folder_input = QLineEdit()
        self.recordings_folder_input.setText(SettingsManager.get_setting('recordings_location'))
        self.start_recording_input = QLineEdit()
        self.start_recording_input.setText(SettingsManager.get_setting('start_recording'))
        self.stop_recording_input = QLineEdit()
        self.stop_recording_input.setText(SettingsManager.get_setting('stop_recording'))
        self.start_playing_input = QLineEdit()
        self.start_playing_input.setText(SettingsManager.get_setting('start_playing'))
        self.stop_playing_input = QLineEdit()
        self.stop_playing_input.setText(SettingsManager.get_setting('stop_playing'))
        
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
        settings_layout.addWidget(self.save_button)
        settings_layout.addWidget(self.reset_button)

        self.setLayout(settings_layout)

    def save_settings(self):
        SettingsManager.set_setting('recordings_location', self.recordings_folder_input.text())
        SettingsManager.set_setting('start_recording', self.start_recording_input.text())
        SettingsManager.set_setting('stop_recording', self.stop_recording_input.text())
        SettingsManager.set_setting('start_playing', self.start_playing_input.text())
        SettingsManager.set_setting('stop_playing', self.stop_playing_input.text())
        
    def reset_settings(self):
        SettingsManager.save_settings(SettingsManager.DEFAULT_SETTINGS)
        self.load_settings()

    def load_settings(self):
        self.recordings_folder_input.setText(SettingsManager.get_setting('recordings_location'))
        self.start_recording_input.setText(SettingsManager.get_setting('start_recording'))
        self.stop_recording_input.setText(SettingsManager.get_setting('stop_recording'))
        self.start_playing_input.setText(SettingsManager.get_setting('start_playing'))
        self.stop_playing_input.setText(SettingsManager.get_setting('stop_playing'))
