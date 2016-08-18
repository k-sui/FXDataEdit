#coding:utf-8

from DBHelper import DBHelper


DB_PATH  = "db/fxdata.db"

if __name__ == "__main__":

# チャート用テーブル作成
#    createTableString = "id integer PRIMARY KEY AUTOINCREMENT, time text unique, firstPrice float, highPrice float, lowPrice float, endPrice float"

#    tableName = "chart10min"
#    helper = DBHelper(DB_PATH, tableName, None)
#    helper.createTable(createTableString)

# 結果用テーブル作成
#    createTableString = "id integer PRIMARY KEY AUTOINCREMENT, time text unique, pro05_loss01 integer"

#    tableName = "result1hour"
#    helper = DBHelper(DB_PATH, tableName, None)
#    helper.createTable(createTableString)


# インジケータ用テーブル作成
    createTableString = "id integer PRIMARY KEY AUTOINCREMENT, time text unique, " \
    + "cci float"