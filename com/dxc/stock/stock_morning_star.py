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

#创建引擎
engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3307/darklight?charset=utf8", max_overflow=5)
def worker(stock):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    df_all =ts.get_k_data(stock)
    df = df_all.tail(5)
    # print('stock:',stock)
    k=3
    day_data=df.iloc[k:(k+1)]
    if day_data['close'].size<=0:
        print("day data is null", day_data['close'], day_data['open'],pd.isnull(day_data))
    else:
        maxval = day_data['close'].values + day_data['close'].values* 0.005
        minval = day_data['close'].values - day_data['close'].values* 0.005
        # print("day data floor",minval,maxval, day_data['open'].values)
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
            if all(day1_close < day1_open):
                    # print("day3",day3_close,day3_open,day3_close.size)
                    if all(day3_close > day3_open) and day3_close.size>0:
                        day3_diff=day3_close - day3_open
                        day1_mean =(day1_open - day1_close)/2
                        # print("day3 and day1 ", day3_diff, day1_mean)
                        if all(day3_diff >= day1_mean):
                            # print("day2, day3 and day1")
                            if all(day2_close<day1_close) and all(day2_open<day1_close):
                                if all(day2_close<day3_close) and all(day2_open<day3_open):
                                    day01=df.iloc[k-2:k-1]
                                    day02 = df.iloc[k - 3:k - 2]
                                    day03 = df.iloc[k - 4:k - 3]
                                    ret01 = day01['close'].values / day02['close'].values - 1
                                    ret02 = day02['close'].values / day03['close'].values - 1
                                    # print("判断是否下跌趋势：",stock,day_data['date'].values,ret01,ret02)
                                    if all(ret01 < 0) and all(ret02 < 0):
                                        print('morning star stock: ',day_data['date'].values , stock)
                                        # 写入数据

                                        # 执行SQL
                                        print("sql engine:", engine,stock,day3_date[0])
                                        cur = engine.execute(
                                            "INSERT INTO kpi_morning_star (stock_code,stage_date_str,stage_comments) VALUES (%s, %s,'早晨之星')",(stock,day3_date[0]))

start_time = time.strftime('%Y-%m-%d %H:%M:%S')
print('start time:',start_time)
with open('./stocks') as f:
    try:
        executor = futures.ThreadPoolExecutor(max_workers=5)
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