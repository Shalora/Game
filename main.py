import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout, QTextEdit, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
import os
import pages as im
import sqlite3
import random
import functions as fu
import names
from datetime import datetime

bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'user.db')

connectSql = sqlite3.connect(getpath)


user = "Shalora"
userid = 0


def checkUser():
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM user WHERE nick = "{user}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    if not zeilen:
        cursor.execute(
            f'INSERT INTO user ("nick", "nahrung", "holz") VALUES ("{user}", 200, 20)')
        connectSql.commit()

        cursor.execute(
            'INSERT INTO gebaeude ("name", "holz") VALUES ("Holzfäller", 20)')
        connectSql.commit()

        cursor.execute(
            'INSERT INTO gebaeude ("name", "holz") VALUES ("Bauernhof", 50)')
        connectSql.commit()

        cursor.execute(
            'INSERT INTO gebaeude ("name", "holz") VALUES ("Hütte", 150)')
        connectSql.commit()

        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM user WHERE nick = "{user}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        userid = zeilen[0][0]
        for i in range(5):
            cursor.execute(
                f'INSERT INTO einwohner ("userid", "alter", "minutenAlter") VALUES ({userid}, 18, 0)')
        connectSql.commit()


class warningWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'interfaces/warning.ui')
        self.warning = uic.loadUi(getpath, self)


class NotifyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'interfaces/notify.ui')
        self.notify = uic.loadUi(getpath, self)


class Dialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM user WHERE nick = "{user}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        self.userid = zeilen[0][0]

        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'interfaces/main.ui')

        self = uic.loadUi(getpath, self)

        self.framelayout.setAlignment(Qt.AlignTop)
        self.testLabel.mousePressEvent = self.open_test
        self.testLabel_2.mousePressEvent = self.open_page2
        self.testLabel_3.mousePressEvent = self.open_statistik
        self.testLabel_4.mousePressEvent = self.open_forschung

        self.labelNews.mousePressEvent = self.showNotify

        self.timerDay = QTimer()
        self.timerDay.setInterval(1000)
        self.timerDay.timeout.connect(self.calculateThings)
        self.timerDay.start()

        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.printRess)
        self.timer.start()

        self.timer2 = QTimer()
        self.timer2.setInterval(10000)
        self.timer2.timeout.connect(self.calcOverview)
        self.timer2.start()

        self.notifyWindow = NotifyWindow()

    def closeEvent(self, event):
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'user.db')

        now = datetime.now()
        current_time = now.strftime("%d%m%y")

        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath2 = os.path.join(
            bundle_dir, f'dbbackup/my_backup{current_time}.db')

        memory_db = sqlite3.connect(getpath)
        backup_db = sqlite3.connect(getpath2)
        memory_db.backup(backup_db)
        memory_db.close()
        backup_db.close()

    def showNotify(self, event):
        self.notifyWindow.show()
        fu.refreshNotify(self.notifyWindow)

    def calculateThings(self):
        gesZufriedenheit = 0
        cursor = connectSql.cursor()
        rohstoffe = fu.getRohstoffe(self)

        HolzArb = 0
        zeilen = fu.getBauten(self, 1)
        if zeilen:
            HolzArb = zeilen[0][4]

        bauern = 0
        zeilen = fu.getBauten(self, 2)
        if zeilen:
            bauern = zeilen[0][4]

        fischer = 0
        zeilen = fu.getBauten(self, 5)
        if zeilen:
            fischer = zeilen[0][4]

        wassertraeger = 0
        zeilen = fu.getBauten(self, 4)
        if zeilen:
            wassertraeger = zeilen[0][4]

        steinmetz = 0
        zeilen = fu.getBauten(self, 8)
        if zeilen:
            steinmetz = zeilen[0][4]

        eisenberg = 0
        zeilen = fu.getBauten(self, 10)
        if zeilen:
            eisenberg = zeilen[0][4]

        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        gesamtEinwohner = len(zeilen)

        for zeile in zeilen:
            gesZufriedenheit += zeile[5]

        durZufriedenheit = gesZufriedenheit / gesamtEinwohner
        fakZufriedenheit = durZufriedenheit / 100

        holzpflug = fu.getForschung(self, 1)
        nahrungForAdd = 1 + (holzpflug[3] * holzpflug[5])

        self.nahrung = rohstoffe["nahrung"] + (
                    ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (gesamtEinwohner * (1 / 300))) * fakZufriedenheit * nahrungForAdd)
        self.holz = rohstoffe["holz"] + \
            ((HolzArb * ((10 / 10) / 60)) * fakZufriedenheit)
        self.wasser = rohstoffe["wasser"] + \
            ((wassertraeger * (1 / 200)) * fakZufriedenheit)
        self.stein = rohstoffe["stein"] + \
            ((steinmetz * (1 / 60)) * fakZufriedenheit)
        self.eisen = rohstoffe["eisen"] + \
            ((eisenberg * (1 / 70)) * fakZufriedenheit)

        if self.nahrung < 0:
            self.nahrung = 0
        if self.holz < 0:
            self.holz = 0
        if self.wasser < 0:
            self.wasser = 0
        if self.stein < 0:
            self.stein = 0
        if self.eisen < 0:
            self.eisen = 0

        exucute = f'UPDATE user set nahrung = "{self.nahrung}", holz = "{self.holz}", wasser = {self.wasser}, ' \
                  f'stein = {self.stein}, eisen = {self.eisen} WHERE id = "{self.userid}" '
        cursor.execute(exucute)
        connectSql.commit()

        exucute = f'SELECT * FROM rohereignisStart WHERE userid = "{self.userid}" and zeitleft > 0'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        if zeilen:

            rest = zeilen[0][2]
            rest -= 1
            ex = f'UPDATE rohereignisStart SET zeitleft = {rest} WHERE userid = "{self.userid}" and zeitleft > 0'
            cursor.execute(ex)

            ex = f'SELECT * FROM rohstoffereignis WHERE id = "{zeilen[0][0]}"'
            cursor.execute(ex)
            zei = cursor.fetchall()
            beschreibung = zei[0][1]
            rohstoffEr = zei[0][2]
            rohstoffPl = zei[0][3]
            rohstoffMi = zei[0][4]

            ex = f'SELECT {rohstoffEr} FROM user WHERE id = "{self.userid}"'
            cursor.execute(ex)
            zei = cursor.fetchall()

            rohstoff = zei[0][0]
            if rohstoffPl:

                if rohstoffEr == "nahrung":
                    calc = ((fischer * (1 / 75)) + (bauern * (1 / 100)
                                                    ) - (gesamtEinwohner * (1 / 300)))

                if rohstoffEr == "holz":
                    calc = (HolzArb * ((10 / 10) / 60))
                if rohstoffEr == "wasser":
                    calc = (wassertraeger * (1 / 200))
                if rohstoffEr == "stein":
                    calc = (wassertraeger * (1 / 60))
                plpr = (rohstoffPl / 100)

                rohstoffnach = rohstoff + (calc * plpr)

            if rohstoffMi:

                if rohstoffEr == "nahrung":
                    calc = ((fischer * (1 / 75)) + (bauern * (1 / 100)
                                                    ) - (gesamtEinwohner * (1 / 300)))
                if rohstoffEr == "holz":
                    calc = (HolzArb * ((10 / 10) / 60))
                if rohstoffEr == "wasser":
                    calc = (wassertraeger * (1 / 200))
                if rohstoffEr == "stein":
                    calc = (wassertraeger * (1 / 60))
                plpr = (rohstoffMi / 100)

                rohstoffnach = rohstoff - (calc * plpr)

            ex = f'UPDATE USER SET {rohstoffEr} = {rohstoffnach} WHERE id = "{self.userid}"'
            cursor.execute(ex)
            connectSql.commit()

            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            getpath = os.path.join(bundle_dir, 'pictures/warn.png')
            pixmap = QPixmap(getpath)
            self.warnLabel.setPixmap(pixmap)

            self.warnLabel.setToolTip(beschreibung)
            self.warnLabel.setStyleSheet("""QToolTip {
                                       background-color: black;
                                       color: red;
                                       border: black solid 1px
                                       }""")

        else:
            self.warnLabel.clear()

        self.calcGeneral()

        fu.checkBuildings(self)

        fu.calcKette(self, "holz", 2, "papier", 1, 9)
        fu.calcKette(self, "holz", 2, "kohle", 1, 11)
        fu.calc2Kette(self, "eisen", 1, "kohle", 1, "eisenbarren", 1, 12)

    def calcOverview(self):
        self.stimmungsEreignis()
        self.einwohnerBeduerfnis()
        self.einwohnerEreignis()
        self.calcEreignis()
        self.calcEinwohner()

    def calcGeneral(self):
        cursor = connectSql.cursor()
        exucute = 'SELECT * FROM general'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        secondsGone = zeilen[0][0]
        lastEreignis = zeilen[0][1]
        secondsGone += 1
        lastEreignis += 1

        exucute = f'UPDATE general SET secondsgone = "{secondsGone}", lastEreignis = "{lastEreignis}"'
        cursor.execute(exucute)
        connectSql.commit()

    def stimmungsEreignis(self):
        hit = random.randint(1, 100)

        if hit == 100:
            cu = connectSql.cursor()
            ex = f'SELECT * FROM einwohner where userid = {self.userid}'
            cu.execute(ex)
            zeilen = cu.fetchall()

            pick = random.randint(0, len(zeilen) - 1)
            einid = zeilen[pick][0]

            stimmung = zeilen[pick][5]

            ex = 'SELECT * FROM stimmungsEreignis'
            cu.execute(ex)
            z = cu.fetchall()

            pickEr = random.randint(0, len(z) - 1)

            fu.saveNotify(self, f'{zeilen[pick][6]} - {z[pickEr][1]}')

            stimmung = stimmung + z[pickEr][2]
            stimmung = stimmung - z[pickEr][3]

            if stimmung < 150 and stimmung > 0:
                ex = f'UPDATE einwohner SET zufriedenheit = {stimmung} WHERE einwohnerid = {einid}'
                cu.execute(ex)
                connectSql.commit()

    def einwohnerBeduerfnis(self):
        hit = random.randint(1, 100)

        if hit == 100:
            cu = connectSql.cursor()
            ex = 'SELECT * FROM general where warningopen = 0'
            cu.execute(ex)
            zeilen = cu.fetchone()

            if zeilen:
                self.warningWin = warningWindow()
                cu = connectSql.cursor()
                ex = f'SELECT * FROM bedarfsMeldungen'
                cu.execute(ex)
                zeilen = cu.fetchall()

                pickMeldung = random.randint(0, len(zeilen) - 1)
                bedarfRes = zeilen[pickMeldung][2]
                bedarfAnz = zeilen[pickMeldung][4]
                ex = f'SELECT * FROM bedarfDo where userid = "{self.userid}" and accept = 0'

                cu.execute(ex)
                ze = cu.fetchall()
                if not ze:
                    exu = f'SELECT * FROM einwohner where userid = {self.userid}'
                    cu.execute(exu)
                    zei = cu.fetchall()
                    pick = random.randint(0, len(zei) - 1)
                    einid = zei[pick][0]

                    ex = f'Insert into bedarfDo ("bid", "userid", "accept", "einid") VALUES ("{zeilen[pickMeldung][0]}", "{self.userid}", "0", "{einid}")'

                    cu.execute(ex)
                    connectSql.commit()

                    exu = f'SELECT * FROM einwohner where einwohnerid = {einid}'
                    cu.execute(exu)
                    zei = cu.fetchall()
                    name = zei[0][6]
                    zufriedenheit = zei[0][5]

                    meldung = f'{name} ({zufriedenheit})\n{zeilen[pickMeldung][1]}\n{bedarfAnz} {bedarfRes}'

                    exucute = 'update general set warningopen = 1'
                    cu.execute(exucute)
                    connectSql.commit()

                    self.warningWin.show()
                    self.warningWin.warningLabel.setText(f'{meldung}')
                    self.warningWin.ablehnenButton.clicked.connect(
                        lambda checked, text=zeilen[pickMeldung][0]: self.bedarfCancelChoose(text))
                    self.warningWin.annehmenButton.clicked.connect(
                        lambda checked, text=zeilen[pickMeldung][0]: self.bedarfAcceptChoose(text))

    def bedarfCancelChoose(self, bid):

        cursor = connectSql.cursor()
        exucute = f'DELETE FROM bedarfDo WHERE bid = "{bid}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        connectSql.commit()
        self.warningWin.close()
        self.warningWin.deleteLater()
        self.warningWin = None

        exucute = 'update general set warningopen = 0'
        cursor.execute(exucute)
        connectSql.commit()

    def bedarfAcceptChoose(self, bid):
        cursor = connectSql.cursor()

        ex = f'SELECT einid FROM bedarfDo WHERE bid = "{bid}" and userid = "{self.userid}" and accept = 0'

        cursor.execute(ex)
        zeilen = cursor.fetchall()
        einid = zeilen[0][0]

        ex = f'SELECT * FROM bedarfsMeldungen where bid = {bid}'

        cursor.execute(ex)
        zeilen = cursor.fetchall()

        rohstoff = zeilen[0][2]
        minus = zeilen[0][4]
        zufriedenheit = zeilen[0][5]

        ex = f'SELECT {rohstoff} FROM user where id = {self.userid}'
        cursor.execute(ex)
        zeilen = cursor.fetchall()
        rohstoffakt = zeilen[0][0]

        ex = f'SELECT zufriedenheit FROM einwohner where einwohnerid = {einid} '
        cursor.execute(ex)
        zeilen = cursor.fetchall()
        zufriedenheitBu = zeilen[0][0]

        if (rohstoffakt - minus) >= 0:
            rohstoffakt -= minus
            ex = f'UPDATE user SET {rohstoff} = {rohstoffakt} where id = {self.userid}'
            cursor.execute(ex)
            connectSql.commit()

            zufriedenheitBu += zufriedenheit
            x = f'UPDATE einwohner SET zufriedenheit = {zufriedenheitBu} where einwohnerid = {einid}'
            cursor.execute(x)
            connectSql.commit()
        else:
            fu.saveNotify(self, "Sie besitzen nicht genug Rohstoffe")

        cursor = connectSql.cursor()
        exucute = f'UPDATE bedarfDo SET accept = "1" WHERE bid = "{bid}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        connectSql.commit()
        self.warningWin.close()
        self.warningWin.deleteLater()
        self.warningWin = None

        exucute = 'update general set warningopen = 0'
        cursor.execute(exucute)
        connectSql.commit()

    def einwohnerEreignis(self):
        hit = random.randint(1, 100)

        if hit == 51000:
            cu = connectSql.cursor()
            ex = 'SELECT * FROM general where warningopen = 0'
            cu.execute(ex)
            zeilen = cu.fetchone()

            if zeilen:

                self.warningWin = warningWindow()

                ex = f'SELECT * FROM einwohnerereignis'
                cu.execute(ex)
                zeilen = cu.fetchall()

                pick = random.randint(0, len(zeilen) - 1)

                ex = f'SELECT * FROM einereignisChoose where userid = "{self.userid}" and accept = 0'
                cu.execute(ex)
                ze = cu.fetchall()
                if not ze:
                    ex = f'Insert into einereignisChoose ("erid", "userid", accept) VALUES ("{zeilen[pick][0]}", "{self.userid}", "0")'
                    cu.execute(ex)
                    connectSql.commit()

                    self.warningWin.show()

                    exucute = 'update general set warningopen = 1'
                    cu.execute(exucute)
                    connectSql.commit()

                    self.warningWin.warningLabel.setText(f'{zeilen[pick][1]}')
                    self.warningWin.ablehnenButton.clicked.connect(
                        lambda checked, text=zeilen[pick][0]: self.cancelChoose(text))
                    self.warningWin.annehmenButton.clicked.connect(
                        lambda checked, text=zeilen[pick][0]: self.acceptChoose(text))

    def acceptChoose(self, erid):
        cursor = connectSql.cursor()
        exucute = f'UPDATE einereignisChoose SET accept = "1" WHERE erid = "{erid}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        connectSql.commit()
        self.warningWin.close()
        self.warningWin.deleteLater()
        self.warningWin = None

        ex = f'SELECT * FROM einwohnerereignis where id = "{erid}"'
        cursor.execute(ex)
        zeil = cursor.fetchall()
        plus = zeil[0][2]

        i = 1

        while i <= plus:
            alter = random.randint(16, 30)
            name = names.get_full_name()

            exucute = f'INSERT INTO einwohner ("userid", "lebensalter", "name") VALUES ("{self.userid}", "{alter}", "{name}")'
            cursor.execute(exucute)
            connectSql.commit()

            fu.saveNotify(
                self, f'Sie haben einen neuen Einwohner Name: {name} Alter: {alter}')
            i += 1

        exucute = 'update general set warningopen = 0'
        cursor.execute(exucute)
        connectSql.commit()

    def cancelChoose(self, erid):
        cursor = connectSql.cursor()
        exucute = f'DELETE FROM einereignisChoose WHERE erid = "{erid}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        connectSql.commit()
        self.warningWin.close()
        self.warningWin.deleteLater()
        self.warningWin = None

        exucute = 'update general set warningopen = 0'
        cursor.execute(exucute)
        connectSql.commit()

    def calcEreignis(self):
        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM general'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        secondsGone = zeilen[0][0]
        lastEreignis = zeilen[0][1]

        if secondsGone > 3600:
            if lastEreignis >= 1800:
                hit = random.randint(1, 100)

                if hit >= 98:
                    exucute = f'SELECT * FROM rohstoffereignis'
                    cursor.execute(exucute)
                    zeilen = cursor.fetchall()
                    ereignisRand = random.randint(0, len(zeilen) - 1)
                    erId = zeilen[ereignisRand][0]

                    fu.saveNotify(self, zeilen[ereignisRand][1])

                    exucute = f'UPDATE general SET lastEreignis = 0'
                    cursor.execute(exucute)
                    connectSql.commit()

                    ex = f'INSERT INTO rohereignisStart ("erid", "userid", "zeitleft") VALUES ("{zeilen[ereignisRand][0]}", "{self.userid}", "{zeilen[ereignisRand][5]}")'
                    cursor.execute(ex)
                    connectSql.commit()

                    fu.changeStimmungAll(self, zeilen[ereignisRand][6])

    def calcEinwohner(self):
        cursor = connectSql.cursor()
        huette = 0
        gesamtAlter = 0
        AnteilZeug = 0

        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        for zeile in zeilen:
            alter = zeile[2] + (1 / (5 * 6))
            exucute = f'UPDATE einwohner SET lebensalter = "{alter}" WHERE einwohnerid = "{zeile[0]}"'
            cursor.execute(exucute)
            connectSql.commit()
            if alter > 14 and alter < 30:
                AnteilZeug += 1
                gesamtAlter += alter

        vorhandenArbeiter = len(zeilen)

        exucute = f'SELECT * FROM bauten where gebid = "3" and userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        if zeilen:
            huette = zeilen[0][3]

        maxArbeiter = 5 + (huette * 5)

        if vorhandenArbeiter < maxArbeiter:
            zeugungsGruppen = round(AnteilZeug / 2)

            if zeugungsGruppen >= 1:

                exucute = f'SELECT * FROM user where id = "{self.userid}"'
                cursor.execute(exucute)
                zeilen = cursor.fetchall()
                secWith = zeilen[0][5]

                maxHit = 200 / zeugungsGruppen

                if secWith > round(maxHit):
                    secWith = round(maxHit)
                hit = random.randint(secWith, round(maxHit))

                if hit != round(maxHit):

                    secWith += 10

                    exucute = f'UPDATE user SET secondsWithout = "{secWith}" where id = "{self.userid}"'
                    cursor.execute(exucute)
                    connectSql.commit()

                else:
                    exucute = f'UPDATE user SET secondsWithout = "0" where id = "{self.userid}"'
                    cursor.execute(exucute)
                    connectSql.commit()

                    exucute = f'INSERT INTO einwohner ("userid", "lebensalter", "name") VALUES ("{self.userid}", "0", "{names.get_full_name()}")'
                    cursor.execute(exucute)
                    connectSql.commit()

                    fu.saveNotify(self, "Ein neuer Einwohner wurde geboren")

        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}" AND lebensalter > 40'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        for zeile in zeilen:

            hit = random.randint(int(zeile[2]), 100)

            if hit == 100:
                if zeile[3] > 0:
                    ex = f'SELECT arbeiter FROM bauten WHERE userid = "{self.userid}" AND id = "{zeile[3]}"'
                    cursor.execute(ex)
                    ze = cursor.fetchall()

                    newAn = ze[0][0] - 1

                    ex = f'UPDATE bauten set arbeiter = "{newAn}" WHERE userid = "{self.userid}" AND id = "{zeile[3]}"'
                    cursor.execute(ex)
                    connectSql.commit()

                exucute = f'DELETE FROM einwohner WHERE einwohnerid = "{zeile[0]}"'
                cursor.execute(exucute)
                connectSql.commit()
                fu.saveNotify(self, "Ein Einwohner ist Gestorben")

    def open_test(self, event):
        self.clearLayout(self.framelayout)
        im.test(self)

    def open_page2(self, event):
        self.clearLayout(self.framelayout)
        im.gebaeude(self)

    def open_forschung(self, event):
        self.clearLayout(self.framelayout)
        im.forschung(self)

    def open_statistik(self, event):
        self.clearLayout(self.framelayout)
        im.statistiken(self)

    def printRess(self):
        vorhandenArbeiter = 0
        huette = 0
        maxArbeiter = 0
        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM bauten where userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        for zeile in zeilen:
            vorhandenArbeiter += zeile[4]

        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        for zeile in zeilen:
            if zeile[2] > 12:
                maxArbeiter += 1

        freiArbeiter = maxArbeiter - vorhandenArbeiter

        rohstoffe = fu.getRohstoffe(self)

        self.labelNahrung.setText(
            f'Nahrung: {str(round(rohstoffe["nahrung"], 2))}\n Holz: {str(round(rohstoffe["holz"], 2))}\n'
            f'Stein: {str(round(rohstoffe["stein"], 2))}\n Wasser: {str(round(rohstoffe["wasser"], 2))}\n'
            f'Eisen: {str(round(rohstoffe["eisen"], 2))}\n Kohle: {str(round(rohstoffe["kohle"], 2))}\n'
            f'Eisenbarren: {str(round(rohstoffe["eisenbarren"], 2))}\n'
            f'Papier: {str(round(rohstoffe["papier"], 2))}\n Freie Arbeiter : {str(freiArbeiter)}')

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == '__main__':
    checkUser()
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()

    sys.exit(app.exec_())
