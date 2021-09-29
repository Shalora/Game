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

class NotifyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        getpath = os.path.join(bundle_dir, 'notify.ui')
        self.notify = uic.loadUi(getpath, self)
        
        self.timerDay = QTimer()
        self.timerDay.setInterval(1000)
        self.timerDay.timeout.connect(self.refreshNotify)
        self.timerDay.start()
        
  
    def refreshNotify(self):
        self.notify1 = [0] * 30
        self.notify2 = [0] * 30
        i = 0
 
        #self.grid = QGridLayout(self.notify)
        self.grid = self.notify.gridLayout
        self.grid.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM notifys ORDER BY id DESC LIMIT 20'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        for zeile in zeilen:
            self.notify1[i] = QLabel(f'{zeile[2]} : {zeile[1]}')
            self.notify1[i].setAlignment(Qt.AlignTop)
            self.grid.addWidget(self.notify1[i], i, 0)
   
            i += 1
        

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
        getpath = os.path.join(bundle_dir, 'main.ui')

        self = uic.loadUi(getpath, self)

        self.framelayout = QGridLayout(self.frameSite)
        self.framelayout.setAlignment(Qt.AlignTop)
        self.testLabel.mousePressEvent = self.open_test
        self.testLabel_2.mousePressEvent = self.open_page2
        
        self.labelNews.mousePressEvent = self.showNotify

        self.timerDay = QTimer()
        self.timerDay.setInterval(1000)
        self.timerDay.timeout.connect(self.calculateThings)
        self.timerDay.start()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.printRess)
        self.timer.start()
        
        self.notifyWindow = NotifyWindow()
        
    def showNotify(self, event):
        self.notifyWindow.show()
        
        

    def calculateThings(self):
        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM user WHERE id = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        nahrung = zeilen[0][2]
        holz = zeilen[0][3]
        wasser = zeilen[0][4]
        
        HolzArb = 0
        zeilen = self.getBauten(1)
        if zeilen:
            HolzArb = zeilen[0][4]
            
        bauern = 0
        zeilen = self.getBauten(2)
        if zeilen:
            bauern = zeilen[0][4]
            
        fischer = 0
        zeilen = self.getBauten(5)
        if zeilen:
            fischer = zeilen[0][4]
            
        wassertraeger = 0
        zeilen = self.getBauten(5)
        if zeilen:
            wassertraeger = zeilen[0][4]

        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        gesamtEinwohner = len(zeilen) 
        
        self.nahrung = nahrung + ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (gesamtEinwohner * (1 / 300)))
        self.holz = holz + (HolzArb * ((10 / 10) / 60))
        self.wasser = wasser + (wassertraeger * (1 / 200))
        
        exucute = f'UPDATE user set nahrung = "{self.nahrung}", holz = "{self.holz}", wasser = {self.wasser} WHERE id = "{self.userid}"'
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
                    calc = ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (gesamtEinwohner * (1 / 300)))
                if rohstoffEr == "holz":
                    calc = (HolzArb * ((10 / 10) / 60))
                if rohstoffEr == "wasser":
                    calc = (wassertraeger * (1 / 200))
                plpr = (rohstoffPl / 100)
                rohstoffnach = rohstoff + (calc * plpr)
                
            if rohstoffMi:
                if rohstoffEr == "nahrung":
                    calc = ((fischer * (1 / 75)) + (bauern * (1 / 100)) - (gesamtEinwohner * (1 / 300)))
                if rohstoffEr == "holz":
                    calc = (HolzArb * ((10 / 10) / 60))
                if rohstoffEr == "wasser":
                    calc = (wassertraeger * (1 / 200))
                plpr = (rohstoffMi / 100)

                rohstoffnach = rohstoff - (calc * plpr)
                
            ex = f'UPDATE USER SET {rohstoffEr} = {rohstoffnach} WHERE id = "{self.userid}"'
            cursor.execute(ex)
            connectSql.commit()
            
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
            getpath = os.path.join(bundle_dir, 'warn.png')
            pixmap = QPixmap(getpath)
            self.warnLabel.setPixmap(pixmap)
            
            self.warnLabel.setToolTip(beschreibung)
        else:
            self.warnLabel.clear()
             
        self.calcEinwohner()
        self.calcGeneral()
        self.calcEreignis()
    
    def getBauten(self, gebId):
        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        return zeilen
        
    def calcGeneral(self):
        cursor = connectSql.cursor()
        exucute = f'SELECT * FROM general'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        secondsGone = zeilen[0][0]
        lastEreignis = zeilen[0][1]
        secondsGone += 1
        lastEreignis += 1
        
        exucute = f'UPDATE general SET secondsgone = "{secondsGone}", lastEreignis = "{lastEreignis}"'
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
                hit = random.randint(1, 1000)
                
                if hit >= 980:
                    exucute = f'SELECT * FROM rohstoffereignis'
                    cursor.execute(exucute)
                    zeilen = cursor.fetchall()
                    ereignisRand = random.randint(0, len(zeilen)-1)
                    erId = zeilen[ereignisRand][0]
                    
                    fu.saveNotify(self, zeilen[ereignisRand][1])
                    
                    exucute = f'UPDATE general SET lastEreignis = 0'
                    cursor.execute(exucute)
                    connectSql.commit()
                    
                    ex = f'INSERT INTO rohereignisStart ("erid", "userid", "zeitleft") VALUES ("{zeilen[ereignisRand][0]}", "{self.userid}", "{zeilen[ereignisRand][5]}")'
                    cursor.execute(ex)
                    connectSql.commit()
                    

    def calcEinwohner(self):
        cursor = connectSql.cursor()
        huette = 0
        gesamtAlter = 0
        vorhandenArbeiter = connectSql.commit()
        AnteilZeug = 0
        
        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        
        for zeile in zeilen:
            alter = zeile[2] + (1 / (5 * 60))
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

                maxHit = 2000 / zeugungsGruppen
                hit = random.randint(secWith, round(maxHit))
                
                if hit != 1000:
                            
                    secWith += 1
                    
                    exucute = f'UPDATE user SET secondsWithout = "{secWith}" where id = "{self.userid}"'
                    cursor.execute(exucute)
                    connectSql.commit()
                    
                else:
                    exucute = f'UPDATE user SET secondsWithout = "0" where id = "{self.userid}"'
                    cursor.execute(exucute)
                    connectSql.commit() 
                    
                    exucute = f'INSERT INTO einwohner ("userid", "lebensalter") VALUES ("{self.userid}", "0")'
                    cursor.execute(exucute)
                    connectSql.commit() 
                    
                    fu.saveNotify(self, "Ein neuer Einwohner wurde geboren")
                    
                
        exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}" AND lebensalter > 40'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        for zeile in zeilen:
            
            hit = random.randint(int(zeile[2]), 200)
            if hit == 200:
                if zeile[4] > 0:
                    ex = f'SELECT arbeiter FROM bauten WHERE userid = "{self.userid}" AND gebid = "{zeile[4]}"'
                    cursor.execute(ex)
                    ze = cursor.fetchall()
                    
                    newAn = ze[0][0] - 1
                    
                    ex = f'UPDATE bauten set arbeiter = "{newAn}" WHERE userid = "{self.userid}" AND gebid = "{zeile[4]}"'
                    cursor.execute(ex)
                    connectSql.commit() 
                
                exucute = f'DELETE FROM einwohner WHERE einwohnerid = "{zeile[0]}"'     
                cursor.execute(exucute)
                connectSql.commit() 
                fu.saveNotify(self, "Ein Einwohner ist Gestorben") 
                
            else:
                add = zeile[3] + (1 / (5 * 60))
                exucute = f'UPDATE einwohner SET notDead = "{add}" WHERE einwohnerid = "{zeile[0]}"'
                cursor.execute(exucute)
                connectSql.commit()  
                         
            

           
    def open_test(self, event):
        self.clearLayout(self.framelayout)
        im.test(self)

    def open_page2(self, event):
        self.clearLayout(self.framelayout)
        im.gebaeude(self)

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
        
        exucute = f'SELECT * FROM user WHERE id = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        self.nahrung = zeilen[0][2]
        self.holz = zeilen[0][3]
        self.wasser = zeilen[0][4]
            
        self.labelNahrung.setText(
            f'Nahrung: {str(round(self.nahrung, 2))} Holz: {str(round(self.holz, 2))} Wasser: {str(round(self.wasser, 2))} Freie Arbeiter : {str(freiArbeiter)}')

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
