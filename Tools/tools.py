#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 12:44:41 2018

@author: leechh
"""
# This function is build to convert a single string to what actually it is.
#like a list, a int, a float, a bool or just a string.
import numpy as np
import pandas as pd


def strtolist(string):
    try:
        if string == 'nan':
            string = np.nan
        else:
            string = eval(string)
    except:
        pass
    return string


# 这个函数用于将一个 多层list展开，
# *注意：在使用此函数时，需要提前准备一个empty list
def expendstr(df_list,lst):
    if type(lst) == list:
        for i in lst:
            df_list = expendstr(df_list, i)
    else:
        df_list.append(lst)
    return df_list


#针对hits，用于找出所有单一值的hits feature。
def feakhits(df):
    feaklist = []
    for i in df.columns:
        df_list = []
        df_list = expendstr(df_list,df[i].tolist())
        if df_list.count(df_list[0])+df_list.count(np.nan) == len(df_list):
            feaklist.append(i)
    return feaklist


def cclen(x):
    if type(x) == list:
        lenx = len(x)
    else:
        lenx = 0
    return lenx


def describeinfo(df, hitsname):
    lens = df[hitsname].apply(cclen)
    cals = len(set(expendstr([], df[hitsname].tolist())))
    print(f'{hitsname} class: {cals} totallen: {len(lens)} len0: {sum(lens==0)} len1: {sum(lens==1)} biglen: {sum(lens>1)}')


