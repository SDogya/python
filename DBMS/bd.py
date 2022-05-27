import random
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2  # ого библеотека с компьютерным зрением, но зачем она автору?
import os
import pygame  # ого еще и библиотека игрового движка! зачем же?


def total_error():
    cv2.imshow('ОШИБОЧКА', cv2.imread(os.path.join("errors", "error.png")))
    pygame.mixer.init()
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() / 12)
    pygame.mixer.music.load(os.path.join("errors", "error.mp3"))
    pygame.mixer.music.play()

    cv2.waitKey(1000)  # правильно чтоб картинку загрузить и издать звук ......thats all folks!
    # почему автор не реализовал это с помощью pyqt ? автору лень
    cv2.destroyAllWindows()
    pygame.mixer.quit()




Masks = {"TEXT": "",
         "DATA": "99.99.9999;_",
         "INTEGER": "9999999999"
         }


class MainWindow(QMainWindow):
    resized = pyqtSignal()

    def s(self):
        pass

    def __init__(self):
        super(MainWindow, self).__init__()
        self.cur_db_name = ""
        self.cur_tb_name = ""
        self.cur_info = ""

        self.MainWindow()
        self.setFixedSize(720, 480)
        self.tools = QToolBar()
        self.cursor: sqlite3.connect("").cursor
        self.con: sqlite3.connect
        self.init_menu()

    def MainWindow(self):
        try:
            self.removeToolBar(self.tools)
        except:
            pass
        label = QLabel(self)
        pixmap = QPixmap(os.path.join("errors", "beer2.png"))

        label.setPixmap(pixmap)
        self.setCentralWidget(label)

    def init_menu(self):
        menu = self.menuBar().addMenu("&File")
        act = QAction("Create db", self)
        act.triggered.connect(self.create_db)
        menu.addAction(act)
        act = QAction("Choose db", self)
        act.triggered.connect(self.choose_db)
        menu.addAction(act)

    def init_toolbar(self, ik):
        try:
            self.removeToolBar(self.tools)  # лень писать нормальное условие
        except:
            pass

        self.tools = QToolBar()
        self.addToolBar(self.tools)
        self.tools.setMovable(False)

        def call_console(self):
            text, ok = QInputDialog.getText(self, 'PseudoConsole', 'Enter sqltie command:')
            if ok:
                try:
                    self.cursor.execute(text)
                    self.con.commit()
                except:
                    total_error()

        button_action = QAction("Console", self)
        button_action.triggered.connect(lambda:call_console(self))
        self.tools.addAction(button_action)

        if ik == 0:  # in db
            button_action = QAction("go back", self)
            button_action.triggered.connect(self.MainWindow)
            self.tools.addAction(button_action)

            button_action = QAction("Create table", self)
            button_action.triggered.connect(self.create_table)
            self.tools.addAction(button_action)

        if ik == 1:  # in table
            button_action = QAction("go main", self)
            button_action.triggered.connect(self.MainWindow)
            self.tools.addAction(button_action)

            button_action = QAction("go back", self)
            button_action.triggered.connect(self.Choose_table_Area)
            self.tools.addAction(button_action)

            button_action = QAction("edit choosen one", self)
            button_action.triggered.connect(self.get_pk)
            self.tools.addAction(button_action)

            button_action = QAction("Create new one", self)
            button_action.triggered.connect(self.create_line)
            self.tools.addAction(button_action)

            button_action = QAction("Delete old ones", self)
            button_action.triggered.connect(self.del_line)
            self.tools.addAction(button_action)

        self.addToolBar(self.tools)

    def get_pk(self):
        if len(self.table.selectionModel().selectedIndexes()) == 0:
            total_error()  # хоть где то его использую
            return
        cell_index = self.table.selectionModel().selectedIndexes()[0].row()

        self.window2 = QWidget()

        names = [i[1] for i in self.cur_info]
        self.window2.show()
        vlay = QVBoxLayout()
        hlay1 = QHBoxLayout()
        lines = []
        for j, i in enumerate(names):
            vlayinhlay = QVBoxLayout()
            vlayinhlay.addWidget(QLabel(str(i)))
            x = QLineEdit(self.table.item(cell_index, j).text(), )
            vlayinhlay.addWidget(x, alignment=(Qt.AlignVCenter | Qt.AlignTop))
            lines.append(x)
            hlay1.addLayout(vlayinhlay)

        hlay2 = QHBoxLayout()
        vlay.addLayout(hlay1)
        vlay.addLayout(hlay2)

        save = QPushButton("save")
        cancel = QPushButton("cancel")
        hlay2.addWidget(save)
        hlay2.addWidget(cancel)

        def save_this(self):
            for i, o in enumerate(lines):
                t_name = self.cur_tb_name[0]
                col_name = self.cur_info[i][1]
                ids = self.cur_info[0][1]
                idn = self.table.item(cell_index, 0).text()
                try:
                    self.cursor.execute(f"""Update {t_name} set {col_name} = "{o.text()}" where {ids} = {idn}""")
                   
                    self.choose_table(self.cur_tb_name)
                    self.window2.close()
                except:
                    total_error()

        save.clicked.connect(lambda: save_this(self))
        cancel.clicked.connect(lambda: self.window2.close())

        self.window2.setLayout(vlay)

    def create_db(self):
        filename, _ = QFileDialog.getSaveFileName(filter="*.db")
        if filename:
            with open(filename, "w") as f:
                pass
            self.cursor = sqlite3.connect(filename).cursor()

            self.cur_db_name = filename
            self.Choose_table_Area()

    def choose_db(self):
        def db_select(self):
            fname = QFileDialog.getOpenFileName(
                self, 'Choose your database', filter='*.db'
            )[0]
            return fname

        selected_db = db_select(self)
        if len(selected_db) != 0:
            self.con = sqlite3.connect(selected_db)
            self.cursor = self.con.cursor()
            self.cur_db_name = selected_db
            self.Choose_table_Area()

    def choose_table(self, name):

        self.cur_tb_name = name
        self.init_toolbar(1)
        self.widgeg = QWidget()

        self.vbox = QVBoxLayout()
        self.widgeg.setLayout(self.vbox)

        self.cursor.execute(f"SELECT * FROM {name[0]};")
        mass = self.cursor.fetchall()

        self.cursor.execute(f"pragma table_info('{name[0]}');")
        info = self.cursor.fetchall()

        self.cur_info = info

        table = QTableWidget()
        self.table = table

        table.setHorizontalScrollBar(QScrollBar(self))
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        table.setColumnCount(len(info))
        table.setRowCount(len(mass))

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setHorizontalHeaderLabels([i[1] for i in info])

        # table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, o in enumerate(mass):
            for j, k in enumerate(o):
                table.setItem(i, j, QTableWidgetItem(str(k)))

        self.table.resizeColumnsToContents()
        self.vbox.addWidget(table)
        self.setCentralWidget(self.widgeg)

    def create_line(self):
        self.window2 = QWidget()

        names = [i[1] for i in self.cur_info]
        self.window2.show()
        vlay = QVBoxLayout()
        hlay1 = QHBoxLayout()
        lines = []

        for j, i in enumerate(names):
            vlayinhlay = QVBoxLayout()
            vlayinhlay.addWidget(QLabel(str(i)))
            x = QLineEdit()
            if self.cur_info[j][2] in Masks:
                x.setInputMask(Masks[self.cur_info[j][2]])
            vlayinhlay.addWidget(x, alignment=(Qt.AlignVCenter | Qt.AlignTop))
            lines.append(x)
            hlay1.addLayout(vlayinhlay)

        hlay2 = QHBoxLayout()
        vlay.addLayout(hlay1)
        vlay.addLayout(hlay2)

        save = QPushButton("save")
        cancel = QPushButton("cancel")
        hlay2.addWidget(save)
        hlay2.addWidget(cancel)

        def save_this(self):
            command = F"INSERT INTO {self.cur_tb_name[0]} ("
            for i in self.cur_info:
                command += f"{i[1]},"
            command = command[:-1] + ") VALUES("
            for i in lines:
                command += f"'{i.text()}',"
            command = command[:-1] + ")"
            try:
                self.cursor.execute(command)
                self.con.commit()
                self.choose_table(self.cur_tb_name)
                self.window2.close()

            except:
                total_error()

        save.clicked.connect(lambda: save_this(self))
        cancel.clicked.connect(lambda: self.window2.close())

        self.window2.setLayout(vlay)

    def del_line(self):
        indexes = self.table.selectionModel().selectedIndexes()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("You realy want delete this?????")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            for i in indexes:
                idn = f"DELETE FROM {self.cur_tb_name[0]} WHERE {self.cur_info[0][1]} = {self.table.item(i.row(), 0).text()};"

                self.cursor.execute(idn)
                self.con.commit()
                self.choose_table(self.cur_tb_name)

    def del_table(self, name):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("I have a question!")
        dlg.setText("You realy want delete this?????")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            self.cursor.execute(f"DROP TABLE {name}")
            self.con.commit()
        self.Choose_table_Area()

    def Choose_table_Area(self):
        self.widgeg = QWidget()
        self.init_toolbar(0)
        self.vbox = QVBoxLayout()
        self.widgeg.setLayout(self.vbox)

        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
        n = self.cursor.fetchall()

        table = QTableWidget()
        table.setHorizontalScrollBar(QScrollBar(self))
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        table.setColumnCount(5)
        m = []
        for i in n:
            if i[0] != "sqlite_sequence":
                m.append(i)
        n = m
        table.setRowCount(len(n))

        table.setHorizontalHeaderLabels(["name", "delete", "rows", "columns", "discription"])
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, o in enumerate(n):
            self.cursor.execute(f"SELECT * FROM {o[0]};")
            tables = self.cursor.fetchall()

            self.cursor.execute(f"pragma table_info('{o[0]}');")
            info = self.cursor.fetchall()

            btn = QPushButton()
            btn.setText(n[i][0])
            btn.clicked.connect(lambda x, i=i: self.choose_table(n[i]))  # костыль detected

            btn2 = QPushButton()
            btn2.setText("del")
            btn2.clicked.connect(lambda ch, name=o[0]: self.del_table(name))  # костыль detected

            table.setCellWidget(i, 0, btn)
            table.setCellWidget(i, 1, btn2)
            table.setItem(i, 2, QTableWidgetItem(str(len(tables))))
            table.setItem(i, 3, QTableWidgetItem(str(len(info))))
            table.setItem(i, 4, QTableWidgetItem(str(info)))

        table.resizeColumnsToContents()
        self.vbox.addWidget(table)
        self.setCentralWidget(self.widgeg)

    def create_table(self):

        Columns = []
        self.window2 = QWidget()
        w = self.window2
        w.show()
        vlay = QVBoxLayout()
        w.setLayout(vlay)

        hlay0 = QHBoxLayout()
        hlay1 = QHBoxLayout()
        hlay2 = QHBoxLayout()

        vlay.addLayout(hlay0)
        vlay.addLayout(hlay1)

        tablename = QLineEdit(f"NewTable_{random.randint(0, 1000)}")
        hlay0.addWidget(QLabel("Enter new table name :"), alignment=Qt.AlignVCenter)
        hlay0.addWidget(tablename)

        save = QPushButton("Save")
        cancel = QPushButton("cancel")
        add = QPushButton("Add")

        maket = QVBoxLayout()
        maket.addWidget(QLabel("Column name"))
        x = QLineEdit("id")
        x.setEnabled(False)
        maket.addWidget(x)
        maket.addWidget(QLabel("Data type"))
        maket.addWidget(QLabel("INTEGER"), alignment=(Qt.AlignVCenter | Qt.AlignTop))
        hlay1.addLayout(maket)

        def add_column():
            maket = QVBoxLayout()
            maket.addWidget(QLabel("Column name :"))
            name = QLineEdit()
            maket.addWidget(name)
            maket.addWidget(QLabel("Data type :"))
            types = QComboBox()
            types.addItems(Masks.keys())
            Columns.append([name, types])
            maket.addWidget(types, alignment=(Qt.AlignVCenter | Qt.AlignTop))
            hlay1.addLayout(maket)

        def save_(self):
            command = f"Create table {tablename.text()} ( id INTEGER PRIMARY KEY autoincrement , "
            for i in Columns:
                if i[0].text() == "":  # защиты от пробелов не будет
                    continue
                command += i[0].text()
                command += " "
                command += i[1].currentText()
                command += " , "
            command = command[:-2] + ");"
          
            try:
                self.cursor.execute(command)
                self.window2.close()
                self.con.commit()
                self.Choose_table_Area()
            except:
                total_error()

        add.clicked.connect(add_column)
        save.clicked.connect(lambda: save_(self))
        cancel.clicked.connect(self.window2.close)
        hlay2.addWidget(save)
        hlay2.addWidget(cancel)
        vlay.addWidget(add)
        vlay.addLayout(hlay2)

app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
