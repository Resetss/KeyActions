import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QSpinBox

from settings_manager import SettingsManager

class SequenceTab(QWidget):
    def __init__(self):
        super().__init__()

        self.recordings_path = SettingsManager.get_recordings_folder()

        self.recordings_list = QListWidget()
        self.refresh_recordings_list()

        self.sequence_display = QListWidget()

        initial_delay = SettingsManager.get_setting("initial_delay")
        self.delay_input = QSpinBox()
        self.delay_input.setMinimum(initial_delay["start"])
        self.delay_input.setMaximum(initial_delay["end"])

        self.sequence_name_input = QLineEdit()
        self.sequence_name_input.setPlaceholderText("Enter sequence name")

        self.add_recording_button = QPushButton("Add Recording")
        self.add_recording_button.clicked.connect(self.add_recording_to_sequence)

        self.add_delay_button = QPushButton("Add Delay")
        self.add_delay_button.clicked.connect(self.add_delay_to_sequence)

        self.remove_item_button = QPushButton("Remove Selected")
        self.remove_item_button.clicked.connect(self.remove_selected_item)

        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)

        left_column_layout = QVBoxLayout()
        left_column_layout.addWidget(self.recordings_list)
        left_column_layout.addWidget(self.add_recording_button)
        left_column_layout.addWidget(QLabel("Delay (seconds):"))
        left_column_layout.addWidget(self.delay_input)
        left_column_layout.addWidget(self.add_delay_button)
        left_column_layout.addWidget(self.remove_item_button)

        right_column_layout = QVBoxLayout()
        right_column_layout.addWidget(self.sequence_display)
        right_column_layout.addWidget(self.sequence_name_input)
        right_column_layout.addWidget(self.save_sequence_button)

        sequence_tab_layout = QHBoxLayout()
        sequence_tab_layout.addLayout(left_column_layout)
        sequence_tab_layout.addLayout(right_column_layout)

        self.setLayout(sequence_tab_layout)

        self.sequence = []

    def refresh_recordings_list(self):
        """Refresh the list of available recordings."""
        self.recordings_list.clear()
        self.recordings_path = SettingsManager.get_recordings_folder()
        recordings = [filename for filename in os.listdir(self.recordings_path) if filename.endswith('.rec')]
        self.recordings_list.addItems(recordings)

    def add_recording_to_sequence(self):
        """Add the selected recording to the sequence."""
        selected_item = self.recordings_list.currentItem()
        if selected_item:
            recording_name = selected_item.text()
            index = self.get_selected_sequence_index()
            if index is None:
                self.sequence.append(('file', recording_name))
            else:
                self.sequence.insert(index + 1, ('file', recording_name))
            self.update_sequence_display()

    def add_delay_to_sequence(self):
        """Add a delay to the sequence."""
        delay_text = self.delay_input.text()
        if delay_text.isdigit():
            delay = int(delay_text)
            index = self.get_selected_sequence_index()
            if index is None:
                self.sequence.append(('delay', delay))
            else:
                self.sequence.insert(index + 1, ('delay', delay))
            self.update_sequence_display()
        else:
            self.delay_input.setText("")

    def remove_selected_item(self):
        """Remove the selected item from the sequence."""
        index = self.get_selected_sequence_index()
        if index is not None:
            del self.sequence[index]
            self.update_sequence_display()

    def get_selected_sequence_index(self):
        """Get the index of the selected item in the sequence."""
        selected_item = self.sequence_display.currentItem()
        if selected_item:
            return self.sequence_display.row(selected_item)
        return None

    def update_sequence_display(self):
        """Update the sequence display to show the current sequence."""
        self.sequence_display.clear()
        for item in self.sequence:
            if item[0] == 'file':
                self.sequence_display.addItem(f"Recording: {item[1]}")
            elif item[0] == 'delay':
                self.sequence_display.addItem(f"Delay: {item[1]} seconds")

    def save_sequence(self):
        """Save the current sequence to a .seq file."""
        sequence_name = self.sequence_name_input.text()
        if sequence_name:
            sequence_data = [{'type': item[0], 'filename': item[1]} if item[0] == 'file' else {'type': 'delay', 'delay': item[1]} for item in self.sequence]
            
            save_path = os.path.join(self.recordings_path, f"{sequence_name}.seq")
            with open(save_path, 'w') as seq_file:
                json.dump(sequence_data, seq_file, indent=4)
            self.sequence_display.addItem(f"Sequence saved as {sequence_name}.seq")
        else:
            self.sequence_name_input.setPlaceholderText("Please enter a sequence name")  # Prompt user for a name if not provided
