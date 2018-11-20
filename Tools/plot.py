#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:27:29 2018

@author: leechh
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append('/home/leechh/code/kaggle-R/Tools/')
from tools import *

# 这个函数用于从四个维度展示 hits feature， 
# 第一个bar图表示在全部数据中某个值的平均占比，
# 第二个bar图表示在确认的购买数据中某个值的平均占比，
# 第三个图表示数量最多的n个值
def listset(x):
    if type(x) == list:
        x = list(set(x))
    return x


def isin(x1, x2):
    x = 0
    if type(x2) == list:
        for i in x2:
            if x1 == i:
                x = 1
    else:
        if x1 == x2:
            x = 1
    return x
            

def plot_hits(origin_df, feature, target='logtarget', top=7, rotation=0):
    df = origin_df.copy()
    plt.figure(figsize=[20, 5])
    plt.subplot(1,4,1)
    full_list = expendstr([], df[feature].tolist())
    full = pd.Series(full_list).value_counts()[:top]/df[feature].shape[0]
    plt.bar(np.arange(full.shape[0])+1,
            full, 
            width=[0.2]*full.shape[0], 
            facecolor='gray', edgecolor='gray',
            tick_label=full.index)
    plt.title(f'*{feature}* full data {len(set(full_list))}')
    plt.xticks(rotation=rotation)
    plt.grid()
    plt.subplot(1,4,2)
    tradeidx = df[target].notnull()
    buy_list = expendstr([], df[tradeidx][feature].tolist())
    buy = pd.Series(buy_list).value_counts()[:top]/df[tradeidx][feature].shape[0]
    plt.bar(np.arange(buy.shape[0])+1, 
            buy,
            width=[0.2]*buy.shape[0], 
            facecolor='gray', edgecolor='gray',
            tick_label=buy.index)
    plt.title(f'*{feature}* confirm trade data {len(set(buy_list))}')
    plt.xticks(rotation=rotation)
    plt.grid()
    plt.subplot(1,4,3)
    idx = list(set(full.index.tolist()+buy.index.tolist()))
    full_data = expendstr([], df[feature].apply(listset).tolist())
    buy_data = expendstr([], df[tradeidx][feature].apply(listset).tolist())
    percent = [buy_data.count(i)/full_data.count(i) for i in idx]
    plt.plot(np.arange(len(idx))+1, 
             [sum(tradeidx)/df[feature].shape[0]]*len(idx),c='salmon')
    plt.bar(np.arange(len(idx))+1,
            percent,
            width=[0.2]*len(idx), 
            facecolor='gray', edgecolor='gray',
            tick_label=idx)
    plt.title(f'*{feature}* percentage')
    plt.xticks(rotation=rotation)
    plt.grid()
    plt.subplot(1,4,4)
    plt.bar(np.arange(buy.shape[0])+1, 
            np.zeros(buy.shape[0]),
            tick_label=buy.index)
    mean = []
    tfp = []
    sfp = []
    for i in buy.index:
        df[f'{feature}_{i}'] = [isin(i,x) for x in df[feature]]
        mean.append(df.groupby(f'{feature}_{i}')[target].describe()['mean'][1])
        tfp.append(df.groupby(f'{feature}_{i}')[target].describe()['25%'][1])
        sfp.append(df.groupby(f'{feature}_{i}')[target].describe()['75%'][1])
    plt.fill_between(np.arange(buy.shape[0])+1, tfp, sfp, color='lightgray')
    plt.plot(np.arange(buy.shape[0])+1, mean, 'k*-')
    plt.ylim([15,20])
    plt.title(f'*{feature}* describe')
    plt.xticks(rotation=rotation)
    plt.grid()
    return None