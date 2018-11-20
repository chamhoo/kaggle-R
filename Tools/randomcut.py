#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 12:11:45 2018

@author: leechh
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def idx(percentage, chunksize):
    return [np.random.randint(100) < percentage for i in np.arange(chunksize)]


def randomcut(path, percentage, nrows=None, chunksize=10_000):
    df_list = []
    chunk = pd.read_csv(path, nrows=nrows, chunksize=chunksize)
    for subchunk in chunk:
        idx_list = idx(percentage, subchunk.shape[0])
        df_list.append(subchunk[idx_list])
    return pd.concat(df_list, ignore_index=True)
