import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
# from natsort import natsorted
import csv
from PyQt6 import QtCore


class RESTRICTIONS(QtWidgets.QDialog):
    def __init__(self, sqlite_connection=None, cursor=None, connect__db=None, parent=None):
        super(RESTRICTIONS, self).__init__(parent)

        self.sqlite_connection = sqlite_connection
        self.cursor = cursor
        self.connect__db = connect__db

        # Добавляем элементы в виджет

        # Добавляем элементы Layout
        self.v__layout = QtWidgets.QVBoxLayout(self)
        self.h__layout_1 = QtWidgets.QHBoxLayout(self)
        self.h__layout_2 = QtWidgets.QHBoxLayout(self)
        # self.h__layout_3 = QtWidgets.QHBoxLayout(self)
        self.v__layout.setObjectName("v__layout")
        self.h__layout_1.setObjectName("h__layout_1")
        self.h__layout_2.setObjectName("h__layout_2")
        # Добавляем элементы Button
        self.btn__save = QtWidgets.QPushButton(self)
        self.btn__close = QtWidgets.QPushButton(self)
        self.btn__save.setObjectName("save")
        self.btn__close.setObjectName("close")
        self.btn__save.clicked.connect(self.save__csv)
        self.btn__close.clicked.connect(self.closed)
        self.btn__save.setText("Сохранить")
        self.btn__close.setText("Закрыть")
        # Добавляем элементы ComboBox
        self.restrict = QtWidgets.QComboBox(self)
        self.restrict.setObjectName("restrict")
        self.restrict.addItem("Отключенные")
        self.restrict.addItem("Заваренные")
        # Добавляем элементы Label
        self.path__save = QtWidgets.QLabel(self)
        self.path__save.setObjectName("path__save")
        # Добавляем созданные элементы в Layout
        self.v__layout.addLayout(self.h__layout_1)
        self.v__layout.addLayout(self.h__layout_2)
        self.h__layout_2.addWidget(self.restrict)
        self.h__layout_2.addWidget(self.btn__save)
        self.h__layout_2.addWidget(self.btn__close)
        self.h__layout_1.addWidget(self.path__save)
        # Задаем параметры
        self.setWindowTitle("Санкции")
        self.setMinimumWidth(500)
        self.setFixedHeight(90)
        self.restrict.setMinimumSize(100, 36)
        self.btn__save.setMinimumSize(100, 36)
        self.btn__close.setMinimumSize(100, 36)
        self.path__save.setMinimumSize(100, 36)

        # self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint)


    def save__csv(self):
        if self.connect__db:
            restrict = self.restrict.currentIndex()
            file__name = ""
            if restrict == 0:
                restrict = "electro__energy"
                file__name = "Отключенные.csv"
            if restrict == 1:
                restrict = "brew"
                file__name = "Заваренные.csv"
            try:
                sql__select_restrict = f"""SELECT owner.id__garage, owner.surname, owner.name, owner.patronymic,
                                                owner.telephone, owner.telephone__2
                                            FROM owner JOIN restrictions 
                                            ON owner.id__garage=restrictions.id__garage WHERE {restrict}='True'"""
                self.cursor.execute(sql__select_restrict)
                res = self.cursor.fetchall()
                file, _ = QFileDialog.getSaveFileName(self, "Сохранение", f"./reports/{file__name}", "*.csv")
                if file:
                    with open(f"{file}", "w", encoding='utf-8', newline="") as f:
                        write = csv.writer(f, delimiter='\t')
                        # write.writerow([f"{file__name.split('.')[0]}"])
                        # write.writerow(["Гараж", "Фамилия", "Имя", "Отчество", "Телефон", "Телефон"])
                        for i in res:
                            result = []
                            for num in range(len(i)):
                                result.append(i[num])
                            write.writerow(result)
                        self.path__save.setText(f"Файл сохранен:  {str(file)}")
            except sqlite3.Error as err:
                print(err)


    def closed(self):
        self.close()
