import sys
import shutil
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Applications": [".exe", ".msi", ".dmg", ".iso"]
}

TEMP_EXTENSIONS = {".tmp", ".crdownload", ".part"}

ROSE_PINE_STYLE = """
    QWidget {
        background-color: #191724;
        color: #e0def4;
        font-family: 'Segoe UI', sans-serif;
    }
    QLabel#title {
        font-size: 15px;
        font-weight: 700;
        color: #ebbcba;
        letter-spacing: 1px;
    }
    QLineEdit {
        background-color: #1f1d2e;
        border: 1px solid #26233a;
        border-radius: 8px;
        padding: 6px 10px;
        color: #e0def4;
        font-size: 12px;
    }
    QLineEdit:focus {
        border: 1px solid #c4a7e7;
    }
    QPushButton {
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
    }
    QPushButton#browse_btn {
        background-color: #26233a;
        color: #9ccfd8;
        border: 1px solid #31748f;
        padding: 6px 12px;
    }
    QPushButton#browse_btn:hover {
        background-color: #31748f;
        color: #e0def4;
    }
    QPushButton#start_btn {
        background-color: #ebbcba;
        color: #191724;
        border: none;
        padding: 8px;
        font-size: 13px;
        font-weight: 700;
    }
    QPushButton#start_btn:hover {
        background-color: #f6c177;
    }
    QPushButton#start_btn:pressed {
        background-color: #eb6f92;
    }
    QCheckBox {
        color: #9ccfd8;
        font-size: 11px;
        spacing: 5px;
    }
    QCheckBox::indicator {
        width: 14px;
        height: 14px;
        border-radius: 4px;
        border: 1px solid #31748f;
        background-color: #1f1d2e;
    }
    QCheckBox::indicator:checked {
        background-color: #ebbcba;
        border: 1px solid #ebbcba;
    }
    QTextEdit {
        background-color: #1f1d2e;
        border: 1px solid #26233a;
        border-radius: 8px;
        padding: 8px;
        color: #9ccfd8;
        font-family: 'Consolas', 'Fira Code', monospace;
        font-size: 11px;
    }
"""

def generate_rosepine_icon() -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setBrush(QColor("#1f1d2e"))
    painter.setPen(QColor("#ebbcba"))
    painter.drawRoundedRect(3, 3, 58, 58, 16, 16)

    painter.setPen(QColor("#ebbcba"))
    font = QFont("Segoe UI", 26)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "✿")
    painter.end()

    return QIcon(pixmap)

def get_file_hash(filepath: Path) -> str:
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

class HavenOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Haven")
        self.setFixedSize(420, 360)
        self.setWindowIcon(generate_rosepine_icon())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Header
        title_label = QLabel("✿ HAVEN // FILE SANCTUARY")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Folder Row
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(8)

        self.entry_path = QLineEdit()
        self.entry_path.setText(str(Path.home() / "Downloads"))
        self.entry_path.setPlaceholderText("Select directory...")
        folder_layout.addWidget(self.entry_path)

        btn_browse = QPushButton("Browse")
        btn_browse.setObjectName("browse_btn")
        btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse.clicked.connect(self.browse_folder)
        folder_layout.addWidget(btn_browse)

        layout.addLayout(folder_layout)

        # Feature Checkboxes
        options_layout = QHBoxLayout()
        
        self.chk_duplicates = QCheckBox("Detect Duplicates")
        self.chk_clean_empty = QCheckBox("Purge Empty Folders")

        self.chk_duplicates.setChecked(True)
        self.chk_clean_empty.setChecked(True)

        options_layout.addWidget(self.chk_duplicates)
        options_layout.addWidget(self.chk_clean_empty)

        layout.addLayout(options_layout)

        # Action Button
        self.btn_start = QPushButton("✧ Organise Space")
        self.btn_start.setObjectName("start_btn")
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.setFixedHeight(36)
        self.btn_start.clicked.connect(self.run_sorting)
        layout.addWidget(self.btn_start)

        # Log Terminal
        self.textbox_log = QTextEdit()
        self.textbox_log.setReadOnly(True)
        layout.addWidget(self.textbox_log)

        self.log("Ready to tidy up your space.")

    def browse_folder(self):
        selected = QFileDialog.getExistingDirectory(self, "Select Folder")
        if selected:
            self.entry_path.setText(selected)

    def log(self, text: str):
        self.textbox_log.append(f"• {text}")

    def run_sorting(self):
        folder_path = Path(self.entry_path.text())
        if not folder_path.exists():
            self.log(f"Error: Path '{folder_path}' not found.")
            return

        check_duplicates = self.chk_duplicates.isChecked()
        clean_empty = self.chk_clean_empty.isChecked()

        self.log(f"Cleaning directory: {folder_path.name}...")

        temp_max_age_days = 7
        processed_count = 0
        seen_hashes = {}

        # 1. Processing files
        for item in list(folder_path.iterdir()):
            if item.is_dir():
                continue

            # Temp Cleanup
            if item.suffix.lower() in TEMP_EXTENSIONS:
                file_age = datetime.now() - datetime.fromtimestamp(item.stat().st_mtime)
                if file_age > timedelta(days=temp_max_age_days):
                    item.unlink()
                    self.log(f"Purged temp: {item.name}")
                    processed_count += 1
                continue

            # Duplicate Detection
            if check_duplicates and item.stat().st_size > 0:
                f_hash = get_file_hash(item)
                if f_hash in seen_hashes:
                    dup_dir = folder_path / "Duplicates"
                    dup_dir.mkdir(exist_ok=True)
                    shutil.move(str(item), str(dup_dir / item.name))
                    self.log(f"Duplicate found: {item.name} ➔ Duplicates/")
                    processed_count += 1
                    continue
                else:
                    seen_hashes[f_hash] = item

            # Screenshot Renaming
            if "screenshot" in item.name.lower() or "скриншот" in item.name.lower():
                mod_time = datetime.fromtimestamp(item.stat().st_mtime)
                new_filename = f"Screenshot_{mod_time.strftime('%Y-%m-%d_%H%M%S')}{item.suffix}"
                target_path = folder_path / new_filename
                
                if not target_path.exists() and item != target_path:
                    item = item.rename(target_path)
                    self.log(f"Renamed: {new_filename}")
                    processed_count += 1

            # Categorization
            target_category = "Other"
            for category, extensions in CATEGORIES.items():
                if item.suffix.lower() in extensions:
                    target_category = category
                    break

            dest_dir = folder_path / target_category
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_dir / item.name))
            self.log(f"Moved: {item.name} ➔ {target_category}/")
            processed_count += 1

        # 2. Clean Empty Subfolders
        if clean_empty:
            for sub_dir in list(folder_path.iterdir()):
                if sub_dir.is_dir() and not any(sub_dir.iterdir()):
                    sub_dir.rmdir()
                    self.log(f"Removed empty folder: {sub_dir.name}/")

        self.log(f"Done. Processed {processed_count} items.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(ROSE_PINE_STYLE)
    window = HavenOrganizerApp()
    window.show()
    sys.exit(app.exec())