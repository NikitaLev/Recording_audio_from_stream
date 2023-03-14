from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    Form, Window = uic.loadUiType("Recording.ui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    app.exec()