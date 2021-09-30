from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
import os
import functions as fu

import sqlite3

bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'user.db')

connectSql = sqlite3.connect(getpath)
user = "Shalora"


def test(self):
    self.frameSite.setStyleSheet("background-color: rgb(20, 20, 20)")

    self.label = [0] * 50000
    self.label2 = [0] * 50000
    self.label3 = [0] * 50000
    self.label4 = [0] * 50000
    i = 0
    j = 0
    
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM einwohner WHERE userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    
    for zeile in zeilen:
        j += 1
        self.label[i] = QLabel(f'{j}')
        self.label[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label[i], i, 0)

        self.label4[i] = QLabel(f'{zeile[6]}')
        self.label4[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label4[i], i, 1)
        
        self.label2[i] = QLabel(f'Alter: {round(zeile[2], 1)}')
        self.label2[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label2[i], i, 2)

        self.label3[i] = QLabel(f'Zufriedenheit: {round(zeile[5], 1)}')
        self.label3[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label3[i], i, 3)
        
        i += 1

    self.frameSite.setLayout(self.framelayout)

def forschung(self):
    cursor = connectSql.cursor()
    exucute = 'SELECT * FROM forschung'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    self.label = [0] * 30
    self.label2 = [0] * 30
    self.label3 = [0] * 30
    self.label4 = [0] * 30
    self.buttonFor = [0] * 30

    i = 0
    for zeile in zeilen:
        self.label[i] = QLabel(f'{zeile[1]}')
        self.label[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label[i], i, 0)

        self.label2[i] = QLabel(f'{zeile[2]} * {zeile[3]}')
        self.label2[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label2[i], i, 1)

        kostennext = zeile[4] * (zeile[5] + 1)
        self.label3[i] = QLabel(f'{kostennext} Papier')
        self.label3[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label3[i], i, 2)

        self.buttonFor[i] = QPushButton("Forschen")
        self.buttonFor[i].setStyleSheet("max-width: 60px")
        self.buttonFor[i].clicked.connect(
            lambda checked, text=zeile[0]: forsch(self, text))
        self.framelayout.addWidget(self.buttonFor[i], i, 3)

def gebaeude(self):
    cursor = connectSql.cursor()
    exucute = 'SELECT * FROM gebaeude where unlock = true '
    cursor.execute(exucute)

    zeilen = cursor.fetchall()
    self.label = [0] * 30
    self.label2 = [0] * 30
    self.label3 = [0] * 30
    self.label4 = [0] * 30
    self.label5 = [0] * 30
    self.buttonBau = [0] * 30
    self.buttonPlus = [0] * 30
    self.buttonMinus = [0] * 30
    i = 0

    for zeile in zeilen:
        maxAr = zeile[3]
        self.label[i] = QLabel(f'{zeile[1]}')
        self.label[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label[i], i, 0)

        self.label4[i] = QLabel(f'Holz: {zeile[2]} Stein: {zeile[6]}')
        self.label4[i].setAlignment(Qt.AlignTop)
        self.framelayout.addWidget(self.label4[i], i, 1)

        exucute = f'SELECT * FROM bauten where userid = {self.userid} and gebid = {zeile[0]}'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()

        if zeilen:
            anzahl = zeilen[0][3]
            self.label2[i] = QLabel(f'Anzahl: {anzahl}')
            self.framelayout.addWidget(self.label2[i], i, 2)
            
            if zeile[3]:
                arbeiter = zeilen[0][4]
                maxshow = maxAr * anzahl
                self.label3[i] = QLabel(f'Arbeiter: {arbeiter} / {maxshow}')
                self.framelayout.addWidget(self.label3[i], i, 3)
                
                self.buttonPlus[i] = QPushButton("+")
                self.buttonPlus[i].setStyleSheet("max-width: 10px")
                self.buttonPlus[i].clicked.connect(
                    lambda checked, text=zeile[0]: addWorker(self, text))
                self.framelayout.addWidget(self.buttonPlus[i], i, 5)
                
                self.buttonMinus[i] = QPushButton("-")
                self.buttonMinus[i].setStyleSheet("max-width: 10px")
                self.buttonMinus[i].clicked.connect(
                    lambda checked, text=zeile[0]: delWorker(self, text))
                self.framelayout.addWidget(self.buttonMinus[i], i, 4)
                
        else:
            self.label2[i] = QLabel(f'Anzahl: 0')
            self.framelayout.addWidget(self.label2[i], i, 2)
            
            if zeile[3]:
                self.label3[i] = QLabel(f'Arbeiter: 0')
                self.framelayout.addWidget(self.label3[i], i, 3)
                
                self.buttonPlus[i] = QPushButton("+")
                self.buttonPlus[i].setStyleSheet("max-width: 10px")
                self.buttonPlus[i].clicked.connect(
                    lambda checked, text=zeile[0]: addWorker(self, text))
                self.framelayout.addWidget(self.buttonPlus[i], i, 5)
                
                self.buttonMinus[i] = QPushButton("-")
                self.buttonMinus[i].setStyleSheet("max-width: 10px")
                self.buttonMinus[i].clicked.connect(
                    lambda checked, text=zeile[0]: delWorker(self, text))
                self.framelayout.addWidget(self.buttonMinus[i], i, 4)

        self.buttonBau[i] = QPushButton("Bauen")
        self.buttonBau[i].setStyleSheet("max-width: 40px")

        self.buttonBau[i].clicked.connect(
            lambda checked, text=zeile[0]: gebbau(self, text))
        self.framelayout.addWidget(self.buttonBau[i], i, 6)
        i += 1

    self.frameSite.setStyleSheet("background-color: rgb(20, 20, 20)")

    self.frameSite.setLayout(self.framelayout)

def addWorker(self, gebId):
    
    huette = 0
    vorhandenArbeiter = 0
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
  
    
    if (vorhandenArbeiter + 1) <= maxArbeiter:
        exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        
        if zeilen:
            gebAnz = zeilen[0][3]
            arbeiter = zeilen[0][4]
            
            exucute = f'SELECT * FROM gebaeude where id = "{gebId}"'
            cursor.execute(exucute)
            gebZeilen = cursor.fetchall()
            
            maxNew = gebAnz * gebZeilen[0][3]
            
            if (arbeiter + 1) <= maxNew:
                arbeiter += 1
                exucute = f'UPDATE bauten set arbeiter = "{arbeiter}" where gebid = "{gebId}" and userid = "{self.userid}"'
                cursor.execute(exucute)
                connectSql.commit()
                
                exucute = f'SELECT * FROM einwohner where job = "0" and userid = "{self.userid}" and lebensalter > "12"'
                cursor.execute(exucute)
                lastZeilen = cursor.fetchall() 
                lastid = lastZeilen[len(lastZeilen)-1][0]
                
                exucute = f'UPDATE einwohner set job = "{zeilen[0][0]}" where userid = "{self.userid}" AND einwohnerid = "{lastid}"'
                cursor.execute(exucute)
                connectSql.commit()
                
                gebaeude(self)
            else:
                fu.saveNotify(self, "Kein Platz mehr vorhanden")
                
        else:
            fu.saveNotify(self, "Gebäude nicht gebaut")
            
    else:
        fu.saveNotify(self, "Keine Arbeiter vorhanden")

def delWorker(self, gebId):
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    if zeilen:
        arbeiter = zeilen[0][4]
        if (arbeiter - 1) >= 0:
            arbeiter -= 1
            exucute = f'UPDATE bauten set arbeiter = "{arbeiter}" where gebid = "{gebId}" and userid = "{self.userid}"'
            cursor.execute(exucute)
            connectSql.commit()
            
            exucute = f'SELECT * FROM einwohner where job = "{zeilen[0][0]}" and userid = "{self.userid}"'
            cursor.execute(exucute)
            lastZeilen = cursor.fetchall() 
            lastid = lastZeilen[len(lastZeilen)-1][0]
            
            exucute = f'UPDATE einwohner set job = "0" WHERE userid = "{self.userid}" AND einwohnerid = "{lastid}"'
            cursor.execute(exucute)
            connectSql.commit()
            
            gebaeude(self)
    
def gebbau(self, gebId):
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM gebaeude where id = "{gebId}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    holzKost = zeilen[0][2]
    steinKost = zeilen[0][6]

    rohstoffe = fu.getRohstoffe(self)

    if holzKost <= rohstoffe["holz"] and steinKost <= rohstoffe["stein"]:

        exucute = f'SELECT * FROM bauten where gebid = "{gebId}" and userid = "{self.userid}"'
        cursor.execute(exucute)
        zeilen = cursor.fetchall()
        if zeilen:
            anzahl = zeilen[0][3] + 1
            exucute = f'update bauten set anzahl = "{anzahl}" where gebid = "{gebId}" and userid = "{self.userid}"'
            cursor.execute(exucute)

            rohstoffe["holz"] = rohstoffe["holz"] - holzKost
            rohstoffe["stein"] = rohstoffe["stein"] - steinKost
            exucute = f'update user set holz = "{rohstoffe["holz"]}", stein = {rohstoffe["stein"]} where id = "{self.userid}"'
            cursor.execute(exucute)
            connectSql.commit()
        else:
            exucute = f'insert into bauten ("userid", "gebid", anzahl, arbeiter) VALUES ("{self.userid}", "{gebId}", 1, 0)'
            cursor.execute(exucute)

            rohstoffe["holz"] = rohstoffe["holz"] - holzKost
            rohstoffe["stein"] = rohstoffe["stein"] - steinKost
            exucute = f'update user set holz = "{rohstoffe["holz"]}", stein = {rohstoffe["stein"]} where id = "{self.userid}"'
            cursor.execute(exucute)
            connectSql.commit()

        if gebId == 6 or gebId == 7:
            if gebId == 6:
                fu.changeStimmungAll(self, 3)
            if gebId == 7:
                fu.changeStimmungAll(self, 5)
    else:
        fu.saveNotify(self, "Nicht genügend Rohstoffe vorhanden")
    gebaeude(self)

def forsch(self, forid):
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM forschung WHERE forid = "{forid}"'

    cursor.execute(exucute)
    zeile = cursor.fetchone()
    rohstoffe = fu.getRohstoffe(self)
    kostenpa = (zeile[5] + 1) * zeile[4]
    level = zeile[5]


    if (rohstoffe["papier"] >= kostenpa):
        level = level + 1

        exucute = f'UPDATE forschung SET level = {level} where forid = {forid}'

        cursor.execute(exucute)
        connectSql.commit()

        rohstoffe["papier"] -= kostenpa
        exucute = f'UPDATE user SET papier = {rohstoffe["papier"]} where id = {self.userid}'
        cursor.execute(exucute)
        connectSql.commit()

        forschung(self)
    else:
        fu.saveNotify(self, "Nicht genügend Papier vorhanden")