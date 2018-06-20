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
#损失函数，一般有梯度下降法和最小二乘法两种极小化损失函数的优化方法,而scikit-learn中的LinearRegression类使用的是最小二乘法
def init_transit_data():
    df = ts.get_k_data('sh').tail(100)
    df['close_y']=df['close']
    df['close_y']=df['close_y'].shift(-1)
    dfxy=df[:len(df)-1]
    x=dfxy[['open','close','high','low','volume']]
    y=dfxy['close_y']
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)
    # print(y_pred)
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
    df1 = df.tail(1)
    x1 = df1[['open', 'close', 'high', 'low', 'volume']]
    y_pred1 = linreg.predict(x1)
    if y_pred1>x1.iloc[0, 1]:
        print('今天的上证指数收盘价是:', x1.iloc[0, 1], '预测明天大概价格:', y_pred1,'预测明天的大盘会涨')
    else:
        print('今天的上证指数收盘价是:', x1.iloc[0, 1], '预测明天大概价格:', y_pred1,'预测明天的大盘会跌')
    # 做ROC曲线
    plt.figure()
    plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
    plt.plot(range(len(y_pred)), y_test, 'r', label="test")
    plt.legend(loc="upper right")  # 显示图中的标签
    plt.xlabel("the number of sales")
    plt.ylabel('value of sales')
    plt.show()
if __name__ == '__main__':
    init_transit_data()


