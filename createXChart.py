#coding:utf-8

import csv  
import numpy as np
import time
import datetime as dt
from DBHelper import DBHelper
from DBConstants import DBConstants
import createTableData

DB_PATH  = "db/fxdata.db"


#1分足のチャートからX分足のチャートを作成する
# 中途半端な分足や時間足には対応していない。(例：13分足や5時間足など、公約数で無い数値)
# 現在は1時間足用にしか作っていない
def createXChart(Xmin):

    # 1分足を一時的に取り込むための配列。(始値,高値,安値,終値)の4要素
    tmpChart1min = []

    # 1分足のチャートを全て読み出すためのヘルパ
    dbHelper1min = DBHelper(DB_PATH, DBConstants.CHART_1MIN_TBL, DBConstants.CHART_COLUMNS)

    # 書き込み用にDBを開く
    dbHelper1hour = DBHelper(DB_PATH, DBConstants.CHART_1HOUR_TBL, DBConstants.CHART_COLUMNS)

    # 現在とひとつ前、どの時刻からのX分足を算出しているかを保持する
    thisTime = None
    prevTime = None

    count = 0

    for row in dbHelper1min.getAllDataCursor().fetchall():


        rowTime = dt.datetime.strptime(row[0],DBConstants.TIME_FORMAT)

        # 1分足の時刻を取得
        minChartTime = generateRoundTime(rowTime,Xmin)

        # 前行がX分区切りの最後の行だった場合、結合して書き出し
        if thisTime is not None and minChartTime >= thisTime + dt.timedelta(minutes=Xmin):
            combined = combine1minChart(thisTime,tmpChart1min)
#            print("added:")
#            print(combined)
            dbHelper1hour.add(combined)
            count = count + 1

            # 現在の時刻をひとつ前の時刻とする。
            prevTime = thisTime
            thisTime = None
            

        # 最初の1行目、または前行がX分区切りの最後の行だった場合
        if thisTime == None:
            thisTime = generateRoundTime(rowTime, Xmin)
            # 1分足の一時保存用の配列を初期化
            tmpChart1min.clear()

        # 各要素を保持
        tmpChart1min.append(row[1:])

        if count % 2000 == 0:
            print("now:")
            print(dt.datetime.now())
            print(prevTime)
            print("")

            # 2000件ごとにコミット
            dbHelper1hour.commit()

            # 何度も引っかかるので加算
            count = count + 1

    # 最後にもコミット
    dbHelper1hour.commit()

# 日足のリストからX分足を作成する
def combine1minChart(thisTime, columns):

    XminChart = [""]*5
    XminChart[0] = thisTime
    XminChart[1:] = columns[0][0:4]

    for row in columns:
        # 高値の更新
        if float(XminChart[2]) < float(row[1]):
            XminChart[2] = row[1]
        # 安値の更新
        if float(XminChart[3]) > float(row[2]):
            XminChart[3] = row[2]
        # 終値の更新
        XminChart[4] = row[3]

    return XminChart

# csvファイルから読み取った最初の2列から時刻データを作成
# Xminの値を受け取っていると、Xmin区切りの直近の時刻を返す
# 例) Xmin = 30  columsの時刻 = 12:43 の場合、 12:30を返す。
def generateRoundTime(time, Xmin=0):
    
    # Xminに値が入っている場合(マイナスは無視)    
    # TODO 1時間足までしか正しく対応できないので、他の場合の対応を出来るように修正が必要
    # 2時間足以上の場合
    if Xmin > 0:
        sec = int(time.second) 
        min = int(time.minute)%Xmin
    rTime = time - dt.timedelta(minutes=min, seconds=sec)

    return rTime

# 時刻が飛んでるか確認する
def isTimeFollowed(thisTime,  prevTime, Xmin):

    if thisTime is None or prevTime is None:
        return True

    timeDif = int((thisTime - prevTime).total_seconds())

    if timeDif == Xmin*60:
        return True

    return False

if __name__ == "__main__":
    createXChart(60)
