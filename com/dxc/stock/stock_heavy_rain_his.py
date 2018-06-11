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

engine = create_engine("mysql+pymysql://root:123456@16.158.102.166:3306/darklight?charset=utf8", max_overflow=5)
def worker(stock):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    df_all =ts.get_k_data(stock)
    df = df_all.tail(5)
    #print('stock:',stock)
    k=3
    day_data=df.iloc[k:(k+1)]
    if day_data['close'].size<=0:
        print("day data is null", day_data['close'], day_data['open'],pd.isnull(day_data))
    else:
        day1 = df.iloc[k:k+1]
        day1_open=day1['open'].values
        day1_close = day1['close'].values
        day2 = df.iloc[k+1:k+2]
        day2_open = day2['open'].values
        day2_close = day2['close'].values
        day2_date = day2['date'].values
        #第二天的收盘价低于开盘价
        if all(day2_close < day2_open) :
            # 第一天的收盘价大于开盘价
            if all(day1_close >day1_open):
                day1var = (day1_close - day1_open)/(day1_close + day1_open)
                # 第一天的收盘价与开盘价的差值足够大
                if day1var > 0.1:
                    # 第二天的收盘价低于第一天的开盘价
                    if all(day2_close < day1_open):
                        #定义上升趋势，连续两期收益率为正
                        day01 = df.iloc[k-1:k]
                        day02 = df.iloc[k - 2:k - 1]
                        day03 = df.iloc[k - 3:k - 2]
                        ret01 = day01['close'].values / day02['close'].values - 1
                        ret02 = day02['close'].values / day03['close'].values - 1
                        if all(ret01>0) and all(ret02>0):
                            print('heavy rain stock: ',day_data['date'].values , stock)
                            # 写入数据
                            # 执行SQL
                            print("sql engine:", engine,stock,day2_date[0])
                            cur = engine.execute(
                                "select * from kpi_heavy_rain where stock_code=%s and stage_date_str=%s",
                                (stock, day2_date[0]))
                            if cur.fetchone() == None:
                                print("sql new stock:", stock, day2_date[0])
                                engine.execute(
                                    "INSERT INTO kpi_heavy_rain (stock_code,stage_date_str,stage_comments) VALUES (%s, %s,'倾盆大雨')",(stock,day2_date[0]))

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