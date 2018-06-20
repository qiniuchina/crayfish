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
    print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    # 训练后模型截距
    print(linreg.intercept_)
    # 训练后模型权重
    print(linreg.coef_)
    df1 = df.tail(1)
    x1 = df1[['open', 'close', 'high', 'low', 'volume']]
    y_pred1 = linreg.predict(x1)
    print('today sh index close price is:', x1.iloc[0, 1], 'tommorrow sh index price maybe:', y_pred1)
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


