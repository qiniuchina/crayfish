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
DAYS = 7
EARN = 10
# engine = create_engine("mysql+pymysql://root:123456@localhost:3307/darklight?charset=utf8", max_overflow=5)
engine = create_engine("mysql+pymysql://happy:qiniuno.1@115.28.165.184:3306/darklight?charset=utf8", max_overflow=5)
def worker(para):
    df_all =ts.get_k_data(code=para[1])
    df_filter = df_all[df_all["date"]>=para[2]]
    rows = df_filter.iloc[:,0].size
    if(rows < DAYS and rows > 0):
        first_close = df_filter.iat[0,2]
        last_close = df_filter.iat[rows-1,2]
        rate = round(((last_close - first_close) / first_close) * 100, 2)
        print(rate)
        engine.execute("UPDATE kpi_morning_star SET day_cut_off_yield=%s where id=%s",(rate.item(), para[0]))
        if(rate.item() >= EARN):
            engine.execute("UPDATE kpi_morning_star SET stage_end_datestr=%s,day_cut_off_yield=%s where id=%s",(time.strftime('%Y-%m-%d'),rate.item(), para[0]))
    elif(rows >= DAYS):
        first_close = df_filter.iat[0,2]
        last_close = df_filter.iat[DAYS-1,2]
        rate = round(((last_close - first_close) / first_close) * 100, 2)
        engine.execute("UPDATE kpi_morning_star SET stage_end_datestr=%s,day_cut_off_yield=%s where id=%s",(time.strftime('%Y-%m-%d'),rate.item(), para[0]))
cur = engine.execute("select * from kpi_morning_star where (stage_end_datestr is null or stage_end_datestr='')")
stocks = cur.fetchall()
print(stocks)
if(len(stocks)>0):
    executor = futures.ThreadPoolExecutor(max_workers=10)    
    for stock in stocks : 
        task = executor.submit(worker, stock)
        task.done()
if __name__ =='__main__':
    pass