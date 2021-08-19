# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

df = px.data.iris() # iris is a pandas DataFrame
fig1 = px.scatter(df, x="sepal_width", y="sepal_length")


app.layout = html.Div(children=[
    html.H1('BOMP: WIP'),

    html.Div(children='''
         Choose a character
    '''),
    dcc.RadioItems(
        id='candidate', 
        options=[{'value': "fds", 'label': "Zolton"},
                 {'value': "fdss", 'label': "Hagen"},
                 {'value': "fdssd", 'label': "Kingsley"}],
        value="fds",
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='scatter_map',config={'scrollZoom':True}),
    dcc.Graph(figure=fig1)
])


@app.callback(
    Output(component_id='scatter_map', component_property='figure'),
    [Input(component_id='candidate', component_property='value')])
def display_scattermap(candidate):

    px.set_mapbox_access_token('pk.eyJ1IjoiY2xpbjI2NSIsImEiOiJja2NuaXpkZjMwMnEyMnJxcGQ4YTM2aTY5In0.4mHf-EjuvLGnivDWEr4uKA')
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    #Note: only mapbox styles that require a token will work, so no "open-street-map" and the like
    fig.update_layout()#mapbox_style="dark")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)