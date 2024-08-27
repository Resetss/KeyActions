# PlayTab class
import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox, QTextEdit, QListWidget
from PyQt5.QtCore import Qt

from event_player import EventPlayer
from settings_manager import SettingsManager


class PlayTab(QWidget):
    def __init__(self):
        super().__init__()

        self.recordings_path = SettingsManager.get_recordings_folder()

        self.recordings_list = QListWidget()
        self.refresh_recordings_list()

        initial_delay = SettingsManager.get_setting("initial_delay")
        self.delay_input = QSpinBox()
        self.delay_input.setMinimum(initial_delay["start"])
        self.delay_input.setMaximum(initial_delay["end"])

        intermediate_delay = SettingsManager.get_setting("intermediate_delay")
        self.intermediate_delay_input = QSpinBox()
        self.intermediate_delay_input.setMinimum(intermediate_delay["start"])
        self.intermediate_delay_input.setMaximum(intermediate_delay["end"])

        number_of_plays = SettingsManager.get_setting("number_of_plays")
        self.number_of_plays_input = QSpinBox()
        self.number_of_plays_input.setMinimum(number_of_plays["start"])
        self.number_of_plays_input.setMaximum(number_of_plays["end"])

        self.play_button = QPushButton("Play Recording")
        self.play_button.clicked.connect(self.play_recording)

        left_column_layout = QVBoxLayout()
        left_column_layout.addWidget(self.recordings_list)
        left_column_layout.addWidget(QLabel("Delay (seconds):"))
        left_column_layout.addWidget(self.delay_input)
        left_column_layout.addWidget(QLabel("Delay Between Plays (seconds):"))
        left_column_layout.addWidget(self.intermediate_delay_input)
        left_column_layout.addWidget(QLabel("Number of plays:"))
        left_column_layout.addWidget(self.number_of_plays_input)
        left_column_layout.addWidget(self.play_button)

        self.play_console = QTextEdit()
        self.play_console.setReadOnly(True)

        self.clear_button = QPushButton("Clear Console")
        self.clear_button.clicked.connect(self.clear_console)

        right_column_layout = QVBoxLayout()
        right_column_layout.addWidget(self.play_console)
        right_column_layout.addWidget(self.clear_button)

        play_tab_layout = QHBoxLayout()
        play_tab_layout.addLayout(left_column_layout)
        play_tab_layout.addLayout(right_column_layout)

        self.setLayout(play_tab_layout)

        self.playing = False 

    def play_recording(self):
        self.play_button.setEnabled(False)
        self.playing = True 

        selected_item = self.recordings_list.currentItem()

        if selected_item:
            recordings_list = [selected_item.text()]
            number_of_plays = self.number_of_plays_input.value()
            inital_delay = self.delay_input.value()
            intermediate_delay = self.intermediate_delay_input.value()

            self.event_player = EventPlayer(recordings_list, number_of_plays, inital_delay, intermediate_delay, self.recordings_path)
            self.event_player.event_signal.connect(self.update_console)
            self.event_player.finished.connect(self.play_ended)
            self.event_player.start()

    def play_ended(self):
        self.play_button.setEnabled(True)
        self.playing = False 

    def stop_playing(self):
        self.event_player.stop()
        self.playing = False 

    def refresh_recordings_list(self):
        self.recordings_list.clear()
        self.recordings_path = SettingsManager.get_recordings_folder()
        recordings = [filename for filename in os.listdir(self.recordings_path) if filename.endswith('.json')]
        self.recordings_list.addItems(recordings)

    def update_console(self, event):
        self.play_console.append(event)

    def clear_console(self):
        self.play_console.clear()