import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_application.utils import *
from dash_application.app import app
import dash_bootstrap_components as dbc
from collections import OrderedDict
from plotly import graph_objs as go

mapbox_access_token = "pk.eyJ1IjoiY29sbGlucy1lbWFzaSIsImEiOiJjazl6aTgzdn" \
                      "UwOGJrM2dxcmNqdzBpYWJhIn0.KyaoBCDDKFxe3ofQNd-fKw"


# Layout for dash application
layout = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    style={
                        "margin-left": "2%",
                        'margin-right': "2%",
                    },
                    children=[
                        dbc.Col(
                            html.Div(
                                children=[
                                    # Change to side by side for mobile layout
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        className='heading-county-summary',
                                                        children=[
                                                            html.H2("COUNTY SUMMARY"),
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className="county-summary-parag",
                                                        children=[
                                                            html.P(id='county-summary'),
                                                        ]
                                                    ),

                                                ]
                                            ),
                                            html.Div(
                                                className="div-for-dropdown",
                                                children=[
                                                    # Dropdown for locations on map
                                                    dcc.Dropdown(
                                                        id='county-dropdown',
                                                        options=[
                                                            {"label": i, "value": i}
                                                            for i in counties_with_constituencies()
                                                        ],
                                                        placeholder="Select a County",
                                                    )
                                                ],
                                            ),
                                            html.Div(
                                                className="div-for-dropdown",
                                                children=[
                                                    # Drop down to select sub county
                                                    dcc.Dropdown(
                                                        id='sub-county-dropdown',
                                                        placeholder="Select a Sub-County",
                                                    )
                                                ],
                                            ),
                                        ],
                                    ),
                                    dcc.Markdown(
                                        children=[
                                            "Source: [Press Releases](https://health.go.ke/press-releases)"
                                        ]
                                    ),
                                    dcc.Markdown(
                                        children=[
                                            "Source: [Global Source](https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/)"
                                        ]
                                    ),
                                    dcc.Location(id='url', refresh=False),
                                ],
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.Div(
                                children=[
                                    dcc.Graph(id='map-graph'),
                                ],
                            ),
                            width=6
                        ),
                        dbc.Col(
                            html.Div(
                                children=[
                                    html.H2("WORLD RESULTS"),
                                    html.P(id='total-cases'),
                                    html.P(id="total-deaths"),
                                    html.P(id="total-recovered"),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                className='heading-county-summary',
                                                children=[
                                                    html.H2("COUNTRIES SUMMARY"),
                                                ]
                                            ),
                                            html.Div(
                                                className="county-summary-parag",
                                                style={
                                                    "height": "11em",
                                                },
                                                children=[
                                                    html.P(id='global-summary'),
                                                ]
                                            ),

                                        ]
                                    ),
                                ]

                            ),
                            width=3
                        )
                    ],
                    align='start',
                ),
            ]
        )
    ]
)


# Update the list of the sub county drop down
@app.callback(
    Output("sub-county-dropdown", "options"),
    [Input("county-dropdown", "value")]
)
def update_list_constituencies(county):
    if county is None:
        return []
    all_const = counties_with_constituencies()
    constituencies = [const for const in all_const[county]]
    return [{"label": i, "value": i} for i in constituencies]


# update the global confirmed cases
@app.callback(
    Output("total-cases", "children"),
    [Input("county-dropdown", "value")]
)
def update_global_confirmed(_):
    confirmed, _, _ = get_global_results()
    confirmed = confirmed/1000000
    return f"Total confirmed cases: {round(confirmed, 2)}M+"


# update the global confirmed deaths
@app.callback(
    Output("total-deaths", "children"),
    [Input("county-dropdown", "value")]
)
def update_global_deaths(_):
    _, deaths, _ = get_global_results()
    if deaths >= 1000000:
        deaths /= 1000000
        return f"Total confirmed deaths: {round(deaths, 2)}M+"
    deaths /= 1000
    return f"Total confirmed deaths: {round(deaths, 1)}K+"


# update the global confirmed recoveries
@app.callback(
    Output("total-recovered", "children"),
    [Input("county-dropdown", "value")]
)
def update_global_recoveries(_):
    _, _, recoveries = get_global_results()
    recoveries /= 1000000
    return f"Total confirmed recoveries: {round(recoveries, 2)}M+"


# Show the summary of all the countries
@app.callback(
    Output("global-summary", "children"),
    [Input("county-dropdown", "value")]
)
def show_global_summary(_):
    output = []
    for i in range(len(sorted_countries)):
        output += ('{0}: {1} cases'.format(sorted_countries[i][0], sorted_countries[i][1])), html.Br(), ''
    return output


# Shows the summary of all the counties
@app.callback(
    Output("county-summary", "children"),
    [Input("county-dropdown", "value")]
)
def show_kenya_summary(_):
    counties = get_counties_and_cases()
    sorted_counties = OrderedDict(sorted(counties.items(), key=lambda x: x[1], reverse=True))
    output = []
    for county, index in sorted_counties.items():
        output += ('{0}: {1}'.format(county, index), html.Br(), '')
    return output


# Update the map
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("sub-county-dropdown", "value"),
    ],
)
def update_map(county, subcounty):
    zoom = 5.0
    lat_initial = -1.2921
    long_initial = 36.8219
    bearing = 0

    # Also add for only county selection
    if county and subcounty:
        zoom = 5.0
        lat_initial = counties_constituencies_coords[county][subcounty]["Lat"]
        long_initial = counties_constituencies_coords[county][subcounty]["Long"]
    scale = 100

    return go.Figure(
        data=[
            # Data for all regions
            go.Scattermapbox(
                lat=confirmed_global["Lat"],
                lon=confirmed_global["Long"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=with_text['Text'],
                marker=go.scattermapbox.Marker(
                    showscale=False,
                    color='red',
                    opacity=0.9,
                    size=8,
                ),
            ),
            # Have here plot of kenya on the map
            go.Scattermapbox(
                lat=kenya_data['Lat'],
                lon=kenya_data['Long'],
                mode='markers',
                hoverinfo='text',
                text=kenya_data['County'] + ": " + kenya_data[ke_date].astype(str),
                marker=go.scattermapbox.Marker(
                    showscale=False,
                    color='red',
                    opacity=1.0,
                    size=10,
                ),
            ),
        ],
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=20, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=lat_initial, lon=long_initial),
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
        ),
    )
