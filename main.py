import sys

import time

from lumina_actions import LuminaActions
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    lumina_actions = LuminaActions()
    lumina_actions.show()
    sys.exit(app.exec_())