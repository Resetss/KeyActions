import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QListWidget

from play import EventPlayer

class PlayTab(QWidget):
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
        self.recordings_list = QListWidget()
        self.refresh_recordings_list()

        self.delay_label = QLabel("Delay (seconds):")
        self.delay_input = QSpinBox()
        self.delay_input.setMinimum(0)
        self.delay_input.setMaximum(60)

        self.intermediate_delay_label = QLabel("Delay Between Plays (seconds):")
        self.intermediate_delay_input = QSpinBox()
        self.intermediate_delay_input.setMinimum(0)
        self.intermediate_delay_input.setMaximum(3600)

        self.number_of_plays_label = QLabel("Number of plays:")
        self.number_of_plays_input = QSpinBox()
        self.number_of_plays_input.setMinimum(1)
        self.number_of_plays_input.setMaximum(100000)

        self.play_button = QPushButton("Play Recording")
        self.play_button.clicked.connect(self.play_recording)

        button_layout.addWidget(self.recordings_list)
        button_layout.addWidget(self.delay_label)
        button_layout.addWidget(self.delay_input)
        button_layout.addWidget(self.intermediate_delay_label)
        button_layout.addWidget(self.intermediate_delay_input)
        button_layout.addWidget(self.number_of_plays_label)
        button_layout.addWidget(self.number_of_plays_input)
        button_layout.addWidget(self.play_button)

        # Right column (console)
        console_layout = QVBoxLayout()

        self.play_console = QTextEdit()
        self.play_console.setReadOnly(True)

        self.clear_button = QPushButton("Clear Console")
        self.clear_button.clicked.connect(self.clear_console)

        console_layout.addWidget(self.play_console)
        console_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(console_layout)

        self.setLayout(main_layout)


    def play_recording(self):
        self.play_button.setEnabled(False)

        selected_item = self.recordings_list.currentItem()
        delay = self.delay_input.value()
        intermediate_delay = self.intermediate_delay_input.value()
        if selected_item:
            filename = selected_item.text()
            number_of_plays = self.number_of_plays_input.value()

            self.event_player = EventPlayer(filename, number_of_plays, delay, intermediate_delay, self.recordings_path)
            self.event_player.event_signal.connect(self.update_console)
            self.event_player.finished.connect(self.end_recording)
            self.event_player.start()

    def end_recording(self):
        self.play_button.setEnabled(True)

    def refresh_recordings_list(self):
        self.recordings_list.clear()
        recordings = [filename for filename in os.listdir(self.recordings_path) if filename.endswith('.json')]
        self.recordings_list.addItems(recordings)

    def update_console(self, event):
        self.play_console.append(event)

    def clear_console(self):
        self.play_console.clear()