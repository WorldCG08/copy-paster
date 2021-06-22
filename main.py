import os
import sqlite3
import threading
import sys
from datetime import date
import time
import pyclip
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('pyclip.ui', self)

        self.hidden = True  #Hide clips at the start

        if os.path.exists('.' + os.sep + 'copypaste.db'):
            self.connection = sqlite3.connect('copypaste.db')
        else:
            self.connection = sqlite3.connect('copypaste.db')
            self.connection.cursor().execute('''CREATE TABLE clips (id INTEGER	constraint clips_pk primary key autoincrement,
             clip text, created text)''')

        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()

        self.cliplist = self.cursor.execute("select clip from clips").fetchall()
        self.cliplist_widget = self.findChild(QtWidgets.QListWidget, 'clip_list')
        self.cliplist_widget.addItems(self.cliplist)

        x = threading.Thread(target=self.clip_listener)
        x.start()
        # self.sh_btn = self.findChild(QtWidgets.QPushButton, 'show_hide_btn')
        # self.sh_btn.setText('Text Changed2')
        # self.sh_btn.clicked.connect(self.sh_btn_pressed)
        # self.line_text = self.findChild(QtWidgets.QLineEdit, 'line_text')
        # self.line_text.setText('Oppapapa')
        self.show()

    def sh_btn_pressed(self):
        self.line_text.setText('miyagi')
        print(self.line_text.text())

    def clip_listener(self):
        connection = sqlite3.connect('copypaste.db')
        cursor = connection.cursor()
        while True:
            time.sleep(1)
            clip = pyclip.paste().decode().strip("'").replace("'", "''")  # text will have the content of clipboard
            if clip not in self.cliplist:
                td = date.today()
                cursor.execute(f"INSERT INTO clips (clip, created) VALUES ('{clip}','{td}')")
                connection.commit()
                self.cliplist.append(clip)
                self.cliplist_widget.insertItem(0, clip)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_()
