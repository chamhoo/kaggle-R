#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 23:15:35 2018

@author: leechh
"""

# INPUT with any rows


import gc
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize


def fuck():
    n = 1
    errorchunk = pd.read_csv('/home/leechh/data/R/test_v2.csv', nrows=5000, chunksize=100)
    for subchunk in errorchunk:    
        if n == 41:
            df = subchunk.copy()
        n = n+1
    return df

def checkerrorplace():
    n = 1
    errorchunk = pd.read_csv('/home/leechh/data/R/train_v2.csv', chunksize=1)
    for subchunk in errorchunk:
        try:
            col = subchunk.hits.apply(replacehits)
            n = n + 1
            del col, subchunk
        except json.JSONDecodeError as e:
            print(e,' in: ',n)

def todict(dic, key, value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic


def resolve_json(hitsdic, hits_json, key='NoneName'):
    if type(hits_json) == list:
        if len(hits_json) == 0:
            pass
        else:
            for subjson in hits_json:
                hitsdic = resolve_json(hitsdic, subjson)
    elif type(hits_json) == dict:
        for i in hits_json.keys():
            hitsdic = resolve_json(hitsdic, hits_json[i],i)
    else:
        hitsdic = todict(hitsdic, key, hits_json)
    return hitsdic


def replacehits(x):
    dic = {}
    return resolve_json(dic, json.loads(x.replace('\'','\"'). \
                                        replace('TRUE','true'). \
                                        replace('True','true'). \
                                        replace('FALSE','false'). \
                                        replace('False','false'). \
                                        replace(', \"',', !&~'). \
                                        replace('\", ','!&~, '). \
                                        replace('\": ','!&~: '). \
                                        replace(': \"',': !&~'). \
                                        replace(' {\"',' {!&~'). \
                                        replace('\"}, ','!&~}, '). \
                                        replace('[{\"','[{!&~'). \
                                        replace('\"}]','!&~}]'). \
                                        replace('\"','_'). \
                                        replace('!&~','\"'). \
                                        encode('gbk','ignore'). \
                                        decode('utf-8','ignore'). \
                                        replace('\\','')))


def replace(x):
    return  json.loads(x)


def load_df(csv_path, nrows=None, chunksize=10_000, percent=100):
    n=1
    df_list = []
    JSON_COLUMNS = ['device', 'hits','geoNetwork', 'totals', 'trafficSource']
    chunk = pd.read_csv(csv_path,
                        nrows=nrows, 
                        chunksize=chunksize, 
                        dtype={'fullVisitorId': 'str'}) # Important!!
    for subchunk in chunk:
        for column in JSON_COLUMNS:
            if column == 'hits':
                column_as_df = json_normalize(subchunk[column].apply(replacehits))
            else:
                column_as_df = json_normalize(subchunk[column].apply(replace))
            column_as_df.columns = [f'{column}_{subcolumn}' for subcolumn in column_as_df.columns]
            subchunk.drop(column, axis=1, inplace=True)
            subchunk = subchunk.reset_index(drop=True).merge(column_as_df,
                                           right_index=True,
                                           left_index=True)
        # Drop the repeated feature.
        '''
        for i in subchunk.columns:
            if sum(subchunk[i] == subchunk[i][0]) == subchunk.shape[0]:
                subchunk.drop([i], axis=True, inplace=True)
        '''
        n = n+1
        df_list.append(subchunk.astype('str'))
        del column_as_df, subchunk
    return pd.concat(df_list, ignore_index=True)

#if __name__ == '__main__':
#train = load_df('/home/leechh/data/R/train_v2.csv',nrows=100, chunksize=10)