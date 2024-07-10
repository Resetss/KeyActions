import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMessageBox

class ManageTab(QWidget):
    def __init__(self):
        super().__init__()

        documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        appdata_path = os.path.join(documents_path, 'LuminaAction')
        self.recordings_path = os.path.join(appdata_path, 'recordings')

        layout = QVBoxLayout()

        self.recordings_list = QListWidget()

        self.delete_button = QPushButton("Delete Selected Recording")
        self.delete_button.clicked.connect(self.delete_selected_recording)

        layout.addWidget(self.recordings_list)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def refresh_recordings_list(self):
        self.recordings_list.clear()
        recordings = [filename for filename in os.listdir(self.recordings_path) if filename.endswith('.json')]
        self.recordings_list.addItems(recordings)

    def delete_selected_recording(self):
        selected_item = self.recordings_list.currentItem()
        if selected_item:
            filename = selected_item.text()
            filepath = os.path.join(self.recordings_path, filename)
            try:
                os.remove(filepath)
                self.refresh_recordings_list()
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Failed to delete recording:\n{e}")
