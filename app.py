import dash
import dash_core_components as dcc
import dash_html_components as html

# import some pre created and available styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initiate plotly app, with css style imported
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
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
    dcc.Graph(id='Mygraph'),
    html.Div(id='output-data-upload')
])