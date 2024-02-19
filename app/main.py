import sys
import sqlite3
from PyQt6 import uic, QtCore
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog
from reportsDialog import ClssDialog
from restrictions import RESTRICTIONS
from PyQt6.QtGui import QIcon
import time
import yaml
import os.path
import datetime


Form, Windows = uic.loadUiType("form.ui")
app = QApplication(sys.argv)
window = Windows()
form = Form()
form.setupUi(window)


global sqlite_connection
global cursor
global connect__db
connect__db = False
date = time.localtime()

sizeX = QApplication.primaryScreen().geometry().width()
sizeY = QApplication.primaryScreen().geometry().height()
app__sizeX = window.width()
app__sizeY = window.height()
biasX = int(sizeX / 2 - int(app__sizeX / 2))
biasY = int(sizeY / 2 - int(app__sizeY / 2))
window.move(biasX, biasY)
# window.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)

with open("qss/dark.css", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)


def set__app_title(path):
    add__title = path.split('/')
    add__title = add__title[-1]
    add__title = str(add__title)
    window.setWindowTitle(add__title)


def new__db():
    global sqlite_connection
    global cursor
    global connect__db
    file = QFileDialog.getSaveFileName(None, 'Create New File', './', "SQLite Database File (*.sqlite *.db)")
    # print(file)
    if not file[0]:
        return
    to_yaml = {'path': file[0]}
    create__garage = '''CREATE TABLE garage(
                        id__garage TEXT PRIMARY KEY,
                        companies TEXT,
                        id__owner INTEGER
                        );'''
    create__price = '''CREATE TABLE price (
                    pay__year INTEGER PRIMARY KEY,
                    membership__fee INTEGER,
                    land__tax INTEGER,
                    electro__energy REAL
                    );'''
    create__owner = '''CREATE TABLE owner (
                    id__owner INTEGER PRIMARY KEY AUTOINCREMENT,
                    surname TEXT,
                    name TEXT,
                    patronymic TEXT,
                    gender TEXT,
                    date__of_birth TEXT,
                    city TEXT,
                    street TEXT,
                    house TEXT,
                    flat TEXT,
                    telephone INTEGER,
                    telephone__2 INTEGER,
                    passport__series TEXT,
                    passport__id TEXT,
                    division__code TEXT,
                    date__of_issue TEXT,
                    issued__by TEXT,
                    comment TEXT,
                    status BOOL,
                    registration__date_beginning TEXT,
                    registration__date_end TEXT,
                    id__garage TEXT NOT NULL
                    );'''
    create__electro_energy = '''CREATE TABLE electro__energy (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             type INT,
                             counter TEXT,
                             testimony REAL,
                             id__garage TEXT NOT NULL
                             );'''
    create__payment = '''CREATE TABLE payment (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      payment__date TEXT,
                      payment__year TEXT NOT NULL,
                      payment__membership_fee REAL,
                      payment__land_tax REAL,
                      payment__electro_energy REAL,
                      payment__penalty TEXT,
                      payment__sum REAL,
                      id__garage TEXT NOT NULL
                      );'''
    create__restrictions = '''CREATE TABLE restrictions (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           electro__energy BOOL,
                           brew BOOL,
                           other VARCHAR(1000),
                           id__garage TEXT NOT NULL
                           );'''
    try:
        db = sqlite3.connect(file[0])
        cur = db.cursor()
        cur.execute(create__garage)
        cur.execute(create__price)
        cur.execute(create__owner)
        cur.execute(create__electro_energy)
        cur.execute(create__payment)
        cur.execute(create__restrictions)
        db.commit()
        cur.close()
        db.close()
        with open('settings.yaml', 'w') as fil:
            yaml.dump(to_yaml, fil)
        sqlite_connection = sqlite3.connect(file[0])
        cursor = sqlite_connection.cursor()
        set__app_title(file[0])
        connect__db = True
    except sqlite3.Error as err:
        print(err)
    myclear()


def open__file():
    global sqlite_connection
    global cursor
    global connect__db
    file = QFileDialog.getOpenFileName(None, 'Open File', './', "SQLite Database File (*.sqlite *.db)")
    if file[0]:
        to_yaml = {'path': file[0]}
        with open('settings.yaml', 'w') as fil:
            yaml.dump(to_yaml, fil)
        if connect__db:
            sqlite_connection.commit()
            cursor.close()
            sqlite_connection.close()
        sqlite_connection = sqlite3.connect(file[0])
        cursor = sqlite_connection.cursor()
        set__app_title(file[0])
        connect__db = True
        myclear()
        form.price__membership_fee.setValue(0)
        form.price__membership_fee.clear()
        form.price__electro_energy.setValue(0)
        form.price__electro_energy.clear()
        form.price__land_tax.setValue(0)
        form.price__land_tax.clear()
        setpay()


def setpay():
    global connect__db
    if not connect__db:
        return
    global cursor
    my__year = date[0]
    form.payment__year.setCurrentText('')
    form.payment__year.setCurrentText(str(my__year))
    try:
        sql = f"""SELECT * FROM price WHERE pay__year='{my__year}'"""
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            form.price__membership_fee.setValue(res[0][1])
            form.price__electro_energy.setValue(res[0][3])
            form.price__land_tax.setValue(res[0][2])
        else:
            form.price__membership_fee.setValue(0)
            form.price__membership_fee.clear()
            form.price__electro_energy.setValue(0)
            form.price__electro_energy.clear()
            form.price__land_tax.setValue(0)
            form.price__land_tax.clear()
    except sqlite3.Error as err:
        print(err)


def myclear():
    form.surname.setText('')
    form.name.setText('')
    form.patronymic.setText('')
    form.gender__male.setChecked(True)
    form.date__of_birth.setDate(QtCore.QDate(date[0], date[1], date[2]))
    form.city.setText('')
    form.street.setText('')
    form.house.setText('')
    form.flat.setText('')
    form.telephone.setValue(0)
    form.telephone.clear()
    form.telephone__2.setValue(0)
    form.telephone__2.clear()
    form.passport__series.setText('')
    form.passport__id.setText('')
    form.division__code.setText('')
    form.date__of_issue.setDate(QtCore.QDate(date[0], date[1], date[2]))
    form.issued__by.setText('')
    form.comment.setPlainText('')
    form.date__today.setDate(QtCore.QDate(date[0], date[1], date[2]))
    form.id__garage.setText('')
    form.date__on_reg.setDate(QtCore.QDate(date[0], date[1], date[2]))
    # form.date__off_reg.setDate(QtCore.QDate(date[0], date[1], date[2]))


def exit__app():
    global sqlite_connection
    sqlite_connection.commit()
    sqlite_connection.close()
    app.quit()


def price__save():
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    my__year = form.date__today.date().year()
    try:
        rp = f"SELECT * FROM price WHERE pay__year='{my__year}'"
        cursor.execute(rp)
        pr = cursor.fetchall()
        membership = form.price__membership_fee.value()
        land = form.price__land_tax.value()
        energy = form.price__electro_energy.value()
        if not pr:
            try:
                sql = f'''INSERT INTO price (pay__year, membership__fee, land__tax, electro__energy)
                                    VALUES ({my__year}, {membership}, {land}, {energy})'''
                cursor.execute(sql)
                sqlite_connection.commit()
            except sqlite3.Error as err:
                print(err)
        else:
            try:
                sql = f"""UPDATE price SET 
                membership__fee={membership}, land__tax={land}, electro__energy={energy} 
                WHERE pay__year='{year}'"""
                cursor.execute(sql)
                sqlite_connection.commit()
            except sqlite3.Error as err:
                print(err)
        payment__year_changed()
    except sqlite3.Error as err:
        print(err)


def date__changed():
    global connect__db
    if not connect__db:
        return
    my__year = form.date__today.date().year()
    global sqlite_connection
    global cursor
    try:
        rp = f"SELECT * FROM price WHERE pay__year='{my__year}'"
        cursor.execute(rp)
        pr = cursor.fetchall()
        if pr:
            form.price__membership_fee.setValue(pr[0][1])
            form.price__electro_energy.setValue(pr[0][3])
            form.price__land_tax.setValue(pr[0][2])
        else:
            form.price__membership_fee.setValue(0)
            form.price__membership_fee.clear()
            form.price__electro_energy.setValue(0)
            form.price__electro_energy.clear()
            form.price__land_tax.setValue(0)
            form.price__land_tax.clear()
    except sqlite3.Error as err:
        print(err)


def id__garage_change():
    global connect__db
    if not connect__db:
        return
    global sqlite_connection
    global cursor
    idg = form.id__garage.text()
    if sqlite_connection.cursor():
        s = f"SELECT * FROM owner WHERE id__garage='{idg}' AND status='True'"
        cursor.execute(s)
        sel = cursor.fetchall()
        if sel:
            long = len(sel)
            pars = sel[long-1]
            id__owner, surname, name, patronymic, gender, date__of_birth, city, street, house, flat, telephone, \
                telephone__2, passport__series, passport__id, division__code, date__of_issue, issued__by, comment, \
                status, registration__date_beginning, registration__date_end, id__garage = pars
            registration__date_beginning = registration__date_beginning.split('.')
            date__of_birth = date__of_birth.split('.')
            date__of_issue = date__of_issue.split('.')
            form.surname.setText(surname)
            form.name.setText(name)
            form.patronymic.setText(patronymic)
            if gender == 'male':
                form.gender__male.setChecked(True)
            if gender == 'female':
                form.gender__female.setChecked(True)
            gender__change_icon()
            form.date__of_birth.setDate(QtCore.QDate(int(date__of_birth[0]), int(date__of_birth[1]),
                                                     int(date__of_birth[2])))
            form.city.setText(city)
            form.street.setText(street)
            form.house.setText(house)
            form.flat.setText(flat)
            form.telephone.setValue(telephone)
            form.telephone__2.setValue(telephone__2)
            form.passport__series.setText(passport__series)
            form.passport__id.setText(passport__id)
            form.division__code.setText(division__code)
            form.date__of_issue.setDate(QtCore.QDate(int(date__of_issue[0]), int(date__of_issue[1]),
                                                     int(date__of_issue[2])))
            form.issued__by.setText(issued__by)
            form.comment.setPlainText(comment)
            if registration__date_beginning[0] != '':
                form.date__on_reg.setDate(QtCore.QDate(int(registration__date_beginning[0]),
                                                       int(registration__date_beginning[1]),
                                                       int(registration__date_beginning[2])))
            else:
                form.date__on_reg.setDate(QtCore.QDate(date[0], date[1], date[2]))
        else:
            form.surname.setText('')
            form.name.setText('')
            form.patronymic.setText('')
            form.gender__male.setChecked(True)
            gender__change_icon()
            form.date__of_birth.setDate(QtCore.QDate(date[0], date[1], date[2]))
            form.city.setText('')
            form.street.setText('')
            form.house.setText('')
            form.flat.setText('')
            form.telephone.setValue(0)
            form.telephone.clear()
            form.telephone__2.setValue(0)
            form.telephone__2.clear()
            form.passport__series.setText('')
            form.passport__id.setText('')
            form.division__code.setText('')
            form.date__of_issue.setDate(QtCore.QDate(date[0], date[1], date[2]))
            form.issued__by.setText('')
            form.comment.setPlainText('')
            form.date__on_reg.setDate(QtCore.QDate(date[0], date[1], date[2]))
    form.testimony.setValue(0)
    form.testimony.clear()
    form.counter__number.setText('')
    payment__year_changed()
    show__electro(idg)
    show__membership(idg)
    set__counter(idg)
    summary()
    show__restrictions()


def add__garage():
    global connect__db
    if not connect__db:
        return
    global sqlite_connection
    global cursor
    if sqlite_connection.cursor():
        idg = form.id__garage.text()
        if idg:
            date__of_issue = form.date__of_issue.date().toString('yyyy.MM.dd')
            date__of_birth = form.date__of_birth.date().toString('yyyy.MM.dd')
            telephone = 8
            telephone__2 = 8
            try:
                sql__select = f"SELECT id__garage FROM garage WHERE id__garage='{idg}'"
                cursor.execute(sql__select)
                res = cursor.fetchall()
                if not res:
                    sqlinsert = f"INSERT INTO garage ('id__garage') VALUES ('{idg}')"
                    cursor.execute(sqlinsert)
                    sqlownerinsert = f"""INSERT INTO owner ('surname', 'name', 'patronymic', 'gender', 'date__of_birth', 
                                'city', 'street', 'house', 'flat', 'telephone', 'telephone__2',
                                'passport__series', 'passport__id', 'division__code',
                                'date__of_issue', 'issued__by', 'comment', 'status', 'registration__date_beginning',
                                'registration__date_end', 'id__garage') 
                                VALUES ('', '', '', 'male', '{date__of_birth}', '', '', '', '', '{telephone}', 
                                '{telephone__2}', '', '', '', '{date__of_issue}', '', '', 'True', '', '', '{idg}')"""
                    cursor.execute(sqlownerinsert)
                    sqlite_connection.commit()
                    add_res_and_pay(idg)
            except sqlite3.Error as err:
                print(err)


def add_res_and_pay(idg):
    sql__r = f"""INSERT INTO restrictions (electro__energy, brew, id__garage) 
                                    VALUES ('False', 'False', '{idg}')"""
    cursor.execute(sql__r)
    sql__p = f"""INSERT INTO payment (payment__date, payment__year, payment__membership_fee,
                                            payment__land_tax, payment__electro_energy, 
                                            payment__penalty, payment__sum, id__garage) 
                                VALUES ('0000.00.00', '0000', '0', '0', '0', '0', '0', '{idg}')"""
    cursor.execute(sql__p)
    sqlite_connection.commit()


def del__garage():
    global connect__db
    if not connect__db:
        return
    global sqlite_connection
    global cursor
    idg = form.id__garage.text()
    if idg:
        sql__select = f"SELECT id__garage FROM garage WHERE id__garage='{idg}'"
        cursor.execute(sql__select)
        res = cursor.fetchall()
        if not res:
            return 
        reply = QtWidgets.QMessageBox()
        reply.setText("Вы уверены что хотите удалить все данные!")
        reply.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        x = reply.exec()
        if x == QtWidgets.QMessageBox.StandardButton.Yes:
            if sqlite_connection.cursor():
                try:
                    sql = f"SELECT id__garage FROM garage WHERE id__garage='{idg}'"
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    if not res:
                        return
                    sqlinsert = f"DELETE FROM garage WHERE id__garage='{idg}'"
                    cursor.execute(sqlinsert)
                    sqldelowner = f"DELETE FROM owner WHERE id__garage='{idg}'"
                    cursor.execute(sqldelowner)
                    sqldeletepay = f"DELETE FROM electro__energy WHERE id__garage='{idg}'"
                    cursor.execute(sqldeletepay)
                    sqldeleteen = f"DELETE FROM payment WHERE id__garage='{idg}'"
                    cursor.execute(sqldeleteen)
                    sqlrestrictions = f"DELETE FROM restrictions WHERE id__garage='{idg}'"
                    cursor.execute(sqlrestrictions)
                    sqlite_connection.commit()
                    myclear()
                except sqlite3.Error as err:
                    print(err)


def add__owner():
    global connect__db
    if not connect__db:
        return
    global sqlite_connection
    global cursor
    if sqlite_connection.cursor():
        idg = form.id__garage.text()
        if idg:
            gender = ''
            surname = form.surname.text()
            name = form.name.text()
            patronymic = form.patronymic.text()
            if form.gender__male.isChecked():
                gender = 'male'
            if form.gender__female.isChecked():
                gender = 'female'
            date__of_birth = form.date__of_birth.date().toString('yyyy.MM.dd')
            city = form.city.text()
            street = form.street.text()
            house = form.house.text()
            flat = form.flat.text()
            telephone = form.telephone.text()
            if not telephone:
                telephone = 8
            telephone__2 = form.telephone__2.text()
            if not telephone__2:
                telephone__2 = 8
            passport__series = form.passport__series.text()
            passport__id = form.passport__id.text()
            division__code = form.division__code.text()
            date__of_issue = form.date__of_issue.date().toString('yyyy.MM.dd')
            issued__by = form.issued__by.text()
            comment = form.comment.toPlainText()
            status = 'True'
            registration__date_beginning = form.date__on_reg.date().toString('yyyy.MM.dd')
            try:
                idsel = f"SELECT id__garage FROM garage WHERE id__garage='{idg}'"
                cursor.execute(idsel)
                idres = cursor.fetchall()
                if not idres:
                    sqlgarageinsert = f"INSERT INTO garage ('id__garage') VALUES ('{idg}')"
                    cursor.execute(sqlgarageinsert)
                    add_res_and_pay(idg)
                sql__date_end = f"""UPDATE owner SET registration__date_end='{registration__date_beginning}' 
                                    WHERE id__garage='{idg}' AND status='True'"""
                cursor.execute(sql__date_end)
                sqlstaus = f"""UPDATE owner SET status='False' WHERE id__garage='{idg}'"""
                cursor.execute(sqlstaus)
                sqlownerinsert = f"""INSERT INTO owner ('surname', 'name', 'patronymic', 'gender', 'date__of_birth', 
                            'city', 'street', 'house', 'flat', 'telephone', 'telephone__2',
                            'passport__series', 'passport__id', 'division__code',
                            'date__of_issue', 'issued__by', 'comment', 'status', 'registration__date_beginning', 
                            'registration__date_end', 'id__garage') 
                            VALUES ('{surname}', '{name}', '{patronymic}', '{gender}', '{date__of_birth}',
                            '{city}', '{street}', '{house}', '{flat}', 
                            '{telephone}', '{telephone__2}', '{passport__series}', '{passport__id}',
                            '{division__code}', '{date__of_issue}', '{issued__by}', 
                            '{comment}', '{status}', '{registration__date_beginning}', '',
                            '{idg}')"""
                cursor.execute(sqlownerinsert)
                sqlite_connection.commit()
            except sqlite3.Error as err:
                print(err)


def update__owner():
    global connect__db
    if not connect__db:
        return
    global sqlite_connection
    global cursor
    if sqlite_connection.cursor():
        idg = form.id__garage.text()
        if idg:
            try:
                gender = ''
                idsel = f"SELECT id__garage FROM garage WHERE id__garage='{idg}'"
                cursor.execute(idsel)
                idres = cursor.fetchall()
                if idres:
                    surname = form.surname.text()
                    name = form.name.text()
                    patronymic = form.patronymic.text()
                    if form.gender__male.isChecked():
                        gender = 'male'
                    if form.gender__female.isChecked():
                        gender = 'female'
                    date__of_birth = form.date__of_birth.date().toString('yyyy.MM.dd')
                    city = form.city.text()
                    street = form.street.text()
                    house = form.house.text()
                    flat = form.flat.text()
                    telephone = form.telephone.text()
                    telephone__2 = form.telephone__2.text()
                    passport__series = form.passport__series.text()
                    passport__id = form.passport__id.text()
                    division__code = form.division__code.text()
                    date__of_issue = form.date__of_issue.date().toString('yyyy.MM.dd')
                    issued__by = form.issued__by.text()
                    comment = form.comment.toPlainText()
                    status = 'True'
                    registration__date_beginning = form.date__on_reg.date().toString('yyyy.MM.dd')

                    sqlownerinsert = f"""UPDATE owner SET 
                                    surname = '{surname}',
                                    name = '{name}', 
                                    patronymic = '{patronymic}',
                                    gender = '{gender}',
                                    date__of_birth = '{date__of_birth}', 
                                    city = '{city}',
                                    street = '{street}',
                                    house = '{house}',
                                    flat = '{flat}',
                                    telephone = '{telephone}',
                                    telephone__2 = '{telephone__2}',
                                    passport__series = '{passport__series}',
                                    passport__id = '{passport__id}',
                                    division__code = '{division__code}',
                                    date__of_issue = '{date__of_issue}',
                                    issued__by = '{issued__by}',
                                    comment = '{comment}',
                                    registration__date_beginning = '{registration__date_beginning}'
                                    WHERE id__garage='{idg}' 
                                    AND status='{status}'
                                    """
                    cursor.execute(sqlownerinsert)
                    sqlite_connection.commit()
            except sqlite3.Error as err:
                print(err)


"""payment"""


def set__counter(idg):
    global cursor
    global connect__db
    if not connect__db:
        return
    try:
        sql = f"SELECT counter FROM electro__energy WHERE id__garage='{idg}' ORDER BY id DESC LIMIT 0, 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            form.counter__number.setText(res[0][0])
    except sqlite3.Error as err:
        print(err)


def show__electro(idg):
    global cursor
    global connect__db
    if not connect__db:
        return
    form.table__electro.clearContents()
    try:
        sql = f"SELECT * FROM electro__energy WHERE id__garage='{idg}' ORDER BY id DESC LIMIT 0, 5"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for x in range(len(res)):
                for y in range(2):
                    form.table__electro.setItem(x, y, QtWidgets.QTableWidgetItem(str(res[x][y+2])))
                    y += 1
        else:
            for x in range(5):
                for y in range(2):
                    form.table__electro.setItem(x, y, QtWidgets.QTableWidgetItem(''))
                    y += 1
    except sqlite3.Error as e:
        print(e)


def show__membership(idg):
    global cursor
    global connect__db
    if not connect__db:
        return
    form.table__membership.clearContents()
    try:
        sql = f"SELECT * FROM payment WHERE id__garage='{idg}' ORDER BY id DESC LIMIT 0, 5"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for x in range(len(res)):
                for y in range(7):
                    form.table__membership.setItem(x, y, QtWidgets.QTableWidgetItem(str(res[x][y+1])))
                    y += 1
        else:
            for x in range(5):
                for y in range(7):
                    form.table__membership.setItem(x, y, QtWidgets.QTableWidgetItem(''))
                    y += 1
    except sqlite3.Error as e:
        print(e)


def payment__clean():
    form.payment__contribution.setValue(0)
    form.payment__contribution.clear()
    form.payment__land.setValue(0)
    form.payment__land.clear()
    form.testimony.setValue(0)
    form.testimony.clear()
    form.payment__electro_energy.setValue(0)
    form.payment__electro_energy.clear()
    # form.counter__number.setText('')


def payment__start():
    global cursor
    global connect__db
    if not connect__db:
        return
    try:
        sql = f"""SELECT * FROM price WHERE pay__year='{date[0]}'"""
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            memb = res[0][1]
            land = res[0][2]
            form.payment__contribution.setValue(memb)
            form.payment__land.setValue(land)
            form.testimony.clear()
            form.testimony.setValue(0)
            form.payment__electro_energy.setValue(res[0][3])
            payall()
        else:
            payment__clean()
    except sqlite3.Error as err:
        print(err)


def payment__year_changed():
    global cursor
    global connect__db
    if not connect__db:
        return
    my__year = form.payment__year.currentText()
    idg = form.id__garage.text()
    memb = 0
    land = 0
    energy = 0
    try:
        if idg:
            sql = f"SELECT payment__membership_fee, payment__land_tax FROM payment WHERE id__garage='{idg}' \
             AND payment__year='{my__year}'"
            cursor.execute(sql)
            res__payment = cursor.fetchall()
            sql = f"""SELECT * FROM price WHERE pay__year='{my__year}'"""
            cursor.execute(sql)
            res__price = cursor.fetchall()
            if res__payment and res__price:
                energy = res__price[0][3]
                memb = res__price[0][1] - res__payment[0][0]
                land = res__price[0][2] - res__payment[0][1]
            else:
                if res__price:
                    memb = res__price[0][1]
                    land = res__price[0][2]
                    energy = res__price[0][3]
            form.payment__contribution.setValue(memb)
            form.payment__land.setValue(land)
            form.testimony.clear()
            form.testimony.setValue(0)
            form.payment__electro_energy.setValue(energy)
            payall()
        else:
            payment__clean()
    except sqlite3.Error as err:
        print("Ошибка при подключении к sqlite", err)


def tofixed(numobj, digits=0):
    return f"{numobj:.{digits}f}"


def payment__add():
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    idg = form.id__garage.text()
    if idg:
        try:
            sql = f"SELECT id__garage FROM garage WHERE id__garage='{idg}'"
            cursor.execute(sql)
            res = cursor.fetchall()
            if not res:
                return
        except sqlite3.Error as err:
            print(err)
            return
        pay__date = str(date.tm_year)
        pay__date = pay__date + '.' + str(date.tm_mon)
        pay__date = pay__date + '.' + str(date.tm_mday)
        my__year = form.payment__year.currentText()
        membership = form.payment__contribution.value()
        land = form.payment__land.value()
        counter = form.counter__number.text()
        if not counter:
            counter = ''
        testimony = form.testimony.value()
        energy = form.payment__electro_energy.value()
        penalty = penalt(membership, land)
        energy = energy * testimony
        to__pay = membership + land + energy + penalty
        try:
            sql__payment = f"""SELECT * FROM payment WHERE payment__year='{my__year}' AND id__garage='{idg}'"""
            cursor.execute(sql__payment)
            res__sql_payment = cursor.fetchall()
            if not res__sql_payment:
                sql__insert = f'''INSERT INTO payment ('payment__date', 'payment__year', \
                                    'payment__membership_fee', 'payment__land_tax',
                                    'payment__electro_energy', 'payment__penalty', 'payment__sum', 'id__garage')
                                    VALUES ('{pay__date}', '{my__year}', '{membership}', '{land}', \
                                    '{energy}', '{penalty}', '{to__pay}', '{idg}')'''
                cursor.execute(sql__insert)
                sqlite_connection.commit()
            else:
                membership = res__sql_payment[0][3] + membership
                land = res__sql_payment[0][4] + land
                energy = res__sql_payment[0][5] + energy
                penalty = float(res__sql_payment[0][6]) + penalty
                to__pay = res__sql_payment[0][7] + to__pay
                sql__update = f"""UPDATE payment SET payment__date='{pay__date}',
                                                     payment__membership_fee='{membership}',   
                                                     payment__land_tax='{land}',
                                                     payment__electro_energy='{energy}',   
                                                     payment__penalty='{penalty}',   
                                                     payment__sum='{to__pay}' 
                                                WHERE payment__year='{my__year}'"""
                cursor.execute(sql__update)
                sqlite_connection.commit()
            sql__testimony = f"SELECT testimony FROM electro__energy WHERE id__garage='{idg}' \
                    ORDER BY id DESC LIMIT 0, 1"
            cursor.execute(sql__testimony)
            res__sql_testimony = cursor.fetchone()
            if res__sql_testimony:
                testimony = res__sql_testimony[0] + testimony
            type__e = 1
            sql__e = f'''INSERT INTO electro__energy ('type', 'counter', 'testimony', 'id__garage')
                                            VALUES ('{type__e}', '{counter}', '{testimony}', '{idg}')'''
            cursor.execute(sql__e)
            sqlite_connection.commit()
            form.testimony.setValue(0)
        except sqlite3.Error as err:
            print(err)
        payment__year_changed()
        show__electro(idg)
        show__membership(idg)


def payall():
    membership = form.payment__contribution.value()
    land = form.payment__land.value()
    testimony = form.testimony.value()
    energy = form.payment__electro_energy.value()
    pen = penalt(membership, land)
    pay = membership + land + (testimony * energy) + pen
    form.penalty__label.setText(str(pen))
    form.payment__sum.setText(str(pay))


def penalt(memb=0, land=0):
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    per__year = form.payment__year.currentText()
    before__membership = f"{per__year}.10.01"
    before__land = f"{int(per__year)+1}.03.01"
    before__membership = before__membership.split('.')
    before__land = before__land.split('.')
    before__membership = datetime.date(int(before__membership[0]),
                                       int(before__membership[1]), int(before__membership[2]))
    before__land = datetime.date(int(before__land[0]), int(before__land[1]), int(before__land[2]))
    today = f"{date.tm_year}.{date.tm_mon}.{date.tm_mday}"
    today = today.split('.')
    today = datetime.date(int(today[0]), int(today[1]), int(today[2]))
    delay__membership_day = int(str(today - before__membership).split()[0])
    delay__land_day = int(str(today - before__land).split()[0])
    penalty = form.payment__penalty.currentText()
    penalty = int(penalty.split('%')[0])/100
    penalty__membership_pay = 0
    penalty__land_pay = 0
    if delay__membership_day > 0:
        penalty__membership_pay = (memb * 0.003) * delay__membership_day
        if penalty__membership_pay > memb:
            penalty__membership_pay = memb
    if delay__land_day > 0:
        penalty__land_pay = (land * 0.003) * delay__land_day
        if penalty__land_pay > land:
            penalty__land_pay = land
    penalty__all = float(tofixed((penalty__membership_pay + penalty__land_pay) * penalty))
    return penalty__all


"""payment end"""


def summary():
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    idg = form.id__garage.text()
    no__data = 'Нет данных'
    if idg:
        sqlsummary__owner = f"""SELECT surname, name, patronymic, street, house, flat, telephone, telephone__2, 
                                        registration__date_beginning 
                                    FROM owner WHERE id__garage='{idg}' AND status='True'"""
        cursor.execute(sqlsummary__owner)
        summary__owner = cursor.fetchall()
        if summary__owner:
            long = len(summary__owner)
            summary__owner = summary__owner[long - 1]
            surname, name, patronymic, street, house, flat, telephone, telephone__2, registration__date = summary__owner
            form.summary__surname_2.setText(str(surname))
            form.summary__name_2.setText(str(name))
            form.summary__middlename_2.setText(str(patronymic))
            form.summary__street_2.setText(str(street))
            form.summary__house_2.setText(str(house))
            form.summary__flat_2.setText(str(flat))
            form.summary__telephone2.setText(str(telephone))
            form.summary__telephone2_2.setText(str(telephone__2))
            form.summary__registration_2.setText(str(registration__date))
        else:
            form.summary__surname_2.setText(no__data)
            form.summary__name_2.setText(no__data)
            form.summary__middlename_2.setText(no__data)
            form.summary__street_2.setText(no__data)
            form.summary__house_2.setText(no__data)
            form.summary__flat_2.setText(no__data)
            form.summary__telephone2.setText(no__data)
            form.summary__telephone2_2.setText(no__data)
            form.summary__registration_2.setText(no__data)
        sqlsummary__pay = f"""SELECT payment__year FROM payment WHERE id__garage='{idg}' 
                                                    AND payment__year=(SELECT MAX(payment__year) FROM payment
                                                    WHERE id__garage='{idg}')"""
        cursor.execute(sqlsummary__pay)
        summary__pay = cursor.fetchall()
        if summary__pay:
            form.last__year_payment.setText(summary__pay[0][0])
        else:
            form.last__year_payment.setText(no__data)

        sqlsummary__electro = f"""SELECT type, counter, testimony FROM electro__energy WHERE id__garage ='{idg}'
                                    ORDER BY testimony DESC LIMIT 1"""
        cursor.execute(sqlsummary__electro)
        summary__electro = cursor.fetchall()
        if summary__electro:
            L = no__data
            if summary__electro[0][0] == 1:
                L = 'Однофазный'
            if summary__electro[0][0] == 3:
                L = 'Трехфазный'
            form.summary__type.setText(L)
            form.summary__counter.setText(str(summary__electro[0][1]))
            form.meter__readings.setText(str(summary__electro[0][2]))
        else:
            form.summary__type.setText(no__data)
            form.summary__counter.setText(no__data)
            form.meter__readings.setText(no__data)

        # form.number__of_applications.setText('')
        # form.number__of_applications.setText('Нет данных')

        sqlsummary__restrictions = f"SELECT electro__energy, brew FROM restrictions WHERE id__garage='{idg}'"
        cursor.execute(sqlsummary__restrictions)
        summary__restrictions = cursor.fetchall()
        if summary__restrictions:
            disabled = 'да' if summary__restrictions[0][0] == 'True' else 'нет'
            brew = 'да' if summary__restrictions[0][1] == 'True' else 'нет'
            form.summary__disabled_2.setText(disabled)
            form.summary__brewed_2.setText(brew)
        else:
            form.summary__disabled_2.setText(no__data)
            form.summary__brewed_2.setText(no__data)
    else:
        form.summary__surname_2.setText(no__data)
        form.summary__name_2.setText(no__data)
        form.summary__middlename_2.setText(no__data)
        form.summary__street_2.setText(no__data)
        form.summary__house_2.setText(no__data)
        form.summary__flat_2.setText(no__data)
        form.summary__telephone2.setText(no__data)
        form.summary__telephone2_2.setText(no__data)
        form.summary__registration_2.setText(no__data)
        form.last__year_payment.setText(no__data)
        form.meter__readings.setText(no__data)
        form.number__of_applications.setText(no__data)
        form.summary__disabled_2.setText(no__data)
        form.summary__brewed_2.setText(no__data)
        form.summary__type.setText(no__data)
        form.summary__counter.setText(no__data)
        form.meter__readings.setText(no__data)


def disabled():
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    idg = form.id__garage.text()
    if idg:
        try:
            checked = form.disabled.isChecked()
            sqldisabled__select = f"SELECT electro__energy FROM restrictions WHERE id__garage='{idg}'"
            cursor.execute(sqldisabled__select)
            res__disabled = cursor.fetchone()
            if not res__disabled:
                sqldisabled__i = f"INSERT INTO restrictions (electro__energy, id__garage) VALUES ('{checked}', '{idg}')"
                cursor.execute(sqldisabled__i)
            else:
                sqldisabled__up = f"UPDATE restrictions SET electro__energy='{checked}' WHERE id__garage='{idg}'"
                cursor.execute(sqldisabled__up)
            sqlite_connection.commit()
        except sqlite3.Error as err:
            print(err)


def brewed():
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    idg = form.id__garage.text()
    if idg:
        try:
            checked = form.brewed.isChecked()
            sqlbrewed__select = f"SELECT brew FROM restrictions WHERE id__garage='{idg}'"
            cursor.execute(sqlbrewed__select)
            res__brewed = cursor.fetchone()
            if not res__brewed:
                sqlbrewed__i = f"INSERT INTO restrictions (brew, id__garage) VALUES ('{checked}', '{idg}')"
                cursor.execute(sqlbrewed__i)
            else:
                sqlbrewed__up = f"UPDATE restrictions SET brew='{checked}' WHERE id__garage='{idg}'"
                cursor.execute(sqlbrewed__up)
            sqlite_connection.commit()
        except sqlite3.Error as err:
            print(err)


def show__restrictions():
    global sqlite_connection
    global cursor
    global connect__db
    if not connect__db:
        return
    idg = form.id__garage.text()
    if idg:
        try:
            sqlrestrictions = f"SELECT * FROM restrictions WHERE id__garage='{idg}'"
            cursor.execute(sqlrestrictions)
            res = cursor.fetchall()
            if not res:
                pass
            else:
                disabled = eval(res[0][1])
                brewed = eval(res[0][2])
                form.disabled.setChecked(disabled)
                form.brewed.setChecked(brewed)
        except sqlite3.Error as err:
            print(err)
    else:
        form.disabled.setChecked(False)
        form.brewed.setChecked(False)


"""-----------------reports-------------------"""


# def сontributions__owed():
#     reports()
#
#
#
def restrictions():
    restriction__reports = RESTRICTIONS(sqlite_connection, cursor, connect__db)
    restriction__reports.exec()


def reports():
    report = ClssDialog(date, sqlite_connection, cursor, connect__db)
    report.exec()


"""-----------------reports end-------------------"""


def gender__change_icon():
    if form.gender__male.isChecked():
        form.gender__female.setIcon(QIcon('icon/gender__m.png'))
    if form.gender__female.isChecked():
        form.gender__female.setIcon(QIcon('icon/gender__f.png'))

with open('settings.yaml') as f:
    myclear()
    payment__penalty_list = ("100%", "90%", "80%", "70%", "60%", "50%", "40%", "30%", "20%", "10%", "0%")
    year = int(date[0]) + 2
    for i in range(11):
        form.payment__year.addItem(str(year))
        year = year-1
    form.payment__year.setCurrentIndex(2)
    form.payment__penalty.addItems(payment__penalty_list)
    path__db = yaml.safe_load(f)
    if os.path.isfile(path__db['path']):
        try:
            sqlite_connection = sqlite3.connect(path__db['path'])
            cursor = sqlite_connection.cursor()
            set__app_title(path__db['path'])
            connect__db = True
            setpay()
        except sqlite3.Error as error:
            print(error)
        payment__start()
    else:
        set__app_title('База не потключена')

gender__change_icon()
form.add__owner.setIcon(QIcon("icon/add__garage.png"))
form.add__owner.setIconSize(QtCore.QSize(20, 20))
form.update__owner.setIcon(QIcon("icon/change.png"))
form.update__owner.setIconSize(QtCore.QSize(20, 20))
form.payment__add.setIcon(QIcon("icon/add__garage.png"))
form.payment__add.setIconSize(QtCore.QSize(20, 20))
form.gender__female.setIconSize(QtCore.QSize(22, 22))
form.l1__l3.setIcon(QIcon("icon/updates__2.png"))
form.l1__l3.setIconSize(QtCore.QSize(36, 36))
"""----Menu----"""
form.Exit.triggered.connect(exit__app)
form.Open.triggered.connect(open__file)
form.New__bd.triggered.connect(new__db)
"""----Menu end----"""

"""----price----"""
form.price__save.clicked.connect(price__save)
form.date__today.dateChanged.connect(date__changed)
"""----price end----"""

"""----garage----"""
form.id__garage.textChanged.connect(id__garage_change)
form.add__garage.clicked.connect(add__garage)
form.del__garage.clicked.connect(del__garage)
"""----garage end----"""

"""----owner----"""
form.add__owner.clicked.connect(add__owner)
form.update__owner.clicked.connect(update__owner)
"""----owner end----"""


"""----payment----"""
form.payment__year.currentTextChanged.connect(payment__year_changed)
form.payment__add.clicked.connect(payment__add)

form.payment__penalty.currentTextChanged.connect(payall)
form.payment__contribution.textChanged.connect(payall)
form.payment__land.textChanged.connect(payall)
form.payment__electro_energy.textChanged.connect(payall)
form.testimony.textChanged.connect(payall)
form.disabled.stateChanged.connect(disabled)
form.brewed.stateChanged.connect(brewed)
"""----payment end----"""

"""----gender icon change ----"""
form.gender.idClicked.connect(gender__change_icon)
"""----gender icon change end----"""

"""----reports----"""
form.debt.triggered.connect(reports)
form.restrictions.triggered.connect(restrictions)
"""----reports end----"""

if __name__ == "__main__":
    window.show()
    sys.exit(app.exec())
