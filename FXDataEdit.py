#coding:utf-8

import createTradeResult

FIRST_YEAR = 2000
LAST_YEAR = 2015

if __name__ == "__main__":
    
    inFileNames = []
    for i in range(FIRST_YEAR,LAST_YEAR+1):
        inFileName = 'input/DAT_MT_USDJPY_M1_%04d.csv' % i
        inFileNames.append(inFileName)

#    create_Xchart.create_Xchart(60*24,inFileNames,"output/1day_2000-2015.csv")

    createTradeResult.createTradeResult('input/')