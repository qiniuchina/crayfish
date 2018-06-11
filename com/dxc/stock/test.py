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
# engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3307/darklight?charset=utf8", max_overflow=5)
# cur = engine.execute( "select * from kpi_morning_star where stock_code=%s and stage_date_str=%s",('600531', '2018-06-05'))
# print("cur:",cur)
# if cur.fetchone() != None:
#     print("cur:",cur.fetchone())
def test(str1, str2):
    print(str1,str2)

def test1(str1):
    print(str1)
if __name__ == '__main__':
    executor = futures.ThreadPoolExecutor(max_workers=10)
    task=executor.submit(test,'hello','fei')
    # task1 = executor.submit(test1, 'hello')
    task.done()