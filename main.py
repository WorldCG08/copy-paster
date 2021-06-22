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

        self.hidden = True
        self.now = date.today()
        self.is_filter = True

        if os.path.exists('.' + os.sep + 'copypaste.db'):
            self.connection = sqlite3.connect('copypaste.db')
        else:
            self.connection = sqlite3.connect('copypaste.db')
            self.connection.cursor().execute('''CREATE TABLE clips (id INTEGER	constraint clips_pk primary key autoincrement,
             clip text, created text)''')

        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()

        self.cliplist = self.cliplist_today = self.cursor.execute("select clip from clips where created = :now", {'now': self.now}).fetchall()
        self.cliplist_widget = self.findChild(QtWidgets.QListWidget, 'clip_list')
        self.cliplist_widget.addItems(self.cliplist)

        self.calendar_widget = self.findChild(QtWidgets.QCalendarWidget, 'calendar')
        self.calendar_widget.clicked.connect(self.date_changed)

        x = threading.Thread(target=self.clip_listener)
        x.start()

        self.show()

    def date_changed(self):
        self.now = self.calendar_widget.selectedDate().toString('yyyy-MM-dd')
        self.cliplist = self.cursor.execute("select clip from clips where created = :now", {'now': self.now}).fetchall()
        self.cliplist_widget.clear()
        self.cliplist_widget.addItems(self.cliplist)

    def clip_listener(self):
        connection = sqlite3.connect('copypaste.db')
        cursor = connection.cursor()
        while True:
            time.sleep(1)
            clip = pyclip.paste().decode().strip("'").replace("'", "''")  # text will have the content of clipboard
            if clip not in self.cliplist_today:
                cursor.execute(f"INSERT INTO clips (clip, created) VALUES ('{clip}','{self.now}')")
                connection.commit()
                if self.now == date.today():
                    self.cliplist_today.append(clip)
                    self.cliplist_widget.insertItem(0, clip)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_()
