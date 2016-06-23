#coding:utf-8

import sqlite3 as sqlite
import csv
import datetime 

class DBHelper:

    DB_PATH  = "db/fxdata.db"
    TABLE_NAME = "chart1min"
    CREATE_TABLE_STRING = None
    TABLE_COLUMNS = "time, firstPrice, highPrice, lowPrice, endPrice"

    def __init__(self):

        # コネクションの確立。複数のコネクションを張る予定は無いのでEXCLUSIVEで
        self.connection = sqlite.connect(self.DB_PATH, isolation_level='EXCLUSIVE')
        self.cursor = self.connection.cursor()

    # テーブルに追加するデータをリストで指定
    def read(self):

        # データ追加用のSQL文の作成
        sqlStr = "SELECT "+self.TABLE_COLUMNS+" FROM " + self.TABLE_NAME + " order by time;"
        print(sqlStr)
        self.cursor.execute(sqlStr)

        chartList = []
        dateFormat = "%Y-%m-%d %H:%M:%S"

        for row in self.cursor:
            time = datetime.datetime.strptime(row[0],dateFormat)
            tmp = [time, float(row[1]), float(row[2]), float(row[3]), float(row[4])]
            chartList.append(tmp)

        return chartList

    def close(self):
        self.cursor.close()
