#!/usr/bin/python3
# coding=utf-8

import pandas as pd
import numpy as np
import tushare as ts
import os
import time
import math
#倾盆大雨形态捕捉
#参数num代表前面几期，不能小于0,最多能取30期.
def heavy_rain_worker_now(stock,*num):
    # print('预测倾盆大雨 :', stock, end_date)
    df_all = ts.get_k_data(stock)
    count=5
    k = count - 2
    if (len(num)) != 0:
        if num[0] > 1 and num[0] <= 30:
            count+=1
            k += 1
    df = df_all.tail(count)
    day_data=df.iloc[k+1:k+2]
    if day_data['close'].size<=0:
        print("day data is null",stock,pd.isnull(day_data))
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
                day1var = (day1_close - day1_open)/day1_open
                # 第一天的收盘价与开盘价的差值足够大
                if day1var > 0.03:
                    # 第二天的收盘价低于第一天的开盘价
                    if all(day2_close < day1_open):
                        #定义上升趋势，连续两期收益率为正
                        day02 = df.iloc[k - 2:k - 1]
                        day03 = df.iloc[k - 1:k]
                        day04 = df.iloc[k:k+1]
                        ret01 = day04['close'].values / day03['close'].values - 1
                        ret02 = day03['close'].values / day02['close'].values - 1
                        if all(ret01>0) and all(ret02>0):
                            print('heavy rain stock: ',day2_date, stock)
                            return True


__all__ =('heavy_rain_worker_now')

if __name__ =='__main__':
    print(heavy_rain_worker_now('300643'))