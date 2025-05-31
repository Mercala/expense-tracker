import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                            QLabel, QPushButton, QVBoxLayout, QWidget)

import warnings
from PyQt6.QtCore import pyqtRemoveInputHook
from .version import __version__

warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*sipPyTypeDict().*")


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.version = __version__
        self.init_ui()

    def init_ui(self):
        # Basic UI setup
        self.setWindowTitle(f"Expense Tracker v{self.version}")
        self.setGeometry(100, 100, 400, 300)

        # Update button
        self.update_btn = QPushButton("Check for Updates", self)
        self.update_btn.clicked.connect(self.check_updates)

        # Layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Company Expense Tracker"))
        layout.addWidget(self.update_btn)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def check_updates(self):
        # This will call your updater functionality
        from updater import check_for_updates
        check_for_updates(self.version)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())