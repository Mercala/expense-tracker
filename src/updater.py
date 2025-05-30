import requests
import json
import os
import sys
import subprocess
from PyQt6.QtWidgets import QMessageBox


def check_for_updates(current_version):
    repo = "mercala/expense-tracker"
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            latest_data = response.json()
            latest_version = latest_data['tag_name']

            if latest_version != current_version:
                # Ask user if they want to update
                msg = QMessageBox()
                msg.setWindowTitle("Update Available")
                msg.setText(f"Version {latest_version} is available!\nUpdate now?")
                msg.setStandardButton(QMessageBox.Yes | QMessageBox.No)
                if msg.exec_() == QMessageBox.Yes:
                    return download_update(lastest_data)

            else:
                QMessageBox.information(None, "No Updates", "You're running the latest version!")

    except Exception as e:
        QMessageBox.warning(None, "Update Error", f"Could not check for updates: {str(e)}")


def download_update(release_data):
    # TODO: Implement download logic
    pass