#coding:utf-8

import sqlite3 as sqlite
import csv

class DBHelper:

    DB_PATH  = "db/fxdata.db"
    TABLE_NAME = None
    CREATE_TABLE_STRING = None
    TABLE_COLUMNS = None

    # createStringが指定されていなければ、既にテーブルはあるものとする。
    def __init__(self, tableName, tableColumns, createString=None):

        self.TABLE_NAME = tableName
        self.TABLE_COLUMNS = tableColumns
        self.CREATE_TABLE_STRING = createString

        # コネクションの確立。複数のコネクションを張る予定は無いのでEXCLUSIVEで
        self.connection = sqlite.connect(self.DB_PATH, isolation_level='EXCLUSIVE')
        self.cursor = self.connection.cursor()

        if self.CREATE_TABLE_STRING is not None:
            sqlStr = "CREATE TABLE " + self.TABLE_NAME + " ("+ self.CREATE_TABLE_STRING+");"
            print(sqlStr)
            self.cursor.execute(sqlStr)

    # テーブルに追加するデータをリストで指定
    def add(self, data):
        if data is None or len(data) ==0:
            return

        # データ追加用のSQL文の作成
        sqlStr = "INSERT INTO " + self.TABLE_NAME + " ("+self.TABLE_COLUMNS+") VALUES('"
        for i in range(len(data)-1):
            sqlStr = sqlStr + str(data[i]) + "', '"

        sqlStr =  str(data[len(data)-1]) + "');"

        self.cursor.execute(sqlStr)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
