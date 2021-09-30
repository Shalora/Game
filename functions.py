import sqlite3
import time
import os
import subprocess


bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'user.db')
connectSql = sqlite3.connect(getpath)
cursor = connectSql.cursor()
    

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

