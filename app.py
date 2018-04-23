#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:48:53 2018

@author: bartlomiejparka
"""

import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table_experiments as dt

import pandas as pd
from pandas import DataFrame, read_csv
from datetime import datetime
import numpy as np

import plotly.plotly as py

import plotly
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
plotly.offline.init_notebook_mode(connected=True)


key_array = []

df = pd.read_csv(
    '/Users/bartlomiejparka/Documents/Resourcing App/data.csv', skiprows = 1)

df.dropna(0, how='all', inplace = True)

df1 = pd.to_datetime(df.iloc[:, 0], format="%d/%m/%Y")

for i in df1:
    key_array.append(i.strftime('%Y-%m'))

df.loc[:,'Key'] = pd.Series(np.asarray(key_array), index=df.index)

uniquevalues = np.unique(df[(df['Status'] == 'Searching')]['Key'].values)
uniquevalues1 = np.unique(df[(df['Status'] == 'Proposed')]['Key'].values)
uniquevalues2 = np.unique(df[(df['Status'] == 'Withdrawn')]['Key'].values)
uniquevalues3 = np.unique(df[(df['Status'] == 'On Hold')]['Key'].values)
uniquevalues4 = np.unique(df[(df['Status'] == 'Confirmed')]['Key'].values)
uniquevalues5 = np.unique(df[(df['Status'] == 'Closed')]['Key'].values)
uniquevalues6 = np.unique(df[(df['Status'] == 'Unset')]['Key'].values)

lsof_uniques = [uniquevalues,uniquevalues1,uniquevalues2,uniquevalues3,uniquevalues4,uniquevalues5,uniquevalues6]

statuses = ['Searching', 'Proposed', 'Withdrawn', 'On Hold', 'Confirmed', 'Closed', 'Unset']

final_x = []
final_y = []

n = 0

for x in lsof_uniques:
    xlist = []
    ylist = []
    for i in x:
        tot = df[(df['Key'] == i) & (df['Status'] == statuses[n])]['Key'].value_counts()
        ylist.append(int(tot))
        xlist.append(i)
    n = n + 1
    final_x.append(xlist)
    final_y.append(ylist)


trace3 = go.Bar(
    x=final_x[2],
    y=final_y[2],
    name='Withdrawn'
)
trace1 = go.Bar(
    x=final_x[0],
    y=final_y[0],
    name='Searching'
)
trace2 = go.Bar(
    x=final_x[1],
    y=final_y[1],
    name='Proposed'
)
trace4 = go.Bar(
    x=final_x[3],
    y=final_y[3],
    name='On Hold'
)
trace5 = go.Bar(
    x=final_x[4],
    y=final_y[4],
    name='Confirmed'
)
trace6 = go.Bar(
    x=final_x[5],
    y=final_y[5],
    name='Closed'
)
trace7 = go.Bar(
    x=final_x[6],
    y=final_y[6],
    name='Unset'
)

data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7]
layout = go.Layout(
    barmode='stack'
)


app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure={
            'data': data,
            'layout': layout
        }
    ),
    
    html.Div(dt.DataTable(
    rows= df.to_dict('records'), # initialise the rows
    row_selectable=True,
    filterable=True,
    sortable=True,
    selected_row_indices=[],
    id='datatable'
))
    
])




@app.callback(
    Output('datatable', 'rows'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    key = datetime.strptime(clickData['points'][0]['x'], '%Y-%m-%d').strftime('%Y-%m')
    lsof_curves = []
    lsof_statuses = []
    for i in range(len(clickData['points'])):
        lsof_curves.append(clickData['points'][i]['curveNumber'])
    for i in enumerate(statuses):
        if i[0] in lsof_curves:
            lsof_statuses.append(i[1])
    dfnew = df[(df.Status.isin(lsof_statuses)) & (df['Key'] == key)]
    return dfnew.to_dict('records')


'''@app.callback(
    Output('datatable', 'selected_row_indices'),
    [Input('basic-interactions', 'clickData')],
    [State('datatable', 'selected_row_indices')])
def display_click_data(clickData, selected_row_indices):
    date = clickData['points'][0]['x']
    lsof_curves = []
    lsof_statuses = []
    for i in range(len(clickData['points'])):
        lsof_curves.append(clickData['points'][i]['curveNumber'])
    for i in enumerate(statuses):
        if i[0] in lsof_curves:
            lsof_statuses.append(i[1])
    dfnew = df.Status.isin(lsof_statuses)
    for i in range(len(dfnew)):
        if dfnew[i] == True:
            selected_row_indices.append(i)
    return selected_row_indices'''



if __name__ == '__main__':
    app.run_server(debug=True)