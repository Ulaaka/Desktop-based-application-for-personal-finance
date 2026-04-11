
import sys
from PyQt5.QtCore import pyqtSignal, QObject

# custom class for capturing print outputs
class Stream(QObject):
    input_text = pyqtSignal(str)

    def write(self, text):
        self.input_text.emit(text)

    def flush(self):
        sys.stdout.flush()