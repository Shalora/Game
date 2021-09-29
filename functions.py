import sqlite3
import time
import os


bundle_dir = os.path.dirname(os.path.abspath(__file__))
getpath = os.path.join(bundle_dir, 'user.db')
connectSql = sqlite3.connect(getpath)
cursor = connectSql.cursor()
    

def saveNotify(self, notify):
    self.labelNews.setText(notify)
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%d.%m.%Y, %H:%M:%S", named_tuple)
    exucute = f'INSERT INTO notifys ("message", "zeit") VALUES ("{notify}", "{time_string}")'
    cursor.execute(exucute)
    connectSql.commit()