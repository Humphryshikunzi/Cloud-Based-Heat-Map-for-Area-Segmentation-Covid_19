# import important libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *


# Load global data sets
confirmed_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv")
deaths_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv")
recovered_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv")

# Load global data set for development testing
# confirmed_global = pd.read_csv("assets/time_series_covid19_confirmed_global.csv")
# deaths_global = pd.read_csv("assets/time_series_covid19_deaths_global.csv")
# recovered_global = pd.read_csv("assets/time_series_covid19_recovered_global.csv")

# Load kenyan data set
# confirmed_kenya = pd.read_csv("")
# deaths_kenya = pd.read_csv("")
# recovered_kenya = pd.read_csv("")

# Load kenyan data set for development testing
confirmed = pd.read_csv("assets/testdata.csv")
confirmed = confirmed.fillna(0)


# House keeping functions
def get_kenya_first_case(dict_data):
    # Takes input a dictionary of dates and the cases on that date
    # Returns the date of the first case in kenya
    for x in dict_data:
        if dict_data[x] != 0:
            return x


def get_num_to_dates(selected):
    # Inputs a selected county
    # Returns a dict of dates and num of cases of county
    y_axis = {}
    dates = [i for i in confirmed.iloc[:]][4:]
    for date in dates:
        y = 0
        for index, cout in enumerate(confirmed["County"]):
            if cout == selected:
                y += confirmed.loc[index, str(date)]
        y_axis[date] = y
    return y_axis


def get_sub_num(selected):
    # Inputs a selected sub-county
    # Returns a dict of dates and num of cases of sub-county
    data = {}
    dates = [i for i in confirmed.iloc[:]][4:]
    for date in dates:
        for index, sub in enumerate(confirmed["Constituency"]):
            if sub == selected:
                data[date] = confirmed.loc[index, date]
    return data


def counties_with_constituencies():
    # Returns a dict with counties -> subcounties -> Lat, Long
    # {county
    #       {
    #       sub-county
    #               {
    #               "Lat": ""
    #               "Long": ""
    #               }
    #       }
    # }
    counties_constituencies = {}
    for county in confirmed["County"]:
        for index, const in enumerate(confirmed["Constituency"]):
            if county not in counties_constituencies:
                counties_constituencies[county] = {}
            if const not in counties_constituencies[county] and confirmed.loc[index, "County"] == county:
                counties_constituencies[county][const] = {
                    "Lat": confirmed.loc[index, "Lat"],
                    "Long": confirmed.loc[index, "Long"]
                }

    return counties_constituencies


def update_list_constituencies(county):
    # Inputs a county
    # Returns a list of all sub-counties in a county
    all_const = counties_with_constituencies()
    constituencies = [const for const in all_const[county]]
    return constituencies


def get_kenya_index_from_global(confirmed, deaths, recoveries):
    # Takes pd data frames confirmed, deaths, recoveries
    # Returns index of kenya from all the pd data frames
    for index, country in enumerate(confirmed["Country/Region"]):
        if country == "Kenya":
            c_index = index
    for index, country in enumerate(deaths["Country/Region"]):
        if country == "Kenya":
            d_index = index
    for index, country in enumerate(recoveries["Country/Region"]):
        if country == "Kenya":
            r_index = index
    return c_index, d_index, r_index


def update_axes(county, sub_county):
    # Inputs a selected county and sub-county
    # Return lists of x-axis(dates), y-axis(values) for graph
    if county is not None and sub_county is None:
        # if county alone is chosen
        dict_of_days_nums = get_num_to_dates(county)
        x_axis = [y for y in dict_of_days_nums]
        y_axis = []
        for axis in x_axis:
            y_axis.append(dict_of_days_nums[axis])
    elif county and sub_county:
        # if both county and sub-county are chosen
        axes = get_sub_num(sub_county)
        x_axis = [x for x in axes]
        y_axis = []
        for i in x_axis:
            y_axis.append(axes[i])
    elif not county and not sub_county:
        # if neither county nor sub-county is chosen
        c_index, _, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
        list_of_dates = [date for date in confirmed_global.iloc[:]][4:]
        first_date = get_kenya_first_case(get_num_to_dates("Australia")) # Change later to kenya
        y_axis = [i for i in confirmed_global.iloc[c_index, list_of_dates.index(first_date):]]
        x_axis = [x for x in list_of_dates[list_of_dates.index(first_date):]]
    return x_axis, y_axis


def county_and_cases():
    # Returns a dict of counties and the number of cases in the county
    county_cases = {}
    all_counties = counties_with_constituencies()
    for county in all_counties:
        _, num = update_axes(county, None)
        county_cases[county] = sum(num)
    return county_cases


def country_and_cases():
    # Returns a dict of coutries and the number of cases in the country
    country_cases = {}
    date = get_today(confirmed_global)
    for index, country in enumerate(confirmed_global["Country/Region"]):
        if country not in country_cases and pd.isnull(confirmed_global.loc[index, "Province/State"]):
            country_cases[country] = confirmed_global.loc[index, date]
        elif country not in country_cases and not pd.isnull(confirmed_global.loc[index, "Province/State"]):
            country_cases[country + ", " + (confirmed_global.loc[index, "Province/State"])] = confirmed_global.loc[index, date]
    return country_cases


def get_global_results():
    # Returns number of cases confirmed, recovered, died
    init_c = init_d = init_r = 0
    today_c, today_d, today_r = list(confirmed_global.head(0))[-1], list(deaths_global.head(0))[-1], list(recovered_global.head(0))[-1]
    results_c, results_d, results_r = confirmed_global[today_c], deaths_global[today_d], recovered_global[today_r]

    for con in results_c:
        init_c += con
        if con is None:
            continue
    for death in results_d:
        init_d += death
        if death is None:
            continue
    for recov in results_r:
        init_r += recov
        if recov is None:
            continue

    return init_c, init_d, init_r


def get_today(csv_file):
    # Takes in a pd data frame
    # Returns the current date
    latest_date = list(csv_file.head(0))[-1]
    return latest_date


def data_without_zeros(x, y):
    # Inputs a list of x and y axis
    # Returns x and y axis from when the first case was reported
    for index, axis in enumerate(y):
        if axis != 0:
            break
    return x[index:], y[index:]


# Important variables set-up
c_index, d_index, r_index = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
counties_constituencies_coords = counties_with_constituencies()
date = get_today(confirmed_global)
cases_in_each_county = county_and_cases()
list_cases_in_each_county = []
for case in cases_in_each_county.items():
    list_cases_in_each_county.append([case[0], case[1]])
sorted_list = sorted(list_cases_in_each_county, key=lambda x: x[1], reverse=True)

# Some final house keeping set-ups :)
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewpoint", "content": "width=device-width"}
    ],
)
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
            className='row',
            children=[
                # Column for user control
                html.Div(
                    className="four columns div-user-controls",
                    style={"width": "24%"},
                    children=[
                        html.H2("COVID-19 DATA ANALYSIS"),
                        html.P(id="cases-kenya"),
                        html.P(id="deaths-kenya"),
                        html.P(id="recoveries-kenya"),


                        # Change to side by side for mobile layout
                        html.Div(
                            className="row",
                            children=[
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
                                html.H2("COUNTY SUMMARY"),
                                html.P(id='county-summary'),
                                # html.P(f"{sorted_list[0][0]}: {sorted_list[0][1]}"),
                                # html.P(f"{sorted_list[1][0]}: {sorted_list[1][1]}"),
                                # html.P(f"{sorted_list[2][0]}: {sorted_list[2][1]}"),
                                # html.P(f"{sorted_list[3][0]}: {sorted_list[3][1]}"),
                                # html.P(
                                #     {f"{list_cases_in_each_county[i][0]}: {list_cases_in_each_county[i][1]}"}
                                #     for i in range(len(list_cases_in_each_county))
                                # ),
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
                        "margin-right": "1%"
                    },
                    children=[
                        html.H2("GLOBAL COVID-19 RESULTS"),
                        html.P(id='total-cases'),
                        html.P(id="total-deaths"),
                        html.P(id="total-recovered"),
                    ]
                ),

                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    style={
                        "float": "left",
                        "display": "flex",
                        "flex-direction": "right",
                        "height": "100vh",
                        "width": "45%",
                        "background-color": "#31302F",
                    },
                    children=[
                        dcc.Graph(id='map-graph'),
                        html.Div(
                            className="text-padding",
                            style={
                                "padding": "5px",
                                "margin-top": "1%",
                            },
                        ),
                        dcc.Graph(
                            id="histogram"),
                    ],
                ),
            ],
        ),
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
                html.H2("OTHER SUMMARY DOCUMENT WOULD GO HERE"),
                html.Div(
                    className="four columns",
                    style={
                        "float": "left",
                        "text-align": "left",
                        "width": "40%"
                    },
                    children=[
                        html.H2("JUST SOME TESTING BEFORE PRODUCTION HEADING"),
                        html.P("ojiwjeifjap9ejf;awejif"),
                        html.P("aoijepoaejoaiejf oaijefoiejaoji eoaeji in the beginning God created the heavens"
                               "and the earth,  and now it you and me are to fill it"),
                        html.P("aoijeoaejifojeifojiefijoaejioeijfaiej"),
                    ]
                ),
                html.Div(
                    className="four columns",
                    style={
                        "float": "right",
                        "width": "40%",
                        "text-align": "left"
                    },
                    children=[
                        html.H2("JUST SOME TESTING BEFORE PRODUCTION HEADING"),
                        html.P(";aoeif;aoejifoajeifoejfoajepoiej"),
                        html.P("aoeijfoajieoaijeofjiaoeijfapoejifoejioeji"),
                        html.P("aoejifoiaejfoaiejfiej"),
                    ]
                )
            ]
        )
    ]
)


# Update total cases in kenya
@app.callback(
    Output("cases-kenya", "children"),
    [Input("county-dropdown", "value")]
)
def update_kenya_confirmed(_):
    k_confirmed = confirmed_global.loc[c_index, str(date)]
    return f"Total confirmed cases in Kenya: {k_confirmed}"


# Update total deaths in kenya
@app.callback(
    Output("deaths-kenya", "children"),
    [Input("county-dropdown", "value")]
)
def update_kenya_deaths(_):
    k_deaths = deaths_global.loc[d_index, str(date)]
    return f"Total deaths in Kenya: {k_deaths}"


# Update total recoveries in Kenya
@app.callback(
    Output("recoveries-kenya", "children"),
    [Input("county-dropdown", "value")]
)
def update_recoveries_kenya(_):
    k_recoveries = recovered_global.loc[r_index, str(date)]
    return f"Total recoveries in Kenya: {k_recoveries}"


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


@app.callback(
    Output("county-summary", "children"),
    [Input("county-dropdown", "value")]
)
def show_kenya_summary(_):
    output = []
    for i in range(len(sorted_list)):
        output += ('{0}: {1} cases'.format(sorted_list[i][0], sorted_list[i][1])), html.Br(), ''
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

    countries = country_and_cases()



    zoom = 2.0
    lat_initial = -1.2921
    long_initial = 36.8219
    bearing = 0

    # Also add for only county selection
    if county and subcounty:
        zoom = 5.0
        lat_initial = counties_constituencies_coords[county][subcounty]["Lat"]
        long_initial = counties_constituencies_coords[county][subcounty]["Long"]
    print(lat_initial)
    print(long_initial)

    return go.Figure(
        data=[
            # Data for all regions
            go.Scattermapbox(
                lat=confirmed_global["Lat"],
                lon=confirmed_global["Long"],
                mode="markers",
                hoverinfo="lat+lon",
                text=" ",
                marker=go.scattermapbox.Marker(
                    showscale=False,
                    color='red',
                    opacity=0.5,
                    size=7,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
                    ],
                    # colorbar=dict(
                    #     title="Number <br> cases",
                    #     x=0.93,
                    #     xpad=0,
                    #     nticks=10,
                    #     tickfont=dict(color="#d8d8d8"),
                    #     titlefont=dict(color="#d8d8d8"),
                    #     thicknessmode="pixels",
                    # ),
                ),
            ),
            # Have here plot of kenya on the map

        ],
        layout=go.Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=lat_initial, lon=long_initial),
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            # updatemenus=[
            #     dict(
            #         buttons=(
            #             [
            #                 dict(
            #                     args=[
            #                         {
            #                             "mapbox.zoom": 3.0,
            #                             "mapbox.center.lon": -1.2921,
            #                             "mapbox.center.lat": 36.8219,
            #                             "mapbox.bearing": 0,
            #                             "mapbox.style": "dark",
            #                         }
            #                     ],
            #                     label="Reset Zoom",
            #                     method="relayout",
            #                 )
            #             ]
            #         ),
            #         direction="right",
            #         pad={"r": 0, "t": 0, "b": 0, "l": 0},
            #         showactive=False,
            #         type="buttons",
            #         x=0.45,
            #         y=0.02,
            #         xanchor="right",
            #         yanchor="bottom",
            #         bgcolor="#323130",
            #         borderwidth=1,
            #         bordercolor="#6d6d6d",
            #         font=dict(color="#FFFFFF"),
            #     )
            # ],
        ),
    )


# Update the line graph
@app.callback(
    Output("histogram", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("sub-county-dropdown", "value"),
    ]
)
def update_histogram(county, sub_county):
    x_axis, y_axis = update_axes(county, sub_county)
    x_axis, y_axis = data_without_zeros(x_axis, y_axis)
    if county is None:
        text = "Graph of COVID-19 cases in Kenya"
    elif county is not None and sub_county is None:
        text = f"Graph of COVID-19 cases in {county}"
    else:
        text = f"Graph of COVID-19 cases in {county}, {sub_county}"
    # labels = ['Confirmed', 'Deaths', "Recoveries"]
    # colors = ['rgb(67,67, 67', 'rgb(115,115,115)', 'rgb(49,130,189)']
    #
    # mode_size = [12, 8, 8]
    # line_size = [4, 2, 2]
    labels = ['Confirmed']
    colors = ['white']

    mode_size = [12]
    line_size = [4]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_axis, y=y_axis, mode='lines',
        name=labels[0],
        line=dict(color=colors[0], width=line_size[0]),
        connectgaps=True,
    ))
    # endpoints
    fig.add_trace(
        go.Scatter(
            x=[x_axis[0], x_axis[-1]],
            y=[y_axis[0], y_axis[-1]],
            mode='markers',
            marker=dict(color=colors[0], size=mode_size[0])
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
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor="#323130",
        paper_bgcolor="#323130"
    )
    annotations = [
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
        dict(
            xref='paper',
            x=0.95,
            y=y_axis[-1],
            xanchor='left',
            yanchor='middle',
            text='{} cases'.format(y_axis[-1]),
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
    app.run_server(debug=True)
