#coding:utf-8

import sqlite3 as sqlite
import csv


class DBHelperTest:

    DB_PATH  = "db/fxdata.db"
    TABLE_NAME = "chart1min"
    CREATE_TABLE_STRING = "id integer PRIMARY KEY AUTOINCREMENT, time text, firstPrice float, highPrice float, lowPrive float, endPrice float"
    TABLE_COLUMNS = "time, firstPrice, highPrice, lowPrive, endPrice"

    def __init__(self):

        # コネクションの確立。複数のコネクションを張る予定は無いのでEXCLUSIVEで
        self.connection = sqlite.connect(self.DB_PATH, isolation_level='EXCLUSIVE')
        self.cursor = self.connection.cursor()
        sqlStr = "CREATE TABLE " + self.TABLE_NAME + " ("+ self.CREATE_TABLE_STRING+");"
        self.cursor.execute(sqlStr)

    def add(self, time, fp, hp, lp, ep):
        # データ追加用のSQL文の作成
        sqlStr = "INSERT INTO " + self.TABLE_NAME + " ("+self.TABLE_COLUMNS+") VALUES('"\
            + str(time) + "', '"\
            + str(fp) + "', '"\
            + str(hp) + "', '"\
            + str(lp) + "', '"\
            + str(ep) + "');"

        self.cursor.execute(sqlStr)

    def commit(self):
        self.connection.commit()

    def close(self):
        cursor.close()


def push2DB(inFileNames):

    
    # DBHelperの作成
    dbHelper = DBHelperTest()

    # 受け取ったファイルを順番に加工して出力
    for inFileName in inFileNames:

        print(inFileName+"を加工中")

        rf = open(inFileName, 'r')
        dataReader = csv.reader(rf)

        for row in dataReader:

            time = create_Xchart.generateTime(row)
            # DBに挿入
            dbHelper.add(time, row[2], row[3], row[4], row[5])

    # コミット
    dbHelper.commit()

if __name__ == "__main__":

    FIRST_YEAR = 2000
    LAST_YEAR = 2015

    LAST_MONTH2016 = 5

    inFileNames = []
    for i in range(FIRST_YEAR,LAST_YEAR+1):
        inFileName = 'input/DAT_MT_USDJPY_M1_%04d.csv' % i
        inFileNames.append(inFileName)

    for j in range(1,LAST_MONTH2016+1):
        inFileName = 'input/DAT_MT_USDJPY_M1_2016%02d.csv' % j
        inFileNames.append(inFileName)

    push2DB(inFileNames)