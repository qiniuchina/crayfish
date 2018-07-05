#!/usr/bin/env python
# coding=utf-8

import time
from concurrent import futures
import traceback
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine
from datetime import datetime, date, timedelta
#早晨之星形态捕捉

#创建引擎
# engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3307/darklight?charset=utf8", max_overflow=5)
engine = create_engine("mysql+pymysql://happy:qiniuno.1@115.28.165.184:3306/darklight?charset=utf8", max_overflow=5)
def worker(stock):
    end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    df_all =ts.get_k_data(stock,start='2018-01-01',end=end_date)
    # 写入数据

    # 执行SQL
    print("sql engine:", engine,stock)
    # conn = Engine.connect()
    # session = Session(bind=conn)
    # trans = conn.begin()
    #
    # user = User(name='2')
    # session.begin_nested()
    # session.add(user)
    # session.commit()
    #
    # session.commit()
    #
    # trans.rollback()


def stock_executor():
    end_date = time.strftime('%Y-%m-%d')
    print('start time:',end_date)
    with open('../stocks') as f:
        try:
            # executor = futures.ThreadPoolExecutor(max_workers=10)
            while True:
                line = next(f).strip()
                print(line)
                df = ts.get_k_data(line)
                # 追加数据到现有表
                if line.startswith('6'):
                    print('sh')
                    df.to_sql('stock_transation_sh', engine, if_exists='append')
                elif line.startswith('0'):
                    print('sz')
                    df.to_sql('stock_transation_sz', engine, if_exists='append')
                elif line.startswith('3') and not(line.startswith('399')):
                    print('cy')
                    df.to_sql('stock_transation_cy', engine, if_exists='append')
                elif line.startswith('sh') or line.startswith('399'):
                    print('index')
                    df.to_sql('stock_transation_index', engine, if_exists='append')
                # task = executor.submit(worker, line)
                # task1 = executor.submit(hr.heavy_rain_worker_now, line, end_date)
                # task2 = executor.submit(ne.night_end_worker_now, line, end_date)
                # task.done()
                # task1.done()
                # task2.done()
            raise
        except StopIteration:
            pass
        except:
            traceback.print_exc()
def getDatetimeToday():
    t = date.today()  # date类型
    dt = datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime
    return dt
def getDatetimeYesterday():
    today = getDatetimeToday()  # datetime类型当前日期
    yesterday = today + timedelta(days=-1)  # 减去一天
    return yesterday

def stock_executor_today():
    end_date=getDatetimeToday().strftime('%Y-%m-%d')
    start_date = getDatetimeYesterday().strftime('%Y-%m-%d')
    print('start time:',end_date,start_date)
    with open('../stocks') as f:
        try:
            # executor = futures.ThreadPoolExecutor(max_workers=10)
            while True:
                line = next(f).strip()
                print(line)
                df = ts.get_k_data(line,start=start_date,end=end_date)
                print('df',df)
                # 追加数据到现有表
                if line.startswith('6'):
                    print('sh')
                    df.to_sql('stock_transation_sh', engine, if_exists='append')
                elif line.startswith('0'):
                    print('sz')
                    df.to_sql('stock_transation_sz', engine, if_exists='append')
                elif line.startswith('3') and not(line.startswith('399')):
                    print('cy')
                    df.to_sql('stock_transation_cy', engine, if_exists='append')
                elif line.startswith('sh') or line.startswith('399'):
                    print('index')
                    df.to_sql('stock_transation_index', engine, if_exists='append')
                # task = executor.submit(worker, line)
                # task1 = executor.submit(hr.heavy_rain_worker_now, line, end_date)
                # task2 = executor.submit(ne.night_end_worker_now, line, end_date)
                # task.done()
                # task1.done()
                # task2.done()
            raise
        except StopIteration:
            pass
        except:
            traceback.print_exc()


if __name__ == '__main__':
    # stock_executor()
    stock_executor_today()
    # print(hr.heavy_rain_worker_now('300643', '2018-06-04'))
    # print(ne.night_end_worker_now('603703', '2018-06-07'))
    # end_date = time.strftime('%Y-%m-%d')
    # df = ts.get_k_data('603703',start=end_date,end=end_date)
    # print(df)
    # engine = create_engine('mysql://user:passwd@127.0.0.1/db_name?charset=utf8')

    # 存入数据库
    # df.to_sql('stock_transation_sh1', engine)

    # 追加数据到现有表
    # df.to_sql('stock_transation_sh1',engine,if_exists='append')