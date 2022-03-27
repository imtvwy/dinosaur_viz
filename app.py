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



app.layout = html.Div([
    html.P("Dinosaur:"),
    dcc.Dropdown(
            id='dino_name',
            options=[{'value': x, 'label': x} 
                 for x in dino_names],
            value='',
            multi=True,
            style={'width': '80%', 'display': 'inline-block'}),
    html.P("Diet:"),
    dcc.Checklist(dino_df.diet.unique(), dino_df.diet.unique(), id='dino_diet'),
    dcc.Graph(id="dino_map"),
])


# Set up callbacks/backend
@app.callback(
   Output("dino_map", "figure"), 
   [Input("dino_name", "value"),
   Input("dino_diet", "value")])
def display_map(dino_name, dino_diet):
    map_df = dino_df
    if(len(dino_name)!=0 and dino_name!=''):
        map_df = dino_df.query('name in @dino_name')
    if(dino_diet!=''):
        map_df = map_df.query('diet in @dino_diet')
    fig = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lng",
        #mapbox_style="open-street-map",
        mapbox_style="open-street-map",
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