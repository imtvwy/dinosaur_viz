import geopandas as gpd
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Setup app and layout/frontend
app = Dash(__name__)
server = app.server


# read data
dino_df = pd.read_csv("data/processed/dino_info.csv")
dino_names = dino_df["name"].sort_values().unique()
period_list = ['Early Jurassic','Mid Jurassic','Late Jurassic','Early Cretaceous','Late Cretaceous']


# App Layout
app.layout = html.Div([
    html.Div(
        html.H1("Dino in the World", style={'font-weight': 'bold', 'font-size':'30px', 'color':'white'}),
        style={'padding': '10px', 'background': '#732626', 'text-align': 'center'}),
    html.Div([
        html.Div([dcc.Graph(id="dino_map")],  style={'width': '60%', 'float':'left', 'display': 'inline-block'}),
        html.Div([
        html.P("Map Background:", style={'font-weight': 'bold'}),
        dcc.Dropdown(
                id='theme',
                options={
                    'open-street-map': 'open-street-map',
                    'stamen-watercolor': 'stamen-watercolor'
                },
                value='open-street-map',
                style={'width': '80%', 'display': 'inline-block'}
        ),
        html.P("Period:", style={'font-weight': 'bold'}),
        dcc.Checklist(period_list, period_list, id='period'),
        html.P("Dinosaur:", style={'font-weight': 'bold'}),
        dcc.Dropdown(
                id='dino_name',
                options=[{'value': x, 'label': x} 
                    for x in dino_names],
                value='',
                multi=True,
                style={'width': '80%', 'display': 'inline-block'}),
        html.P("Diet:", style={'font-weight': 'bold'}),
        dcc.Checklist(dino_df.diet.unique(), dino_df.diet.unique(), id='dino_diet'),
        ],  style={'width': '20%', 'float':'right'})
    ])
])


# Set up callbacks/backend
@app.callback(
   Output("dino_map", "figure"), 
   [Input("theme", "value"),
    Input("period", "value"),
    Input("dino_name", "value"),
    Input("dino_diet", "value")])
def display_map(theme, period, dino_name, dino_diet):
    map_df = dino_df
    if(period!=''):
        map_df["period_short"]=map_df["period"].str.split().str.get(0) + " " + map_df["period"].str.split().str.get(1)
        map_df = map_df.query('period_short in @period')
    print(map_df)
    if(len(dino_name)!=0 and dino_name!=''):
        map_df = map_df.query('name in @dino_name')
    print(map_df)
    if(dino_diet!=''):
        map_df = map_df.query('diet in @dino_diet')
    print(map_df)
    fig = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lng",
        mapbox_style=theme,
        center=dict(lat=0, lon=0),
        zoom=1.5,
        width=1200,
        height=800,
        hover_name="name",
        hover_data=["period", "diet", "type", "length"],
        opacity=0.3,
        color="name",
        size="length",
        size_max=15

    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)