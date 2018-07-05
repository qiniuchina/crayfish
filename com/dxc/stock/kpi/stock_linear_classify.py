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
from sklearn.svm import SVC
#用于标准化数据
from sklearn.preprocessing import StandardScaler
#一种线性分类技术
from sklearn.linear_model import LogisticRegression
#一种线性分类技术
from sklearn.linear_model import SGDClassifier
#用于分析数据
from sklearn.metrics import classification_report
from datetime import datetime

import matplotlib.dates as mdates

def init_transit_data():
    # df = ts.get_hist_data('sh').head(500)
    df = ts.get_hist_data('600343').head(500)
    df['close_y']=df['close']
    df['close_y']=df['close_y'].shift(-1)
    dfxy=df[:len(df)-1]
    x=dfxy[['open','close','high','low','volume','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20']]
    # x = dfxy[['open', 'close', 'high', 'low', 'volume']]
    y=np.where(dfxy['close_y']>dfxy['close'],1,0)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)
    # print(X_test)
    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_test1 = ss.fit_transform(X_test)
    # print(X_test)
    df1 = df.head(1)
    x1 = df1[['open','close','high','low','volume','price_change','p_change','ma5','ma10','ma20','v_ma5','v_ma10','v_ma20']]
    # x1 = df1[['open','close','high','low','volume']]
    # y_pred1 = classifier.predict(x1)
    # print('明天股票会：',y_pred1)
    # if y_pred1>x1.iloc[0, 2]:
    #     print('今天的数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1,'预测明天会涨')
    # else:
    #     print('今天的指数收盘价是:', x1.iloc[0, 2], '预测明天大概价格:', y_pred1,'预测明天会跌')
    lr = LogisticRegression()
    sgdc = SGDClassifier()
    lr.fit(X_train, y_train)
    lr_y_predict = lr.predict(X_test1)                                                               #用fit之后的结果对X_test进行预测
    print('lr_y_predict',lr_y_predict)
    x1=ss.fit_transform(x1)
    lr_y_pred1 = lr.predict(x1)
    print('lr_y_pred1', lr_y_pred1)
    sgdc.fit(X_train, y_train)
    sgdc_y_predict = sgdc.predict(X_test1)
    sgdc_y_pred1 = sgdc.predict(x1)
    print('sgdc_y_pred1', sgdc_y_pred1)
    #对X_test的预测结果与y_test进行对比
    print('Accuracy of LR Classifier:', lr.score(X_test, y_test))
    # 输出y_test与预测结果的对比
    print(classification_report(y_test, lr_y_predict, target_names=['跌', '涨']))
    print('Accuarcy of SGD Classifier:', sgdc.score(X_test, y_test))
    print(classification_report(y_test, sgdc_y_predict))
    fig, ax = plt.subplots()
    xs =[datetime.strptime(d, '%Y-%m-%d').date() for d in X_test.index.values]
    ys = y_test
    # 配置横坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.scatter(xs, ys,s=30, marker='o', color='red', zorder=1)
    # ax.scatter(xs, lr_y_predict, s=30, marker='x', color='blue', zorder=1)
    ax.scatter(xs, sgdc_y_predict, s=30, marker='x', color='blue', zorder=1)
    # ax.scatter(xs1, y=dfxy[dfxy['close_y'] < dfxy['close']]['close_y'], s=30, marker='x',color='green', zorder=10)
    # ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel('date')
    ax.set_ylabel('result')
    # plt.plot(xs, ys)
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.show()
if __name__ == '__main__':
    init_transit_data()


