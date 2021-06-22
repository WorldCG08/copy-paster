from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('pyclip.ui', self) # Load the .ui file

        self.sh_btn = self.findChild(QtWidgets.QPushButton, 'show_hide_btn')
        self.sh_btn.setText('Text Changed2')
        self.sh_btn.clicked.connect(self.sh_btn_pressed)
        self.line_text = self.findChild(QtWidgets.QLineEdit, 'line_text')
        self.line_text.setText('Oppapapa')
        self.show() # Show the GUI

    def sh_btn_pressed(self):
        self.line_text.setText('miyagi')
        print(self.line_text.text())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_()
