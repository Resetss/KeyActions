from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import QTimer
from pynput import keyboard

from settings_manager import SettingsManager

from record_tab import RecordTab
from play_tab import PlayTab
from manage_tab import ManageTab
from sequence_tab import SequenceTab
from settings_tab import SettingsTab

class LuminaActions(QWidget):
    def __init__(self):
        super().__init__()

        SettingsManager.initialize_settings()

        dimensions = SettingsManager.get_window_sizes()
        self.setWindowTitle("Lumina Actions")
        self.setGeometry(100, 100, dimensions["width"], dimensions["height"])

        # Main Layout
        layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.record_tab = RecordTab()
        self.play_tab = PlayTab()
        self.manage_tab = ManageTab()
        self.sequence_tab = SequenceTab()
        self.settings_tab = SettingsTab()

        self.tabs.addTab(self.record_tab, "Record")
        self.tabs.addTab(self.play_tab, "Play")
        self.tabs.addTab(self.manage_tab, "Manage Recordings")
        self.tabs.addTab(self.sequence_tab, "Sequences")
        self.tabs.addTab(self.settings_tab, "Settings")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.apply_dark_theme()

        debug = False
        if debug:
            self.stylesheet_timer = QTimer(self)
            self.stylesheet_timer.timeout.connect(self.apply_dark_theme)
            self.stylesheet_timer.start(1000)

        self.register_hotkeys()

    def register_hotkeys(self):
        self.start_recording_key = SettingsManager.get_setting("start_recording").lower()
        self.stop_recording_key = SettingsManager.get_setting("stop_recording").lower()        
        self.start_playing_key = SettingsManager.get_setting("start_playing").lower()
        self.stop_playing_key = SettingsManager.get_setting("stop_playing").lower()

    def register_global_hotkeys(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        current_key = str(key).replace("Key.", "")
        current_tab_index = self.tabs.currentIndex()
        current_tab_name = self.tabs.tabText(current_tab_index)

        if current_tab_name == "Play":
            if current_key == self.start_playing_key:
                self.play_tab.play_recording()
            elif current_key == self.stop_playing_key:
                self.play_tab.stop_playing()
        
        if current_tab_name == "Record":
            if current_key == self.stop_recording_key:
                self.record_tab.stop_recording()

    def on_release(self, key):        
        current_key = str(key).replace("Key.", "")
        current_tab_index = self.tabs.currentIndex()
        current_tab_name = self.tabs.tabText(current_tab_index)

        if current_tab_name == "Record":
            if current_key == self.start_recording_key:
                self.record_tab.start_recording()

    def on_tab_changed(self, index):
        self.register_global_hotkeys()

        if self.tabs.tabText(index) == "Play":
            self.play_tab.refresh_recordings_list()
        elif self.tabs.tabText(index) == "Manage Recordings":
            self.manage_tab.refresh_recordings_list()

    def apply_dark_theme(self):
        with open('styles/dark.css', 'r') as file:
            dark_stylesheet = file.read()
        self.setStyleSheet(dark_stylesheet)

    def closeEvent(self, event):
        window_size = self.size()
        SettingsManager.set_setting('last_window_size', {"width": window_size.width(), "height": window_size.height()})
        super().closeEvent(event)
