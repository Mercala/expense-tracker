import requests
import os
import sys
import tempfile
import zipfile
import shutil
from PyQt6.QtWidgets import (QMessageBox, QProgressDialog, 
                            QApplication)
from PyQt6.QtCore import Qt, QCoreApplication, QTimer


def check_for_updates(current_version, parent_window=None):
    repo = "Mercala/expense-tracker"
    # api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    api_url = f"https://api.github.com/repos/{repo}/tags"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            latest_data = response.json()
            # latest_version = latest_data['tag_name'].lstrip('v')
            latest_version = latest_data[0]['name'].lstrip('v')

            if latest_version != current_version:
                msg = QMessageBox(parent=parent_window)
                msg.setWindowTitle("Update Available")
                msg.setText(f"Version {latest_version} is available!\nUpdate now?")
                msg.setStandardButtons(
                    QMessageBox.StandardButton.Yes | 
                    QMessageBox.StandardButton.No
                )

                if msg.exec() == QMessageBox.StandardButton.Yes:
                    return download_update(latest_data, parent_window)

            else:
                QMessageBox.information(parent_window, "No Updates", "You're running the latest version!")

    except Exception as e:
        QMessageBox.warning(parent_window, "Update Error", f"Could not check for updates: {str(e)}")


def download_update(release_data, parent_window):
    try:
        # Setup progress dialog (indeterminate since we don't have content-length)
        progress = QProgressDialog("Downloading update...", "Cancel", 0, 0, parent_window)
        progress.setWindowTitle("Updating")
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setMinimumDuration(0)
        progress.show()
        QCoreApplication.processEvents()

        # Download setup
        zip_url = release_data['zipball_url']
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, "update.zip")
        
        # Download with chunked encoding
        response = requests.get(zip_url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if progress.wasCanceled():
                    shutil.rmtree(temp_dir)
                    return False
                f.write(chunk)
                QCoreApplication.processEvents()

        # Extract update
        progress.setLabelText("Installing update...")
        extracted_dir = None
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])

        # Copy files to application directory (platform independent)
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for item in os.listdir(extracted_dir):
            src = os.path.join(extracted_dir, item)
            dst = os.path.join(app_dir, item)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        # Cleanup
        shutil.rmtree(temp_dir)

        # Schedule restart
        progress.close()
        QMessageBox.information(parent_window, "Update Complete", 
            "Update installed successfully!\nApplication will restart now.")
        
        QTimer.singleShot(1000, restart_application)
        return True

    except Exception as e:
        QMessageBox.critical(parent_window, "Update Failed", 
            f"Update failed: {str(e)}")
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
        return False

def restart_application():
    """Restarts the current application"""
    python = sys.executable
    os.execl(python, python, *sys.argv)


#  End!