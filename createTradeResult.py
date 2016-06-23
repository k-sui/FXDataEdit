#coding:utf-8

import csv  
import numpy as np
import time
import datetime as dt
from DBHelper import DBHelper
from DBConstants import DBConstants

DB_PATH  = "db/fxdata.db"

# 1分足のチャートを使ってX分足の取引結果を作成する
# profitRate, lossRateは買った時の何倍の上下かを指定(例：1の上下を示す場合は0.01)
def createTradeResult(dbPath, Xmin, resultColumn, profitRate, lossRate):

    # 1分足を一時的に取り込むための配列。(始値,高値,安値,終値)の4要素
    tmp1minChart = []

    # 結果を保存するためのリスト
    resultList =[]

    # 1分足を読み込むためのDBHelper
    chart1minHelper = DBHelper(dbPath, DBConstants.CHART_1MIN_TBL, DBConstants.CHART_COLUMNS)

    # X分足の読み込みと、X分足の結果を書き込むためのDBHelper
    chartXminHelper, resultXminHelper = createXminHelper(dbPath, Xmin)

    # 定期的にコミットするためのループ回数のカウンタ
    count = 0

    # X分足チャートのデータを全てに対して結果を作成する(※カーソルを手放すために配列として全て読み込む)
    for row in chartXminHelper.getCursor().fetchall():

        # 始点とする時刻を作成
        now = dt.datetime.strptime(row[0],DBConstants.TIME_FORMAT)

        # 始点時刻以降の1分足を読みだしていき、結果を作成する
        # 始点の終値でエントリーすることを想定するので、nowの時刻よりXmin後から確認開始
        xminLater = dt.timedelta(minutes=Xmin)
        entryTime = now + xminLater

        # iの時刻の終値を取得(終値でエントリーしたと想定)
        entryPrice = row[4]

        # 買った場合と売った場合の結果を記録する。成功：1, 失敗：0。-1はまだ結果が出ていないことを示す。
        longResult = -1
        shortResult = -1

        # DBに書き込む形の結果。初期値は売り買いどちらも失敗に設定
        result = DBConstants.RESULT_NOR

        for row1min in chart1minHelper.getCursor(time=entryTime):

            # long,shortの両方に結果が出ていれば結果を設定してループを抜ける
            if longResult != -1 and shortResult != -1 :
                if longResult == 1:
                    result = DBConstants.RESULT_BUY
                elif shortResult == 1:
                    result = DBConstants.RESULT_SELL
                else:
                    result = DBConstants.RESULT_NOR
                break

            # longポジションを取る場合の結果の判定
            # 利確する上昇比率(profitRate)を高値が超えていれば記録
            if row1min[2] > entryPrice*(1+profitRate):
                longResult = 1
            if row1min[3] < entryPrice*(1-lossRate):
                longResult = 0

            # shortポジションを取る場合の結果の判定
            # 利確する上昇比率(profitRate)を高値が超えていれば記録
            if row1min[3] < entryPrice*(1-profitRate):
                shortResult = 1
            if row1min[2] > entryPrice*(1+lossRate):
                shortResult = 0

        # TODO DBに書き込み
        resultXminHelper.insertOrUpdate(now, resultColumn, result)

        # カウンタを加算
        count = count + 1

        # 2000回に1回コミット
        if count % 2000 == 0:
            resultXminHelper.commit()


    resultXminHelper.commit()




# 指定された時間間隔用のDBHelperを作成
def createXminHelper(dbPass, Xmin):

    if Xmin == 1:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_1MIN_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_1MIN_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    elif Xmin == 5:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_5MIN_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_5MIN_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    elif Xmin == 10:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_10MIN_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_10MIN_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    elif Xmin == 30:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_30MIN_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_30MIN_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    elif Xmin == 60:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_1HOUR_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_1HOUR_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    elif Xmin == 240:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_4HOUR_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_4HOUR_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    elif Xmin == 1440:
        chartXminHelper = DBHelper(dbPass, DBConstants.CHART_1DAY_TBL, DBConstants.CHART_COLUMNS)
        resultXminHelper = DBHelper(dbPass, DBConstants.RESULT_1DAY_TBL, DBConstants.RESULT_COLUMNS)
        return chartXminHelper, resultXminHelper

    else:
        return None, None

if __name__ == "__main__":
    createTradeResult(DB_PATH, 60, "pro05_loss01", 0.005, 0.001)