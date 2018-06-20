#!/usr/bin/env python
# coding=utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
# import statsmodels.api as sm
import statsmodels.formula.api as smf
import tushare as ts

if __name__ == '__main__':
    df = ts.get_k_data('600343').tail(20)
    x = df[['open','high','low']]
    y = df['close']
    # result = sm.OLS(y,sm.add_constant(x)).fit()
    result = smf.ols(formula='close ~ open + high + low', data=df).fit()  # 方法二
    y_pred = result.predict(x)

    df['price_pred'] = y_pred
    print(df)
    print(result.summary())
    print(result.params)
