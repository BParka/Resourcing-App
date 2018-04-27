#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:48:53 2018

@author: bartlomiejparka
"""

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

key_array = []

df_init = pd.read_csv(
    '/Users/bartlomiejparka/Documents/Resourcing App/grmt_resource_requests.csv')

df_top_table = pd.read_csv(
    '/Users/bartlomiejparka/Documents/Resourcing App/toptable.csv')

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

def generate_table(dataframe, max_rows=8):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    generate_table(df_top_table),
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
    #resizable=True,
    #selected_row_indices=[],
    #column_widths=([50] * len(col_list_keep)),
    #min_width=500,
    columns=col_list_keep,
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

if __name__ == '__main__':
    app.run_server(debug=True)