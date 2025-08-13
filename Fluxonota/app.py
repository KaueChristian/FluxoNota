from PySide6.QtWidgets import QApplication
from Fluxonota.main_window import MainWindow

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()