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
#损失函数，一般有梯度下降法和最小二乘法两种极小化损失函数的优化方法,而scikit-learn中的LinearRegression类使用的是最小二乘法
def init_transit_data():
    # df = ts.get_hist_data('sh').head(500)
    df = ts.get_hist_data('600343').head(500)
    df['close_y']=df['close']
    df['close_y']=df['close_y'].shift(-1)
    dfxy=df[:len(df)-1]
    x=dfxy[['open','close','high','low','volume','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20']]
    y=dfxy['close_y']
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
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
    y_pred1 = linreg.predict(x1)
    if y_pred1>x1.iloc[0, 2]:
        print('今天的数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1,'预测明天会涨')
    else:
        print('今天的指数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1,'预测明天会跌')
    # 这里画图真实值和预测值的变化关系，离中间的直线y=x直接越近的点代表预测损失越低
    plt.figure()
    # plt.plot(X_test['close'], y_pred, 'b', label="predict")
    # plt.plot(X_test['close'], y_test, 'r', label="test")
    # plt.legend(loc="upper right")  # 显示图中的标签
    # plt.xlabel("the number of sales")
    # plt.ylabel('value of sales')
    # plt.show()

    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()
if __name__ == '__main__':
    init_transit_data()


