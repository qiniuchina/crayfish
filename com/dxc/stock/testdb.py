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
from datetime import datetime, date, timedelta


engine = create_engine("mysql+pymysql://happy:qiniuno.1@115.28.165.184:3306/darklight?charset=utf8", max_overflow=5)
if __name__ == '__main__':
    # data = [['sh', '2018-07-05', 2756.12,1,-2,0]]
    # df = pd.DataFrame(data, columns=['stock_code', 'real_date_str','prev_price','pred_result','real_result','curr_price'])
    # df.set_index(['stock_code','real_date_str'])
    # print(df)
    # df.to_sql('stock_index_pred', engine, if_exists='append')
    cur = engine.execute(
        "select * from stock_index_pred where stock_code=%s and real_date_str=%s",
        ('sh', '2018-07-05'))
    cur_row = cur.fetchone()
    print('cur_row:', cur_row)
    print('cur_row:', cur_row[4])
    if 2755< cur_row[4]  :
        print('跌')
    pass
