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
#早晨之星形态捕捉

#创建引擎
engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3307/darklight?charset=utf8", max_overflow=5)
def worker(stock):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    df_all =ts.get_k_data(stock)
    #至少取6天以上的数据才可以完整计算模型
    count=6
    df = df_all.tail(count)
    # print('stock:',stock)
    k=count-2
    day_data=df.iloc[k:(k+1)]
    if day_data['close'].size<=0:
        print("day data is null", day_data['close'], day_data['open'],pd.isnull(day_data))
    else:
        maxval = day_data['close'].values + day_data['close'].values* 0.003
        minval = day_data['close'].values - day_data['close'].values* 0.003
        # print("day data floor",minval,maxval, day_data['open'].values)
        # 定义十字星,收盘价和开盘价大致相等
        if all(day_data['open'].values>=minval) and all(day_data['open'].values<=maxval):
            # print('十字星：',stock,day_data['date'].values)
            day1 = df.iloc[k-1:k]
            day1_open=day1['open'].values
            day1_close = day1['close'].values
            day2 = df.iloc[k:k+1]
            day2_open = day2['open'].values
            day2_close = day2['close'].values
            day3 =df.iloc[k+1:k+2]
            day3_open = day3['open'].values
            day3_close = day3['close'].values
            day3_date = day3['date'].values
            # morning star model
            # print('day1:',day1_close,day1_open )
            #第一天的收盘价低于开盘价,并且是一根大阴线
            day1_close_maxval = day1_close + day1_close * 0.01
            # print('day1 close:',day1_close_maxval,day1_open )
            if all(day1_close_maxval < day1_open):
                    # print("day3",day2['date'].values,day3_close,day3_open,day3_close.size)
                    #第三天的收盘价高于开盘价
                    if all(day3_close > day3_open) and day3_close.size>0:
                        day3_diff=day3_close - day3_open
                        day1_mean =(day1_open - day1_close)/2
                        # print("day3 and day1 ", day3_diff, day1_mean)
                        #第三天收盘价和开盘价的差值要大于等于第一天开盘价与收盘价差值的一半
                        if all(day3_diff >= day1_mean):
                            # print("day2, day3 and day1")
                            #第二天的收盘价和开盘价均需小于第一天的收盘价和第三天的开盘价
                            if all(day2_close<day1_close) and all(day2_open<day1_close):
                                if all(day2_close<day3_close) and all(day2_open<day3_open):
                                    day01 = df.iloc[k - 4:k - 3]
                                    day02 = df.iloc[k - 3:k - 2]
                                    day03=df.iloc[k-2:k-1]

                                    ret01 = day02['close'].values / day01['close'].values - 1
                                    ret02 = day03['close'].values / day02['close'].values - 1
                                    print("判断是否下跌趋势：",stock,day_data['date'].values,ret01,ret02)
                                    #定义下跌趋势，目前是第一天前两天连续下跌
                                    if all(ret01 < 0) and all(ret02 < 0):
                                        print('morning star stock: ',day_data['date'].values , stock)
                                        # 写入数据

                                        # 执行SQL
                                        print("sql engine:", engine,stock,day3_date[0])
                                        cur = engine.execute(
                                            "select * from kpi_morning_star where stock_code=%s and stage_date_str=%s",
                                            (stock, day3_date[0]))
                                        if cur.fetchone() == None:
                                            print("sql new stock:", stock, day3_date[0])
                                            engine.execute(
                                                "INSERT INTO kpi_morning_star (stock_code,stage_date_str,stage_comments) VALUES (%s, %s,'早晨之星')",(stock,day3_date[0]))

start_time = time.strftime('%Y-%m-%d %H:%M:%S')
print('start time:',start_time)
with open('./stocks') as f:
    try:
        executor = futures.ThreadPoolExecutor(max_workers=10)
        while True:
            line = next(f).strip()
            task = executor.submit(worker, line)
            task.done()
    except StopIteration:
        pass

# t = Thread(target=worker,args=('002381',))
# t.start()
# end_time = time.strftime('%Y-%m-%d %H:%M:%S')
# print('end time:',start_time)