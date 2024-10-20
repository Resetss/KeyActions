import sys

from key_actions import KeyActions
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    key_actions = KeyActions()
    key_actions.show()
    sys.exit(app.exec_())