from PyQt5.QtCore import QThread, pyqtSignal
import re
import os


class ScriptProcessor(QThread):
    progress = pyqtSignal(int)
    completed = pyqtSignal(str)
    stopped = pyqtSignal()

    def __init__(self, scripts, save_path):
        super().__init__()
        self.scripts = scripts
        self.save_path = save_path
        self.is_running = True

    def run(self):
        total_files = len(self.scripts)
        for i, script in enumerate(self.scripts):
            if not self.is_running:
                self.stopped.emit()
                return
            self.process_script(script)
            self.progress.emit(int((i+1) / total_files * 100))
        self.completed.emit("All scripts processed successfully!")

    def process_script(self, script):
        try:
            with open(script, 'r') as file:
                content = file.readlines()
            new_content = []
            for line in content:

                # Remove any part of the line that has a comment (starting with #)
                clean_line = re.sub(r'#.*', '', line).rstrip()
                # Preserve new lines to keep structure
                if clean_line.strip() or line.strip() == "":
                    new_content.append(clean_line + '\n')

            # Save to the new path
            filename = os.path.basename(script)
            save_file_path = os.path.join(self.save_path, filename)
            with open(save_file_path, 'w') as new_file:
                new_file.writelines(new_content)
        except Exception as e:
            print(f"Error processing {script}: {e}")

    def stop(self):
        self.is_running = False