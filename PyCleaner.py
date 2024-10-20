import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarkstyle
from core.CleanThread import ScriptProcessor

class PyCleaner(QWidget):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.save_path = ""

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PyCleaner v1.0")
        self.setGeometry(300, 300, 600, 400)
        self.setWindowIcon(QIcon('icon.png'))

        layout = QVBoxLayout()

        # Display selected scripts
        self.script_list = QListWidget()
        self.script_list.setAcceptDrops(True)
        self.script_list.setDragDropMode(QListWidget.InternalMove) 
        layout.addWidget(self.script_list)

        # Select Path button
        path_layout = QHBoxLayout()
        self.path_label = QLabel("Select path to save cleaned scripts :")
        self.select_path_button = QPushButton("Select Path")
        self.select_path_button.clicked.connect(self.select_save_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.select_path_button)
        layout.addLayout(path_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_cleaning)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_cleaning)
        self.select_button = QPushButton("Select Scripts")
        self.select_button.clicked.connect(self.select_scripts)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.select_button)
        layout.addLayout(button_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # About Developer
        self.about_label = QLabel("Developed by: Sihab Sahariar | sihabsahariarcse@gmail.com", alignment=Qt.AlignRight)
        layout.addWidget(self.about_label)

        self.setLayout(layout)

    def select_scripts(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Python Scripts", "", "Python Files (*.py)")
        if files:
            self.scripts = files
            self.script_list.addItems(files)

    def select_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.save_path:
            self.path_label.setText(f"Save Path: {self.save_path}")

    def start_cleaning(self):
        if not self.scripts:
            QMessageBox.warning(self, "No Scripts", "Please select scripts to clean!")
            return
        if not self.save_path:
            QMessageBox.warning(self, "No Save Path", "Please select a save path!")
            return

        self.progress_bar.setValue(0)
        self.script_processor = ScriptProcessor(self.scripts, self.save_path)
        self.script_processor.progress.connect(self.update_progress)
        self.script_processor.completed.connect(self.processing_completed)
        self.script_processor.stopped.connect(self.processing_stopped)
        self.script_processor.start()

    def stop_cleaning(self):
        if hasattr(self, 'script_processor') and self.script_processor.isRunning():
            self.script_processor.stop()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def processing_completed(self, message):
        QMessageBox.information(self, "Completed", message)

    def processing_stopped(self):
        QMessageBox.warning(self, "Stopped", "Script processing was stopped!")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.endswith('.py'):
                self.scripts.append(file_path)
                self.script_list.addItem(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = PyCleaner()
    window.show()
    sys.exit(app.exec_())
