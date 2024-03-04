from PyQt6 import QtWidgets
import csv
from natsort import natsorted
from PyQt6.QtWidgets import QFileDialog


class ClssDialog(QtWidgets.QDialog):
    def __init__(self, ldate=None, sqlite_connection=None, cursor=None, connect__db=None, parent=None):
        super(ClssDialog, self).__init__(parent)

        self.ldate = ldate
        self.sqlite_connection = sqlite_connection
        self.cursor = cursor
        self.connect__db = connect__db


        # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setGeometry(400, 400, 500, 100)
        # print(self.width())
        self.vLayout = QtWidgets.QVBoxLayout(self)
        self.vLayout.setObjectName("vLayout")

        self.hLayout = QtWidgets.QHBoxLayout(self)
        self.hLayout.setObjectName("hLayout")
        self.hLayout__2 = QtWidgets.QHBoxLayout(self)
        self.hLayout__2.setObjectName("hLayout__2")

        self.closed = QtWidgets.QPushButton(self)
        self.closed.setObjectName("closed")
        self.closed.clicked.connect(self.btnClosed)
        self.closed.setFixedHeight(36)

        self.saveDialog = QtWidgets.QPushButton(self)
        self.saveDialog.setObjectName("save")
        self.saveDialog.clicked.connect(self.btnDialog)
        self.saveDialog.setFixedHeight(36)

        self.yyyy = QtWidgets.QComboBox(self)
        self.yyyy.setObjectName("yyyy")
        year = int(self.ldate[0]) + 2
        for i in range(11):
            self.yyyy.addItem(str(year))
            year = year - 1
        self.yyyy.setCurrentIndex(2)
        self.yyyy.setEditable(True)
        self.yyyy.setFixedHeight(36)

        self.what__report = QtWidgets.QComboBox(self)
        self.what__report.setObjectName("what__report")
        # self.what__report.addItem("Все")
        self.what__report.addItem("Земля")
        self.what__report.addItem("Взнос")
        self.what__report.setFixedHeight(36)

        self.yyyy__label = QtWidgets.QLabel(self)
        self.yyyy__label.setObjectName("yyyy__label")
        self.what__report_label = QtWidgets.QLabel(self)
        self.what__report_label.setObjectName("what__report_label")
        self.empty__label = QtWidgets.QLabel(self)
        self.empty__label.setObjectName("empty__label")
        self.path__label = QtWidgets.QLabel(self)
        self.path__label.setObjectName("path__save")

        self.hLayout.addWidget(self.yyyy__label)
        self.hLayout.addWidget(self.what__report_label)
        self.hLayout.addWidget(self.empty__label)

        self.hLayout__2.addWidget(self.yyyy)
        self.hLayout__2.addWidget(self.what__report)
        self.hLayout__2.addWidget(self.saveDialog)

        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addLayout(self.hLayout__2)
        self.vLayout.addWidget(self.path__label)
        self.vLayout.addWidget(self.closed)
        self.setWindowTitle("Отчеты")
        self.yyyy__label.setText("Год")
        self.what__report_label.setText("Задолженность")
        self.saveDialog.setText("Сохранить")
        self.closed.setText("Закрыть")


    def btnClosed(self):
        self.close()


    def btnDialog(self):
        if not self.connect__db:
            return
        yyyy = self.yyyy.currentText()
        what__report = self.what__report.currentText()

        sql__price = f"""SELECT membership__fee, land__tax FROM price WHERE pay__year={yyyy}"""
        self.cursor.execute(sql__price)
        res__price = self.cursor.fetchall()
        what__price = 1
        save = ''
        if res__price:
            if what__report == 'Взнос':
                what = 'payment__membership_fee'
                save = 'по членскому взносу'
                what__price = res__price[0][0]
            if what__report == 'Земля':
                what = 'payment__land_tax'
                save = 'по землянному налогу'
                what__price = res__price[0][1]
        else:
            if what__report == 'Взнос':
                what = 'payment__membership_fee'
                save = 'по членскому взносу'
            if what__report == 'Земля':
                what = 'payment__land_tax'
                save = 'по землянному налогу'
        # sql__join = f"""SELECT garage.id__garage
        #                 FROM garage JOIN payment ON garage.id__garage = payment.id__garage
        #                 WHERE payment.{what}={what__price} AND payment.payment__year={yyyy}"""
        sql__ecxept = f"""SELECT id__garage FROM garage EXCEPT SELECT id__garage 
                         FROM payment WHERE payment.{what}={what__price} AND payment.payment__year={yyyy}"""
        self.cursor.execute(sql__ecxept)
        res = self.cursor.fetchall()
        self.saveFileDialog(res, save, yyyy)


    def saveFileDialog(self, res, save, yyyy):
        res = res
        save__data = save
        yyyy = yyyy
        result = []
        for value in res:
            result.append(value[0])
        result = natsorted(result)
        file, _ = QFileDialog.getSaveFileName(self, "Сохранение", f"./reports/{save__data} за {yyyy}.csv", "*.csv")
        if file:
            self.path__label.setText(f"Файл сохранен:  {str(file)}")
            # file__name = file.split("/")
            # file__name = file__name[-1]
            with open(f"{file}", "w", encoding='utf-8', newline="") as f:
                writer = csv.writer(f, delimiter='\t')
                # writer.writerow([f"Долг за {yyyy} {save__data}"])
                writer.writerow(result)


