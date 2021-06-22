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
        self.is_filter = 2

        if os.path.exists('.' + os.sep + 'copypaste.db'):
            self.connection = sqlite3.connect('copypaste.db')
        else:
            self.connection = sqlite3.connect('copypaste.db')
            self.connection.cursor().execute('''CREATE TABLE clips (id INTEGER	constraint clips_pk primary key autoincrement,
             clip text, created text)''')

        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()

        self.cliplist = self.cliplist_today = self.clipQuery()
        self.cliplist_widget = self.findChild(QtWidgets.QListWidget, 'clip_list')
        self.clipwidget_reload()

        self.calendar_widget = self.findChild(QtWidgets.QCalendarWidget, 'calendar')
        self.calendar_widget.clicked.connect(self.date_changed)

        self.filter_box = self.findChild(QtWidgets.QCheckBox, 'filter_checkbox')
        self.filter_box.clicked.connect(self.filter_box_switch)

        self.del_btn = self.findChild(QtWidgets.QPushButton, 'del_btn')
        self.del_btn.clicked.connect(self.delete_clip)

        x = threading.Thread(target=self.clip_listener)
        x.start()

        self.show()

    def date_changed(self):
        self.now = self.calendar_widget.selectedDate().toString('yyyy-MM-dd')
        self.clipwidget_reload()

    def filter_box_switch(self):
        self.is_filter = self.filter_box.checkState()
        self.clipwidget_reload()

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

    def clipwidget_reload(self):
        self.cliplist = self.clipQuery()
        self.cliplist_widget.clear()
        self.cliplist_widget.addItems(self.cliplist)

    def clipQuery(self):
        if self.is_filter == 2:
            return self.cursor.execute("select clip from clips where created = :now", {'now': self.now}).fetchall()
        else:
            return self.cursor.execute("select clip from clips").fetchall()

    def delete_clip(self):
        listItems = self.cliplist_widget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.cursor.execute(f"DELETE FROM clips WHERE clip = '{item.text()}'")
            self.connection.commit()
            print(item.text())
            self.cliplist_widget.takeItem(self.cliplist_widget.row(item))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    window = Ui()  # Create an instance of our class
    app.exec_()
