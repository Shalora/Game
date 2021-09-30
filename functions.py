import sqlite3
import time
import os
import subprocess


bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'user.db')
connectSql = sqlite3.connect(getpath)
cursor = connectSql.cursor()

def getRohstoffe(self):
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM user WHERE id = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchone()
    rohstoffe = {
        "nahrung": zeilen[2],
        "holz": zeilen[3],
        "wasser": zeilen[4],
        "stein": zeilen[6],
        "papier": zeilen[7]
    }
    return rohstoffe


def saveNotify(self, notify):
    self.labelNews.setText(notify)
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%d.%m.%Y %H:%M:%S", named_tuple)
    self.labelNews.setText(f'{time_string} - {notify}')
    exucute = f'INSERT INTO notifys ("message", "zeit") VALUES ("{notify}", "{time_string}")'
    cursor.execute(exucute)
    connectSql.commit()
    subprocess.Popen(['notify-send', f'{time_string} - {notify}'])

def checkBuildings(self):
    exucute = f'SELECT * FROM einwohner where userid = "{self.userid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    einwohner = len(zeilen)


    exucute = f'SELECT * FROM gebaeude'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    for zeile in zeilen:

        if not zeile[5]:
            if zeile[4] <= einwohner:

                ex = f'UPDATE gebaeude set unlock = TRUE where id = "{zeile[0]}"'
                cursor.execute(ex)
                connectSql.commit()

def changeStimmungAll(self, change):
    exucute = f'SELECT * FROM einwohner'
    cursor.execute(exucute)
    zeilen = cursor.fetchall()
    for zeile in zeilen:
        stimmung = zeile[5] + change
        ex = f'Update einwohner set zufriedenheit = {stimmung} where einwohnerid = {zeile[0]}'
        cursor.execute(ex)
        connectSql.commit()

def calcKette(self, verbrauch, verbrauchWert, erzeugt, erzeugtWert, gebid):
    rohstoffe = getRohstoffe(self)
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM bauten WHERE gebid = "{gebid}"'
    cursor.execute(exucute)
    bauten = cursor.fetchone()

    if bauten:
        if bauten[3]:
            if verbrauchWert <= rohstoffe[verbrauch]:
                arbeiter = bauten[4]

                rohstoffe[verbrauch] = rohstoffe[verbrauch] - (verbrauchWert / 5 / 60 * arbeiter)
                rohstoffe[erzeugt] = rohstoffe[erzeugt] + (erzeugtWert / 5 / 60 * arbeiter)

                ex = f'Update user set {verbrauch} = {rohstoffe[verbrauch]}, {erzeugt} = {rohstoffe[erzeugt]}' \
                     f' where id = {self.userid}'
                cursor.execute(ex)
                connectSql.commit()

def getForschung(self, forid):
    cursor = connectSql.cursor()
    exucute = f'SELECT * FROM forschung WHERE forid = "{forid}"'
    cursor.execute(exucute)
    zeilen = cursor.fetchone()
    return zeilen





