from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTabWidget

from PyQt5.QtCore import QTimer

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

    def on_tab_changed(self, index):
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