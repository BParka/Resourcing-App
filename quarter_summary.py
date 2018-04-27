#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:20:42 2018

@author: bartlomiejparka
"""
from tinydb import TinyDB, Query

import pandas as pd
from pandas import DataFrame, read_csv
from datetime import datetime
import numpy as np

db = TinyDB('db.json')
User = Query()
db.insert({'name': 'John', 'age': 22})
db.search(User.name == 'John')

key_array = []

df_init = pd.read_csv(
    '/Users/bartlomiejparka/Documents/Resourcing App/grmt_resource_requests.csv')

col_list_keep =['Job Title',
 'Status',
 'Openseat Number',
 'Duplicate Seat',
 'Assignment Type',
 'Work Location',
 'Landed',
 'Contract Specification',
 'PgW',
 'Lot',
 'Project Name',
 'Confirmed Candidate',
 'RO Number',
 'Commercial Status',
 'ADAM Grade',
 'No.Required',
 'PRG Band High',
 'PRG Band Low',
 'Open to Contractors',
 'BP Requested Seat?',
 'IBM Requested Start Date',
 'BP Requested Start Date',
 'BP PM',
 'PGW Lead',
 'IBM PM',
 'Job Description',
 'Mandatory Skills',
 'Desirable skills']

result_keep = [df_init[e] for e in col_list_keep]

df = pd.concat(result_keep, axis=1)

df.dropna(0, how='all', inplace = True)

df['IBM Requested Start Date'].replace("\ufeff", "", regex=True, inplace=True)

df1 = pd.to_datetime(df['IBM Requested Start Date'], format="%d/%m/%Y")

for i in df1:
    key_array.append(i.strftime('%Y-%m'))

df.loc[:,'Key'] = pd.Series(np.asarray(key_array), index=df.index)