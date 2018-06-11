#Author:Haiyan

#!/usr/bin/python3
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
#参数num代表前面几期，不能小于0,最多能取30期.
def night_end_worker_now(stock,end_date, *num):
    # print('预测黄昏之星 :',stock, end_date)
    df_all = ts.get_k_data(stock,start='2018-01-01',end=end_date)
    count = 30
    k = count-2
    if(len(num))!=0:
        if num[0] > 1 and num[0] <=10:
            count+=1
            k+=1
    df = df_all.tail(count)
    # print(df)
    day_data = df.iloc[k:(k + 1)]
    # print(day_data)
# tail(x) 是返回最后x行数据 Returns last n rows of each group
    if day_data['close'].size<=0:
        print("day data is null",stock,pd.isnull(day_data))
    else:
        maxval = day_data['close'].values + day_data['close'].values* 0.005
        minval = day_data['close'].values - day_data['close'].values* 0.005
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
                        print('night end stock: ', day3_date, stock)
                        return True

__all__ =('night_end_worker_now')

if __name__ =='__main__':
    print(night_end_worker_now('300643','2018-06-04'))

