import dash
import dash_html_components as html
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewpoint", "content": "width=device-width"}
    ],
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css", 'dash_application/assets/style.css', dbc.themes.BOOTSTRAP]
)

server = app.server
app.head = [
    html.Link(
        href='assets/favicon.ico',
        rel='icon',
    )
]
app.title = 'COVID-19 KENYA DASHBOARD'
server = app.server
mapbox_access_token = "pk.eyJ1IjoiY29sbGlucy1lbWFzaSIsImEiOiJjazl6aTgzdnUwOGJrM2dxcmNqdzBpYWJhIn0.KyaoBCDDKFxe3ofQNd-fKw"


# Layout for dash application
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            style={
                "text-align": "center",
                "margin-top": "1.8rem",
                "margin-left": "10%",
                "margin-right": "10%",
                "padding-top": "1.8rem",
                "width": "80%",
                "font-size": "150%",
                "color": "##bdbdbd",
                "font-weight": "400",
            },
            children=[
                html.Img(
                    className="logo",
                    style={
                        "float": "left",
                    },
                    src=app.get_asset_url("logo1.png"),
                ),
                html.Img(
                    className="logo",
                    style={
                        "float": "right"
                    },
                    src=app.get_asset_url("logo1.png"),
                ),
                html.H1("CORONA VIRUS DISEASE KENYA DASHBOARD: HEAT MAP AND DATA ANALYSIS TOOL"),
            ]
        ),
        html.Div(
            className='row wrapper',
            style={
                "text-align": "center",
                "display": "inherit",
                "margin-bottom": "10px",
            },
            children=[
                html.Div(
                    className='row',
                    style={
                        "background": "#292929",
                        "margin-left": "2%",
                        "margin-right": "2%",
                        "text-align": "center",
                        "width": "80%",
                        "display": "inline-block",
                        "justify-content": "space-around",
                        "overflow-x": "auto",
                    },
                    children=[
                        html.Div(
                            className='summary-heading',
                            style={
                                "display": "inline-block",
                                "margin": "0 auto",
                                "float": "left",
                                "padding": "3px",
                                "width": "20%",
                            },
                            children=[
                                html.P("+0 in past 24hrs", className='hrs-24', id='c-hrs-element'),
                                html.H1("0", className='cases-num', id='cases-element'),
                                html.P("CASES", className='cases-text'),
                            ]
                        ),
                        html.Div(
                            className='summary-heading',
                            style={
                                "display": "inline-block",
                                "margin": "0 auto",
                                "padding": "3px",
                                "float": "center",
                                "width": "20%"
                            },
                            children=[
                                html.P("+ 24 in past 24hrs", className='hrs-24', id="r-hrs-element"),
                                html.H1("0", className='recovered-num', id='recovered-element'),
                                html.P("RECOVERIES", className='recovered-text'),
                            ]
                        ),
                        html.Div(
                            className='summary-heading',
                            style={
                                "display": "inline-block",
                                "padding": "3px",
                                "margin": "0 auto",
                                "float": "right",
                                "width": "20%"
                            },
                            children=[
                                html.P("+ 24 in past 24hrs", className='hrs-24', id='d-hrs-element'),
                                html.H1("0", className='deaths-num', id='deaths-element'),
                                html.P("DEATHS", className='deaths-text'),
                            ]
                        ),
                    ]
                ),

            ]

        ),
        html.Div(
            className='row',
            children=[
                # Column for user control
                html.Div(
                    className="four columns div-user-controls",
                    style={
                        "width": "24%",
                        "padding-top": "0px",
                    },
                    children=[
                        # Change to side by side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className='row',
                                    children=[
                                        html.Div(
                                            className='heading-county-summary',
                                            children=[
                                                html.H2("COUNTY SUMMARY"),
                                            ]
                                        ),
                                        html.Div(
                                            className="row county-summary-parag",
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
                        html.P(id="kenya-total-cases"),
                        html.P(id="kenya-total-recoveries"),
                        html.P(id="kenya-total-deaths"),
                        dcc.Markdown(
                            children=[
                                "Source: [Press Releases](https://health.go.ke/press-releases)"
                            ]
                        ),
                        dcc.Markdown(
                            children=[
                                "Source: [Global Source](https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/)"
                            ]
                        )
                    ],
                ),
                # Column for global summary
                html.Div(
                    className="four columns div-user-controls",
                    style={
                        "float": "right",
                        "width": "25%",
                        "margin-left": "1%",
                        "margin-right": "1%",
                        "padding-top": "0px",
                    },
                    children=[
                        html.H2("WORLD RESULTS"),
                        html.P(id='total-cases'),
                        html.P(id="total-deaths"),
                        html.P(id="total-recovered"),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='heading-county-summary',
                                    children=[
                                        html.H2("COUNTRIES SUMMARY"),
                                    ]
                                ),
                                html.Div(
                                    className="row county-summary-parag",
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

                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    style={
                        "float": "left",
                        "display": "flex",
                        "flex-direction": "right",
                        "height": "65vh",
                        "width": "45%",
                        "background-color": "#31302F",
                    },
                    children=[
                        dcc.Graph(id='map-graph'),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            style={
                "display": "inline-block",
                "text-align": "center",
                "margin-top": "1.8rem",
                "margin-left": "10%",
                "margin-right": "10%",
                "padding-top": "1.8rem",
                "width": "80%",
                "color": "##bdbdbd",
            },
            children=[
                html.H2("OTHER SUMMARY DOCUMENT WOULD GO HERE"),
                html.Div(
                    className="eight four columns",
                    style={
                        "display": "inline-block",
                        "margin": "0 auto",
                        "float": "left",
                        "padding": "3px",
                        "width": "33%"
                    },
                    children=[
                        dcc.Graph(
                            id='histogram1'
                        ),
                    ]
                ),
                html.Div(
                    className="four columns",
                    style={
                        "display": "inline-block",
                        "margin": "0 auto",
                        "padding": "3px",
                        "width": "33%",
                        "height": "30%",
                    },
                    children=[
                        dcc.Graph(id="histogram2")
                    ]
                ),
                html.Div(
                    className="four columns",
                    style={
                        "width": "33%",
                        "text-align": "center",
                        "display": "inline-block",
                        "margin": "0 auto",
                        "padding": "3px",
                    },
                    children=[
                        dcc.Graph(id="histogram3")
                    ]
                )
            ]
        )
    ]
)


# Update total cases in kenya
@app.callback(
    Output("cases-element", "children"),
    [Input("county-dropdown", "value")]
)
def update_kenya_confirmed(_):
    k_confirmed = confirmed_global.loc[c_index, str(date)]
    return f"{k_confirmed}"


# Update total deaths in kenya
@app.callback(
    Output("deaths-element", "children"),
    [Input("county-dropdown", "value")]
)
def update_kenya_deaths(_):
    k_deaths = deaths_global.loc[d_index, str(date)]
    return f"{k_deaths}"


# Update total recoveries in Kenya
@app.callback(
    Output("recovered-element", "children"),
    [Input("county-dropdown", "value")]
)
def update_recoveries_kenya(_):
    k_recoveries = recovered_global.loc[r_index, str(date)]
    return f"{k_recoveries}"


@app.callback(
    Output("c-hrs-element", "children"),
    [Input("county-dropdown", "value")]
)
def show_24_hours(_):
    today = get_today(confirmed_global)
    yesterday = get_prev_date(confirmed_global)
    c_index, _, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = confirmed_global.loc[c_index, today] - confirmed_global.loc[c_index, yesterday]
    return f"+{difference} in past 24hrs"


@app.callback(
    Output("d-hrs-element", "children"),
    [Input("county-dropdown", "value")]
)
def show_24_hours(_):
    today = get_today(deaths_global)
    yesterday = get_prev_date(deaths_global)
    _, d_index, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = deaths_global.loc[d_index, today] - deaths_global.loc[d_index, yesterday]
    return f"+{difference} in past 24hrs"


@app.callback(
    Output("r-hrs-element", "children"),
    [Input("county-dropdown", "value")]
)
def show_24_hours(_):
    today = get_today(recovered_global)
    yesterday = get_prev_date(recovered_global)
    _, _, r_index = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = recovered_global.loc[d_index, today] - recovered_global.loc[d_index, yesterday]
    return f"+{difference} in past 24hrs"


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


# Update the line graph
@app.callback(
    Output("histogram1", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("sub-county-dropdown", "value"),
    ]
)
def update_histogram(country, sub_county):
    if country is None:
        text = "GRAPH OF ACTIVE CASES<br>Comaparison of Kenya and US"
        country = 'US'
    elif country is not None and sub_county is None:
        text = f"GRAPH OF ACTIVE CASES<br>Comparison of Kenaya and {country}"
    else:
        text = f"Comparison of Kenya and {country}, {sub_county}"

    title = "GRAPH FOR ACTIVE CASES"
    labels = [f"{country}", "Kenya"]
    colors = ['rgb(49,130,189)', 'red']
    mode_size = [8, 12]
    line_size = [2, 4]

    # Chosen country
    row, col = get_first_date(country)
    x_axis, y = get_axes(row, col, confirmed_global)
    y_axis,mean, std_div = normalize_axis(y)

    # Kenya
    row, col = get_first_date("Kenya")
    ke_x_axis, y = get_axes(row, col, confirmed_global)
    ke_y_axis, ke_mean, ke_std_div = normalize_axis(y)

    mean_data = [mean, ke_mean]
    std_data = [std_div, ke_std_div]

    x_data = [x_axis, ke_x_axis]
    y_data = [y_axis, ke_y_axis]

    fig = go.Figure()

    for i in range(len(y_data)):
        fig.add_trace(go.Scatter(
            x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))
        # endpoints
        fig.add_trace(
            go.Scatter(
                x=[x_data[i][0], x_data[i][-1]],
                y=[y_data[i][0], y_data[-1]],
                mode='markers',
                marker=dict(color=colors[i], size=mode_size[i])
            )
        )
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=False,
            margin=dict(
                autoexpand=False,
                l=20,
                r=20,
                pad=4,
                t=20,
            ),
            showlegend=True,
            plot_bgcolor="#323130",
            paper_bgcolor="#323130",
            height=400,
        )

        for y_trace, label, color, m, std in zip(y_data, labels, colors, mean_data, std_data):
            annotations = [

                # Title of the graph
                dict(
                    xref='paper',

                    yref='paper',
                    x=0.0,
                    y=1.05,
                    xanchor='left',
                    yanchor='top',
                    text=text,
                    font=dict(
                        family='Open Sans',
                        size=12,
                        color='#d8d8d8'
                    ),
                    showarrow=False
                ),
                # Labeling the right side of the plot
                dict(
                    xref='paper',
                    x=0.95,
                    y=y_trace[-1],
                    xanchor='left',
                    yanchor='middle',
                    text='{} cases'.format(y_trace[-1]),
                    font=dict(
                        family='Arial',
                        size=16,
                        color='rgb(150, 150, 150)',

                    ),
                    showarrow=False
                )
            ]
    fig.update_layout(annotations=annotations)

    return fig


@app.callback(
    Output("histogram2", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("sub-county-dropdown", "value"),
    ]
)
def update_graph_for_recoveries(country, sub):
    if country is None:
        text = "GRAPH OF RECOVERIES<br>Comaparison of Kenya and US"
        country = 'US'
    elif country is not None and sub is None:
        text = f"GRAPH OF RECOVERIES<br>Comparison of Kenaya and {country}"
    else:
        text = f"Comparison of Kenya and {country}, {sub}"

    title = "GRAPH FOR RECOVERIES CASES"
    labels = [f"{country}", "Kenya"]
    colors = ['rgb(49,130,189)', 'red']
    mode_size = [8, 12]
    line_size = [2, 4]

    # Chosen country
    row, col = get_first_date(country)
    x_axis, y = get_axes(row, col, recovered_global)
    y_axis,mean, std_div = normalize_axis(y)

    # Kenya
    row, col = get_first_date("Kenya")
    ke_x_axis, y = get_axes(row, col, recovered_global)
    ke_y_axis, ke_mean, ke_std_div = normalize_axis(y)

    mean_data = [mean, ke_mean]
    std_data = [std_div, ke_std_div]

    x_data = [x_axis, ke_x_axis]
    y_data = [y_axis, ke_y_axis]

    fig = go.Figure()

    for i in range(len(y_data)):
        fig.add_trace(go.Scatter(
            x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))
        # endpoints
        fig.add_trace(
            go.Scatter(
                x=[x_data[i][0], x_data[i][-1]],
                y=[y_data[i][0], y_data[-1]],
                mode='markers',
                marker=dict(color=colors[i], size=mode_size[i])
            )
        )
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=False,
            margin=dict(
                autoexpand=False,
                l=20,
                r=20,
                pad=4,
                t=20,
            ),
            showlegend=True,
            plot_bgcolor="#323130",
            paper_bgcolor="#323130",
            height=400,
        )

        for y_trace, label, color, m, std in zip(y_data, labels, colors, mean_data, std_data):
            annotations = [

                # Title of the graph
                dict(
                    xref='paper',

                    yref='paper',
                    x=0.0,
                    y=1.05,
                    xanchor='left',
                    yanchor='top',
                    text=text,
                    font=dict(
                        family='Open Sans',
                        size=12,
                        color='#d8d8d8'
                    ),
                    showarrow=False
                ),
                # Labeling the right side of the plot
                dict(
                    xref='paper',
                    x=0.95,
                    y=y_trace[-1],
                    xanchor='left',
                    yanchor='middle',
                    text='{} cases'.format(y_trace[-1]),
                    font=dict(
                        family='Arial',
                        size=16,
                        color='rgb(150, 150, 150)',

                    ),
                    showarrow=False
                )
            ]
    fig.update_layout(annotations=annotations)

    return fig


@app.callback(
    Output("histogram3", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("sub-county-dropdown", "value"),
    ]
)
def update_graph_for_deaths(country, sub):
    if country is None:
        text = "GRAPH FOR DEATHS<br>Comaparison of Kenya and US"
        country = 'US'
    elif country is not None and sub is None:
        text = f"Comparison of Kenaya and {country}"
    else:
        text = f"Comparison of Kenya and {country}, {sub}"

    title = "GRAPH FOR RECOVERIES CASES"
    labels = [f"{country}", "Kenya"]
    colors = ['rgb(49,130,189)', 'red']
    mode_size = [8, 12]
    line_size = [2, 4]

    # Chosen country
    row, col = get_first_date(country)
    x_axis, y = get_axes(row, col, deaths_global)
    y_axis,mean, std_div = normalize_axis(y)

    # Kenya
    row, col = get_first_date("Kenya")
    ke_x_axis, y = get_axes(row, col, deaths_global)
    ke_y_axis, ke_mean, ke_std_div = normalize_axis(y)

    mean_data = [mean, ke_mean]
    std_data = [std_div, ke_std_div]

    x_data = [x_axis, ke_x_axis]
    y_data = [y_axis, ke_y_axis]

    fig = go.Figure()

    for i in range(len(y_data)):
        fig.add_trace(go.Scatter(
            x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))
        # endpoints
        fig.add_trace(
            go.Scatter(
                x=[x_data[i][0], x_data[i][-1]],
                y=[y_data[i][0], y_data[-1]],
                mode='markers',
                marker=dict(color=colors[i], size=mode_size[i])
            )
        )
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=False,
            margin=dict(
                autoexpand=False,
                l=20,
                r=20,
                pad=4,
                t=20,
            ),
            showlegend=True,
            plot_bgcolor="#323130",
            paper_bgcolor="#323130",
            height=400,
        )

        for y_trace, label, color, m, std in zip(y_data, labels, colors, mean_data, std_data):
            annotations = [

                # Title of the graph
                dict(
                    xref='paper',

                    yref='paper',
                    x=0.0,
                    y=1.05,
                    xanchor='left',
                    yanchor='top',
                    text=text,
                    font=dict(
                        family='Open Sans',
                        size=12,
                        color='#d8d8d8'
                    ),
                    showarrow=False
                ),
                # Labeling the right side of the plot
                dict(
                    xref='paper',
                    x=0.95,
                    y=y_trace[-1],
                    xanchor='left',
                    yanchor='middle',
                    text='{} cases'.format(y_trace[-1]),
                    font=dict(
                        family='Arial',
                        size=16,
                        color='rgb(150, 150, 150)',

                    ),
                    showarrow=False
                )
            ]
    fig.update_layout(annotations=annotations)

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)

