#Author:Haiyan

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
#黄昏之星形态捕捉

#创建引擎
# engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/darklight?charset=utf8", max_overflow=5)
def worker(stock):
    df_all = ts.get_k_data(stock)
    df = df_all.tail(50)
    k = 9
    while k < len(df) - 2:
        k += 1
        day_data = df.iloc[k:(k + 1)]
    # tail(x) 是返回最后x行数据 Returns last n rows of each group
        if day_data['close'].size<=0:
            print("day data is null", day_data['close'], day_data['open'],pd.isnull(day_data))
        else:
            maxval = day_data['close'].values + day_data['close'].values* 0.003
            minval = day_data['close'].values - day_data['close'].values* 0.003
            # print("day data floor",minval,maxval, day_data['open'].values)
            # 定义十字星,收盘价和开盘价大致相等
            if all(day_data['open'].values>=minval) and all(day_data['open'].values<=maxval):
                # print('十字星：',stock,day_data['date'].values)
                #找到附近的三天的价格
                day1 = df.iloc[k - 1:k]
                day1_open = day1['open'].values
                day1_close = day1['close'].values
                day1_high = day1['high'].values
                day2 = df.iloc[k:k + 1]
                day2_open = day2['open'].values
                day2_close = day2['close'].values
                day3 = df.iloc[k + 1:k + 2]
                day3_open = day3['open'].values
                day3_close = day3['close'].values
                day3_date = day3['date'].values
                day3_min = day3['low'].values
                # 在升势中出现一支大阳线，股价大幅上扬，幅度较前一日高出4%收盘大于开盘
                # 　第二日：第二日K线较昨日跳开，收盘同样在缺口之上。线性实体狭小，实体长度小于1 %，有上下影线；
                # 解释为：第一天差不多上涨了4%，第二天的开盘价比第一天的收盘价高1%，第二天的收盘价比第一天的最高价高
                if all(day1_close > (day1_open + day1_open * 0.04)) and all(day2_open > (day1_close * 0.001 + day1_close)) and day2_close > day1_high:
                    # 　第三日：阴线，回落到第一支蜡烛下，开盘价小于昨日收盘价，今日的阴线实体长度大于4%：
                    day3_diff = day3_open - day3_close

                    if all(day3_diff > day3_open * 0.04) and day3_open < day2_close and day3_open > day3_close and day3_min < day1_close and day3_close.size > 0:
                        # 判断是否是10天以来的最高价,实质上的要求是20天，可修改范围
                        data_center = 0
                        for i in range(10):
                            if all(data_center < df.iloc[(k - i):(k - i + 1)]['high'].values):
                                # print(i)
                                # print(df.iloc[(k-i):(k-i+1)]['high'].values)
                                data_center = df.iloc[(k - i):(k - i + 1)]['high'].values
                                # print(data_center)
                        if all(data_center <= day_data['high'].values):
                            print('night end stock: ', day_data['date'].values, stock)
                            # 执行SQL
                            # print("sql engine:", engine, stock, day3_date[0])
                            # cur = engine.execute(
                            #     "select * from kpi_morning_star where stock_code=%s and stage_date_str=%s",
                            #     (stock, day3_date[0]))
                            # if cur.fetchone() == None:
                            #     print("sql new stock:", stock, day3_date[0])
                            #     engine.execute(
                            #         "INSERT INTO kpi_morning_star (stock_code,stage_date_str,stage_comments) VALUES (%s, %s,'早晨之星')",
                            #         (stock, day3_date[0]))


start_time = time.strftime('%Y-%m-%d %H:%M:%S')
print('start time:', start_time)
with open('./stocks') as f:
                try:
                    executor = futures.ThreadPoolExecutor(max_workers=5)
                    while True:
                        line = next(f).strip()
                        task = executor.submit(worker, line)
                        task.done()
                except StopIteration:
                    pass
