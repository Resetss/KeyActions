import os
import json

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit

from record import EventRecorder

class RecordTab(QWidget):
    def __init__(self):
        super().__init__()

        # TODO Move hardcodded recording path as a parameter connected 
        # with settings tab
        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        appdata_path = os.path.join(documents_path, 'LuminaAction')
        self.recordings_path = os.path.join(appdata_path, 'recordings')

        main_layout = QHBoxLayout()

        # Left column (buttons)
        button_layout = QVBoxLayout()
        self.name_label = QLabel("Name of recording:")
        self.name_input = QLineEdit()

        self.error_label = QLabel("Name cannot be blank!")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide() 

        self.record_all_checkbox = QCheckBox("Record Mouse Movement")

        self.delay_label = QLabel("Delay (seconds):")
        self.delay_input = QSpinBox()
        self.delay_input.setMinimum(0)
        self.delay_input.setMaximum(60)

        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        button_layout.addWidget(self.name_label)
        button_layout.addWidget(self.name_input)
        button_layout.addWidget(self.error_label)
        button_layout.addWidget(self.record_all_checkbox)
        button_layout.addWidget(self.delay_label)
        button_layout.addWidget(self.delay_input)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # Right column (console)
        console_layout = QVBoxLayout()

        self.record_console = QTextEdit()
        self.record_console.setReadOnly(True)

        self.clear_button = QPushButton("Clear Console")
        self.clear_button.clicked.connect(self.clear_console)

        console_layout.addWidget(self.record_console)
        console_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(console_layout)

        self.setLayout(main_layout)

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.error_label.hide()

        name_of_recording = self.name_input.text()
        record_all = self.record_all_checkbox.isChecked()
        delay = self.delay_input.value()

        if name_of_recording == "":
            self.end_recording()
            self.error_label.show()
            return

        self.event_listener = EventRecorder(name_of_recording, record_all, delay, self.recordings_path)
        self.event_listener.event_signal.connect(self.update_console)
        self.event_listener.finished.connect(self.end_recording)
        self.event_listener.start()

    def end_recording(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def stop_recording(self):
        self.event_listener.stop()

    def update_console(self, event):
        self.record_console.append(event)

    def clear_console(self):
        self.record_console.clear()