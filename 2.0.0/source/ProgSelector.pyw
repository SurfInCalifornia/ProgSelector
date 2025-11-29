import sys
import os
import subprocess
import ctypes
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(SCRIPT_DIR, "logo2.ico")
TASKBAR_ICON_PATH = os.path.join(SCRIPT_DIR, "logo.ico")
DNSPY_PATH = r"C:\dnSpy\dnSpy.exe"

def find_best_visual_studio():
    base_path = r"C:\Program Files\Microsoft Visual Studio"
    version_path = os.path.join(base_path, "18")
    if not os.path.exists(version_path):
        return None
    for edition in ["Enterprise", "Professional", "Community"]:
        p = os.path.join(version_path, edition, "Common7", "IDE", "devenv.exe")
        if os.path.exists(p):
            return p
    return None

VS_PATH = find_best_visual_studio()

def open_with_vs(path):
    subprocess.Popen([VS_PATH, path])
    sys.exit()

def open_with_dnspy(path):
    subprocess.Popen([DNSPY_PATH, path])
    sys.exit()

def set_taskbar_icon_for_window(win):
    hwnd = int(win.winId())
    hicon = ctypes.windll.user32.LoadImageW(0, TASKBAR_ICON_PATH, 1, 0, 0, 0x00000010)
    ctypes.windll.user32.SendMessageW(hwnd, 0x80, 1, hicon)
    ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, hicon)

class WindowsMixin:
    def showEvent(self, event):
        set_taskbar_icon_for_window(self)

class SelectionWindow(QDialog, WindowsMixin):
    def __init__(self, file_path):
        super().__init__(None, Qt.WindowType.Window)
        self.file_path = file_path
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowTitle("Choose Program")
        self.setFixedSize(450, 320)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        filename = os.path.basename(file_path)
        vs_ok = VS_PATH is not None
        dnspy_ok = os.path.exists(DNSPY_PATH)
        t = f"You are opening the library file '{filename}'.\n\n"
        if not dnspy_ok:
            t += "dnSpy is not installed at C:\\dnSpy\n\n"
        t += "Available programs:"
        label = QLabel(t)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label)
        button_height = 30
        scale_factor = 1.6
        bh = int(button_height * scale_factor)
        if vs_ok:
            b_vs = QPushButton(f"Open '{filename}' with Visual Studio 2026")
            b_vs.setFixedHeight(bh)
            b_vs.clicked.connect(lambda: open_with_vs(self.file_path))
            layout.addWidget(b_vs)
        if dnspy_ok:
            b_dn = QPushButton(f"Open '{filename}' with dnSpy")
            b_dn.setFixedHeight(bh)
            b_dn.clicked.connect(lambda: open_with_dnspy(self.file_path))
            layout.addWidget(b_dn)
        if not vs_ok and not dnspy_ok:
            label.setText(f"Cannot open '{filename}':\n- Visual Studio not installed\n- dnSpy not installed at C:\\dnSpy")
            b = QPushButton("Exit")
            b.setFixedHeight(bh)
            b.clicked.connect(self.close)
            layout.addWidget(b)
        else:
            b = QPushButton("Cancel")
            b.setFixedHeight(bh)
            b.clicked.connect(self.close)
            layout.addWidget(b)
        self.setStyleSheet(
            "QWidget {background-color:#2e2e2e;color:white;}"
            "QPushButton {background-color:#000000;color:white;border-radius:5px;}"
            "QPushButton:hover {background-color:#232323;}"
            "QPushButton:pressed {background-color:#333333;}"
        )

class UnsupportedWindow(QDialog, WindowsMixin):
    def __init__(self):
        super().__init__(None, Qt.WindowType.Window)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setWindowTitle("Unsupported File Type")
        self.setFixedSize(400, 200)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        label = QLabel("This program only supports .dll files.")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label)
        button_height = 30
        scale_factor = 1.6
        bh = int(button_height * scale_factor)
        b = QPushButton("Exit")
        b.setFixedHeight(bh)
        b.clicked.connect(self.close)
        layout.addWidget(b)
        self.setStyleSheet(
            "QWidget {background-color:#2e2e2e;color:white;}"
            "QPushButton {background-color:#000000;color:white;border-radius:5px;}"
            "QPushButton:hover {background-color:#232323;}"
            "QPushButton:pressed {background-color:#333333;}"
        )

def handle_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext != ".dll":
        w = UnsupportedWindow()
        w.exec()
        return
    w = SelectionWindow(path)
    w.exec()

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_PATH))
    if len(sys.argv) > 1:
        handle_file(sys.argv[1])
        sys.exit()
    dlg = QFileDialog(None)
    dlg.setWindowIcon(QIcon(ICON_PATH))
    dlg.setWindowTitle("Select a Dynamic Link Library")
    dlg.setNameFilters(["Dynamic Link Libraries (*.dll)"])
    dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
    dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    dlg.setWindowFlag(Qt.WindowType.Tool)
    if dlg.exec():
        file_path = dlg.selectedFiles()[0]
        handle_file(file_path)
    sys.exit()

if __name__ == "__main__":
    main()
