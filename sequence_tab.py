import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QListWidget

class SequenceTab(QWidget):
    def __init__(self):
        super().__init__()

        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        appdata_path = os.path.join(documents_path, 'LuminaAction')
        self.recordings_path = os.path.join(appdata_path, 'recordings')

        main_layout = QHBoxLayout()

        button_layout = QVBoxLayout()
        self.recordings_list = QListWidget()

        self.refresh_recordings_list()
        
        self.add_delay = QPushButton("Add Delay")
        self.add_delay_label = QLabel("Delay (seconds):")
        self.add_delay_input = QSpinBox()
        self.add_delay_input.setMinimum(0)
        self.add_delay_input.setMaximum(60)
        
        
        button_layout.addWidget(self.recordings_list)
        button_layout.addWidget(self.add_delay_label)
        button_layout.addWidget(self.add_delay_input)
        button_layout.addWidget(self.add_delay)
    

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)


    def refresh_recordings_list(self):
        self.recordings_list.clear()
        recordings = [filename for filename in os.listdir(self.recordings_path) if filename.endswith('.json')]
        self.recordings_list.addItems(recordings)