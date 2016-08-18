#coding:utf-8

import csv  
import numpy as np
import time
import datetime


#1分足のチャートからX分足のチャートを作成する
# 中途半端な分足や時間足には対応していない。(例：13分足や5時間足など、公約数で無い数値)
def create_Xchart(Xmin, inFileNames, outFileName):

    # 1分足を一時的に取り込むための配列。(始値,高値,安値,終値)の4要素
    tmp1minChart = []

    wf = open(outFileName, 'a') #ファイルが無ければ作る、の'a'を指定
    dataWriter = csv.writer(wf,lineterminator='\n')

    errorFileName = "output/errorlog_" + str(Xmin) + "min" + datetime.datetime.now().strftime('%Y%m%d') + ".log"
    wf_error = open(errorFileName,'a')
    errorWriter = csv.writer(wf_error,lineterminator='\n')

    # 現在とひとつ前、どの時刻からのX分足を算出しているかを保持する
    thisTime = None
    prevTime = None

    # 受け取ったファイルを順番に加工して出力
    for inFileName in inFileNames:

        print(inFileName+"を加工中")

        rf = open(inFileName, 'r')
        dataReader = csv.reader(rf)

        for row in dataReader:

            # 1分足の時刻を取得
            minChartTime = generateTime(row[:2])

            # 前行がX分区切りの最後の行だった場合、結合して書き出し
            if thisTime is not None and minChartTime >= thisTime + datetime.timedelta(minutes=Xmin):
                combined = combine1minChart(thisTime,tmp1minChart)
                dataWriter.writerow(combined)

                # 抜けてるデータがあったら前後の時刻をログに書きだし
                if isTimeFollowed(thisTime,prevTime,Xmin) == False:
                    errorWriter.writerow([prevTime,thisTime])
            
                # 現在の時刻をひとつ前の時刻とする。
                prevTime = thisTime
                thisTime = None
            

            # 最初の1行目、または前行がX分区切りの最後の行だった場合
            if thisTime == None:
                thisTime = generateTime(row[:2],Xmin)
                # 1分足の一時保存用の配列を初期化
                tmp1minChart.clear()

            # 各要素を保持
            tmp1minChart.append(row[2:])

# 日足のリストからX分足を作成する
def combine1minChart(thisTime, columns):

    XminChart = [""]*5
    XminChart[0] = thisTime
    XminChart[1:] = columns[0][0:4]

    for row in columns:
        # 安値の更新
        if float(XminChart[2]) > float(row[1]):
            XminChart[2] = row[1]
        # 高値の更新
        if float(XminChart[3]) < float(row[2]):
            XminChart[3] = row[2]
        # 終値の更新
        XminChart[4] = row[3]

    return XminChart

# csvファイルから読み取った最初の2列から時刻データを作成
# Xminの値を受け取っていると、Xmin区切りの直近の時刻を返す
# 例) Xmin = 30  columsの時刻 = 12:43 の場合、 12:30を返す。
def generateTime(colums, Xmin=0):
    # csvファイルから日付、時刻を取得
    tmpDate = colums[0].split(".")
    tmpTime = colums[1].split(":")
    
    # Xminに値が入っている場合(マイナスは無視)    
    # TODO 1時間足までしか正しく対応できないので、他の場合の対応を出来るように修正が必要
    # 2時間足以上の場合
    if Xmin > 0:
        tmpTime[1] = str(int(tmpTime[1]) - int(tmpTime[1]) % Xmin ) 

    genTime = datetime.datetime(year=int(tmpDate[0]), month=int(tmpDate[1]), day=int(tmpDate[2]), hour=int(tmpTime[0]), minute=int(tmpTime[1]))

    return genTime

# 時刻が飛んでるか確認する
def isTimeFollowed(thisTime,  prevTime, Xmin):

    if thisTime is None or prevTime is None:
        return True

    timeDif = int((thisTime - prevTime).total_seconds())

    if timeDif == Xmin*60:
        return True

    return False

