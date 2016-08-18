#coding:utf-8


class DBConstants(object):

    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    TIME_COLUMN = "time"

    CHART_1MIN_TBL = "chart1min"
    CHART_5MIN_TBL = "chart5min"
    CHART_10MIN_TBL = "chart10min"
    CHART_30MIN_TBL = "chart30min"
    CHART_1HOUR_TBL = "chart1hour"
    CHART_4HOUR_TBL = "chart4hour"
    CHART_1DAY_TBL = "chart1day"
    CHART_COLUMNS = "time, firstPrice, highPrice, lowPrice, endPrice"

    INDICATOR_1MIN_TBL = "indicator1min"
    INDICATOR_5MIN_TBL = "indicator5min"
    INDICATOR_10MIN_TBL = "indicator10min"
    INDICATOR_30MIN_TBL = "indicator30min"
    INDICATOR_1HOUR_TBL = "indicator1hour"
    INDICATOR_4HOUR_TBL = "indicator4hour"
    INDICATOR_1DAY_TBL = "indicator1day"
    INDICATOR_COLUMNS = ""

    RESULT_1MIN_TBL = "result1min"
    RESULT_5MIN_TBL = "result5min"
    RESULT_10MIN_TBL = "result10min"
    RESULT_30MIN_TBL = "result30min"
    RESULT_1HOUR_TBL = "result1hour"
    RESULT_4HOUR_TBL = "result4hour"
    RESULT_1DAY_TBL = "result1day"
    RESULT_COLUMNS = "time, pro05_loss01"

    # 取引結果のDB上での定義
    RESULT_BUY = 1
    RESULT_SELL = -1
    RESULT_NOR = 0

