import os
import json

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTabWidget

from PyQt5.QtCore import QTimer

from record_tab import RecordTab
from play_tab import PlayTab
from manage_tab import ManageTab
from dev_notes import DevNotes

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lumina Actions")
        self.setGeometry(100, 100, 600, 400)

        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        appdata_path = os.path.join(documents_path, 'LuminaAction')
        self.recordings_path = os.path.join(appdata_path, 'recordings')
        self.settings_path = os.path.join(appdata_path, 'settings.json')

        # Ensure directories exist
        os.makedirs(self.recordings_path, exist_ok=True)
        if not os.path.exists(self.settings_path):
            with open(self.settings_path, 'w') as f:
                json.dump({}, f)

        layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.record_tab = RecordTab()
        self.play_tab = PlayTab()
        self.manage_tab = ManageTab()
        self.dev_notes = DevNotes()

        self.tabs.addTab(self.record_tab, "Record")
        self.tabs.addTab(self.play_tab, "Play")
        self.tabs.addTab(self.manage_tab, "Manage Recordings")
        self.tabs.addTab(self.dev_notes, "Dev Notes")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.apply_dark_theme()

        debug = False 
        if debug: 
            self.stylesheet_timer = QTimer(self)
            self.stylesheet_timer.timeout.connect(self.apply_dark_theme)
            self.stylesheet_timer.start(1000)

    def on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Play":
            self.play_tab.refresh_recordings_list()
        if self.tabs.tabText(index) == "Manage Recordings":
            self.manage_tab.refresh_recordings_list()
            
    def apply_dark_theme(self):
        print("Applied")
        with open('styles/dark.css', 'r') as file:
            dark_stylesheet = file.read()
        self.setStyleSheet(dark_stylesheet)
