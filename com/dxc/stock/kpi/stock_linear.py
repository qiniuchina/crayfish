#!/usr/bin/env python
# coding=utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import tushare as ts
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.metrics import hamming_loss
import seaborn as sns
from sqlalchemy import create_engine
from datetime import datetime, date, timedelta
import traceback
import time
#损失函数，一般有梯度下降法和最小二乘法两种极小化损失函数的优化方法,而scikit-learn中的LinearRegression类使用的是最小二乘法
def init_transit_data():
    stock_code = 'sh'
    df = ts.get_hist_data('sh').head(500)
    # df = ts.get_hist_data('600343').head(500)
    # dftest=df[:10]
    # df = df[10:-1]
    df['close_y']=df['close']
    df['close_y']=df['close_y'].shift(-1)
    dfxy=df[:len(df)-1]
    x=dfxy[['open','close','high','low','volume','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20']]
    # x = dfxy[['open', 'close', 'high', 'low', 'volume']]
    y=dfxy['close_y']
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    # X_train, y_train = x,y
    # dftest['close_y'] = dftest['close']
    # dftest['close_y'] = dftest['close_y'].shift(-1)
    # dftestxy = dftest[:len(dftest) - 1]
    # X_test = dftestxy[
    #     ['open', 'close', 'high', 'low', 'volume', 'price_change', 'p_change', 'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10',
    #      'v_ma20']]
    # x = dfxy[['open', 'close', 'high', 'low', 'volume']]
    # y_test = dftestxy['close_y']
    # print(X_train)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)

    # print(y_pred)
    # 均方根误差
    print('平方误差(MSE)', metrics.mean_squared_error(y_test, y_pred))
    # 均方根误差
    print('均方根误差(RMSE)',np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    #需要得到每个输出的R2，可以使用sklearn.matrics中的r2_score函数
    print('R平方：',metrics.r2_score(y_test, y_pred))
    # 训练后模型截距
    print('模型截距:',linreg.intercept_)
    # 训练后模型权重
    print('模型权重:',linreg.coef_)
    # 获取模型的score值
    print('模型的score值', linreg.score(X_test, y_test))

    df1 = df.head(1)
    x1 = df1[['open','close','high','low','volume','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20']]
    # x1 = df1[['open','close','high','low','volume']]
    y_pred1 = linreg.predict(x1)
    flag =-2
    if y_pred1>x1.iloc[0, 2]:
        print('今天的数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1,'预测明天会涨')
        flag =1
    elif y_pred1==x1.iloc[0, 2]:
        print('今天的指数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1, '预测明天不会有波动')
        flag = 0
    else:
        print('今天的指数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1,'预测明天会跌')
        flag = -1
    furture_date_str=getDatetimeFurther()
    data = [[stock_code,furture_date_str , x1.iloc[0, 2], flag, -2, 0]]
    df = pd.DataFrame(data, columns=['stock_code', 'real_date_str', 'prev_price', 'pred_result', 'real_result','curr_price'])
    df.set_index(['stock_code', 'real_date_str'])
    print(df)
    engine = create_engine("mysql+pymysql://happy:qiniuno.1@115.28.165.184:3306/darklight?charset=utf8", max_overflow=5)
    furture = engine.execute(
        "select * from stock_index_pred where stock_code=%s and real_date_str=%s",
        (stock_code, furture_date_str))
    furture_row = furture.fetchone()
    print('furture_row:', furture_row)
    if furture_row == None:
        df.to_sql('stock_index_pred', engine, if_exists='append')
    date_str = getDatetimeToday()
    print("select stock pred:", stock_code, date_str)
    cur = engine.execute(
        "select * from stock_index_pred where stock_code=%s and real_date_str=%s",
        (stock_code, date_str))
    cur_row= cur.fetchone()
    print('cur_row:',cur_row)
    if cur_row != None:
        print("update stock pred:", stock_code, date_str)
        flag1 =-2
        if  x1.iloc[0, 2] > cur_row[4]:
            flag1 = 1
        elif x1.iloc[0, 2] < cur_row[4]:
            flag1 =-1
        elif x1.iloc[0, 2] == cur_row[4]:
            flag1 =0

        try:
            engine.execute(
                "UPDATE stock_index_pred SET real_result=%s, curr_price=%s  where stock_code=%s and real_date_str=%s",
                (flag1, float(x1.iloc[0, 2]),stock_code, date_str))
            # raise
        except Exception:
            traceback.print_exc()
    # 这里画图真实值和预测值的变化关系，离中间的直线y=x直接越近的点代表预测损失越低
    # plt.figure()
    # plt.plot(X_test['close'], y_pred, 'b', label="predict")
    # plt.plot(X_test['close'], y_test, 'r', label="test")
    # plt.legend(loc="upper right")  # 显示图中的标签
    # plt.xlabel("the number of sales")
    # plt.ylabel('value of sales')
    # plt.show()

    # fig, ax = plt.subplots()
    # ax.scatter(y_test, y_pred)
    # ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    # ax.set_xlabel('Measured')
    # ax.set_ylabel('Predicted')
    # # plt.show()
    #
    # #这里推荐使用的是seaborn包。这个包的数据可视化效果比较好看。其实seaborn也应该属于matplotlib的内部包seaborn的pairplot函数绘制X的每一维度和对应Y的散点图。
    # # 通过设置size和aspect参数来调节显示的大小和比例。可以从图中看出，open特征和close是有比较强的线性关系的，volume和明天的收盘价线性关系更弱。
    # # 通过加入一个参数kind='reg'，seaborn可以添加一条最佳拟合直线和95%的置信带
    # sns.pairplot(dfxy, x_vars=['open', 'close', 'high','low','volume'], y_vars='close_y', size=7, aspect=0.8, kind='reg')
    # plt.show()
    # print(X_test)
    # xMatData = np.zeros([len(X_test), 3], dtype=np.float32)
    # for index in range(len(X_test)):
    #     xMatData[index][0] = y_test[index]
    #     xMatData[index][1] = y_pred[index]
    #     xMatData[index][2] = X_test.iat[index, 2]
    #     # xMatData[index][3] = X_test.index[index]
    # print(xMatData)
    # labels = y_test.index
    # print(type(labels))
    # xdata = len(y_test.index)
    # print(xdata)
    # fig, ax = plt.subplots()
    # ax.plot(xMatData)
    # ax.set_xticks(range(len(labels)))
    # ax.set_xticklabels(labels)
    # plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    # plt.show()
def getDatetimeToday():
    t = date.today()  # date类型
    # dt = datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime
    ds = datetime.strftime(t, '%Y-%m-%d')
    return ds
def getDatetimeFurther():
    t = date.today()  # date类型
    dt = datetime.strptime(str(t), '%Y-%m-%d')  # date转str再转datetime
    further = dt + timedelta(days=1)  # 加一天
    ds = datetime.strftime(further, '%Y-%m-%d')
    return ds

if __name__ == '__main__':
    init_transit_data()


