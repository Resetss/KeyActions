import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit

from event_recorder import EventRecorder
from settings_manager import SettingsManager

class RecordTab(QWidget):
    def __init__(self):
        super().__init__()

        self.recordings_path = SettingsManager.get_recordings_folder() 

        self.name_input = QLineEdit()

        self.error_label = QLabel("Name cannot be blank!")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide() 

        self.record_all_checkbox = QCheckBox("Record Mouse Movement")
        
        initial_delay = SettingsManager.get_setting("initial_delay")
        self.initial_delay_input = QSpinBox()
        self.initial_delay_input.setMinimum(initial_delay["start"])
        self.initial_delay_input.setMaximum(initial_delay["end"])

        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        left_column_layout = QVBoxLayout()
        left_column_layout.addWidget(QLabel("Name of recording:"))
        left_column_layout.addWidget(self.name_input)
        left_column_layout.addWidget(self.error_label)
        left_column_layout.addWidget(self.record_all_checkbox)
        left_column_layout.addWidget(QLabel("Delay (seconds):"))
        left_column_layout.addWidget(self.initial_delay_input)
        left_column_layout.addWidget(self.start_button)
        left_column_layout.addWidget(self.stop_button)

        self.record_console = QTextEdit()
        self.record_console.setReadOnly(True)

        self.clear_button = QPushButton("Clear Console")
        self.clear_button.clicked.connect(self.clear_console)

        right_column_layout = QVBoxLayout()
        right_column_layout.addWidget(self.record_console)
        right_column_layout.addWidget(self.clear_button)

        record_layout = QHBoxLayout()
        record_layout.addLayout(left_column_layout)
        record_layout.addLayout(right_column_layout)

        self.setLayout(record_layout)

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.error_label.hide()

        name_of_recording = self.name_input.text()
        record_all = self.record_all_checkbox.isChecked()
        inital_delay = self.initial_delay_input.value()

        if name_of_recording == "":
            self.end_recording()
            self.error_label.show()
            return

        self.event_listener = EventRecorder(name_of_recording, record_all, inital_delay, self.recordings_path)
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