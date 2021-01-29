import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import numpy as np

import plotly.express as px


# import some pre created and available styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initiate plotly app, with css style imported
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# define some standard styling
colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

# create app layout
app.layout = html.Div([
    # core elements
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True  # Allow multiple files to be uploaded
    ),
    html.Div([html.Small('Acceptable file extensions: .csv, .xls, .xlsx, .txt, .tsv')], style={'marginLeft': '10px'}),
    dcc.Graph(id='Mygraph'),
    html.Div(id='output-data-upload')
])


def parse_data(contents, filename):
    """ parse targeted data file types """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    return df


@app.callback(
    Output('Mygraph', 'figure'),
    [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename')
    ])
def update_graph(contents, filename):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }

    fig = {}
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        # df = df.set_index(df.columns[0])
        # fig['data'] = df.iplot(asFigure=True, kind='scatter', mode='lines+markers', size=1)

        fig = px.scatter(df)
        fig.update_traces(mode='lines+markers')
        fig.update_layout(clickmode='event+select')
    return fig


@app.callback(
    Output('output-data-upload', 'children'),
    [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename')
    ]
)
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            )
        ])

    return table


if __name__ == '__main__':
    app.run_server(debug=True)
