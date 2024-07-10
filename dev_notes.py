from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel

class DevNotes(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Currently, pressing Esc terminates both the record and play processes."))
        
        layout.addWidget(QLabel("This application serializes data files under Documents/LuminaActions."))
    
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel(""))

        self.setLayout(layout)
