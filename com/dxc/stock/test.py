#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import numpy as np
import tushare as ts
import os
import time
import math
from concurrent import futures
from sqlalchemy import create_engine

from astropy.units import Ybarn
from datetime import datetime, date, timedelta


#创建引擎
# engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3307/darklight?charset=utf8", max_overflow=5)
# cur = engine.execute( "select * from kpi_morning_star where stock_code=%s and stage_date_str=%s",('600531', '2018-06-05'))
# print("cur:",cur)
# if cur.fetchone() != None:
#     print("cur:",cur.fetchone())
def test(str1, str2):
    print(str1,str2)

def test1(str1):
    print(str1)


def computeCorrelation(X, Y):
    xBar = np.mean(X)
    yBar = np.mean(Y)
    SSR = 0
    varX = 0
    varY = 0
    for i in range(0, len(X)):
        diffXXBar = X[i] - xBar
        diffYYBar = Y[i] - yBar
        SSR += (diffXXBar * diffYYBar)
        varX += diffXXBar ** 2
        varY += diffYYBar ** 2

    SST = math.sqrt(varX * varY)
    return SSR / SST
if __name__ == '__main__':
    # executor = futures.ThreadPoolExecutor(max_workers=10)
    # task=executor.submit(test,'hello','fei')
    # task1 = executor.submit(test1, 'hello')
    # task.done()
    # testX = [1, 3, 8, 7, 9]
    # testY = [10, 12, 24, 21, 34]
    # print(computeCorrelation(testX, testY))
    t = date.today()  # date类型
    df=datetime.strftime(t,'%Y-%m-%d')
    print(df)
    t = date.today()  # date类型
    dt = datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime
    further = dt + timedelta(days=1)  # 加一天
    ds = datetime.strftime(further, '%Y-%m-%d')
    print(ds)
    # end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    pass
