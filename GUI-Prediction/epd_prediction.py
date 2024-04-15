#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 00:35:32 2024

@author: zhangliangkai
"""

import sklearn.datasets as datasets
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
# 导入数据
dataset = pd.read_excel("EPD-data-3.18.xlsx")

# 计算25th和75th分位数的值
# 计算pocp_total的25th和75th分位数的值
q25 = dataset['gwp_100_total'].quantile(0.25)
q75 = dataset['gwp_100_total'].quantile(0.75)


IQR = q75 - q25

max = q75 + 1.5 * IQR
min = q25 - 1.5 * IQR


# 创建一个布尔数组，表示dataset中的pocp_total是否在25th和75th分位数之间
mask = (dataset['gwp_100_total'] >= min) & (dataset['gwp_100_total'] <= max)



# 用布尔索引筛选出dataset中满足条件的行，得到新的dataframe，名字叫result
dataset = dataset[mask]
# 准备训练数据
# 自变量：state_AL到Agg_content

X = dataset.iloc[:, 3:97]
y = dataset.iloc[:, 100]# GWP-100-Total

y1=dataset.iloc[:,97]  #GWP-100-A1
y2=dataset.iloc[:,98]  #GWP-100-A2
y3=dataset.iloc[:,99]  #GWP-100-A3

# 将数据分为训练集和测试集
from sklearn.model_selection import train_test_split
#GWP-100-total
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=0)
regr = RandomForestRegressor()

#GWP-100-A1
X1_train, X1_test, y1_train, y1_test = train_test_split(X,
                                                    y1,
                                                    test_size=0.2,
                                                    random_state=0)
regr1 = RandomForestRegressor()

#GWP-100-A2
X2_train, X2_test, y2_train, y2_test = train_test_split(X,
                                                    y2,
                                                    test_size=0.2,
                                                    random_state=0)
regr2 = RandomForestRegressor()

#GWP-100-A3
X3_train, X3_test, y3_train, y3_test = train_test_split(X,
                                                    y3,
                                                    test_size=0.2,
                                                    random_state=0)
regr3 = RandomForestRegressor()



# 特征缩放，通常没必要
# 因为数据单位，自变量数值范围差距巨大，不缩放也没问题
#from sklearn.preprocessing import StandardScaler

#sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)#

# 训练随机森林解决回归问题
def runPrediction(pred_data=None):
    from sklearn.ensemble import RandomForestRegressor

    regressor = RandomForestRegressor(n_estimators=200, random_state=0)
    regressor.fit(X_train, y_train)
    # y_pred = regressor.predict(X_test)

    regressor1 = RandomForestRegressor(n_estimators=200, random_state=0)
    regressor1.fit(X1_train, y1_train)

    regressor2 = RandomForestRegressor(n_estimators=200, random_state=0)
    regressor2.fit(X2_train, y2_train)

    regressor3 = RandomForestRegressor(n_estimators=200, random_state=0)
    regressor3.fit(X3_train, y3_train)

    # pred_data = pd.read_excel("EPD-prediction.xlsx")
    new_y_pred = regressor.predict(pred_data)
    print('GWP-100-Total=', round((new_y_pred[0]), 2))

    new_y1_pred = regressor1.predict(pred_data)
    print('GWP-100-A1 =', round((new_y1_pred[0]), 2))

    new_y2_pred = regressor2.predict(pred_data)
    print('GWP-100-A2 =', round((new_y2_pred[0]), 2))

    new_y3_pred = regressor3.predict(pred_data)
    print('GWP-100-A3 =', round((new_y3_pred[0]), 2))

    print('Sum GWP-100-A1,A2,A3 = ',
          round(new_y1_pred[0] + new_y2_pred[0] + new_y3_pred[0], 2))
