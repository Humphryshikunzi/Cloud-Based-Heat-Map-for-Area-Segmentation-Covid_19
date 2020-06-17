import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
from collections import OrderedDict
from plotly import graph_objs as go
import flask
import numpy as np
import pandas as pd
from random import randint
import os
import dash_bootstrap_components as dbc


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewpoint", "content": "width=device-width"}
    ],
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


app.head = [
    html.Link(
        href='assets/favicon.ico',
        rel='icon',
    )
]
app.title = 'COVID-19 KENYA DASHBOARD'


confirmed_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
deaths_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
recovered_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
with_text = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
with_text_d = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
with_text_r = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
# confirmed_global = pd.read_csv("time_series_covid19_confirmed_global.csv")
# deaths_global = pd.read_csv("time_series_covid19_deaths_global.csv")
# recovered_global = pd.read_csv("time_series_covid19_recovered_global.csv")
# with_text = pd.read_csv("time_series_covid19_confirmed_global.csv")
# with_text_d = pd.read_csv('time_series_covid19_deaths_global.csv')
# with_text_r = pd.read_csv('time_series_covid19_recovered_global.csv')

confirmed = pd.read_csv("testdata.csv")
confirmed = confirmed.fillna(0)
kenya_data = pd.read_csv("https://raw.githubusercontent.com/collins-emasi/kenya-data/master/complete_set.csv")
ke_with_text = pd.read_csv('https://raw.githubusercontent.com/collins-emasi/kenya-data/master/complete_set.csv')
# kenya_data = pd.read_csv('D:/kenya-data/complete_set.csv')
# ke_with_text = pd.read_csv('D:/kenya-data/complete_set.csv')


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


def ke_axes_confirmed():
    y_axis = []
    for y in confirmed_global.loc[c_index, '3/13/20':]:
        y_axis.append(y)
    x_axis = list(range(len(y_axis)))
    return x_axis, y_axis


def ke_axes_deaths():
    y_axis = []
    for y in deaths_global.loc[d_index, '3/13/20':]:
        y_axis.append(y)
    x_axis = list(range(len(y_axis)))
    return x_axis, y_axis


def ke_axes_recoveries():
    y_axis = []
    for y in deaths_global.loc[r_index, '3/13/20':]:
        y_axis.append(y)
    x_axis = list(range(len(y_axis)))
    return x_axis, y_axis


def Get_Country_Index():
    country_indexes = {'Brazil': 28, 'India': 131, 'Italy': 137, 'Kenya': 142, 'South Africa': 200}
    return country_indexes


def Get_Country_Population():
    countries_population = {'Brazil': 217301365, 'India': 1350716488, 'Italy': 60472125, 'Kenya': 53629525,
                            'South Africa': 59220561}
    return countries_population


def Get_Country_Cases(country_population, index_of_country=142):
    # get the total cases for a Country from the dowloaded data, using index for the Country, with default Kenya(142)
    get_covid = confirmed_global.iloc[[index_of_country]]

    # convert to 2D array
    get_covid_to_2D_array = np.array(get_covid)

    # convert to 1D array
    get_covid_to_1_array = get_covid_to_2D_array[0]

    # get rid of lon, lat, Country, State and index
    get_covid_to_1_array_cleaned = np.array(get_covid_to_1_array[4:])

    # get the day the fisrt case was reported
    get_first_day = np.argmax(get_covid_to_1_array_cleaned > 0)

    # reduce the array to include elements only for days when the day first case was reported
    get_covid_cases = get_covid_to_1_array_cleaned[get_first_day:]

    # Normalise the final data
    get_covid_cases_normalised = (get_covid_cases / country_population) * 100000

    # return a dictionary of cases for good visualization and normalised for plotting
    final_cases = {'cases': get_covid_cases, 'cases_normalised': get_covid_cases_normalised}
    return final_cases


kenya_cases = Get_Country_Cases(Get_Country_Population()['Kenya'], Get_Country_Index()['Kenya'])
italy_cases = Get_Country_Cases(Get_Country_Population()['Italy'], Get_Country_Index()['Italy'])
brazil_cases = Get_Country_Cases(Get_Country_Population()['Brazil'], Get_Country_Index()['Brazil'])
south_africa_cases = Get_Country_Cases(Get_Country_Population()['South Africa'], Get_Country_Index()['South Africa'])
india_cases = Get_Country_Cases(Get_Country_Population()['India'], Get_Country_Index()['India'])


# get the number of days when each country reported cases, starting from day one
kenya_days = len(kenya_cases['cases'])
italy_days = len(italy_cases['cases'])
india_days = len(india_cases['cases'])
brazil_days = len(brazil_cases['cases'])
south_africa_days = len(south_africa_cases['cases'])

coutries_and_days = [kenya_days, italy_days, india_days, brazil_days, south_africa_days]
coutry_with_highest_days = max(coutries_and_days)

# get  the values for x axis for each country
italy_x_axis = np.arange(1, italy_days + 1)
kenya_x_axis = np.arange(1, kenya_days + 1)
india_x_axis = np.arange(1, india_days + 1)
brazil_x_axis = np.arange(1, brazil_days + 1)
south_africa_x_axis = np.arange(1, south_africa_days + 1)


# update number of hours
def show_24_hours_c():
    today = get_today(confirmed_global)
    yesterday = get_prev_date(confirmed_global)
    c_index, _, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = confirmed_global.loc[c_index, today] - confirmed_global.loc[c_index, yesterday]
    return f"+{difference} as of yesterday"


def show_24_hours_d():
    today = get_today(deaths_global)
    yesterday = get_prev_date(deaths_global)
    _, d_index, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = deaths_global.loc[d_index, today] - deaths_global.loc[d_index, yesterday]
    return f"+{difference} as of yesteday"


def show_24_hours_r():
    today = get_today(recovered_global)
    yesterday = get_prev_date(recovered_global)
    _, _, r_index = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = recovered_global.loc[d_index, today] - recovered_global.loc[d_index, yesterday]
    return f"+{difference} as of yesterday"


def update_kenya_confirmed():
    k_confirmed = confirmed_global.loc[c_index, str(date)]
    return f"{k_confirmed}"


def update_kenya_deaths():
    k_deaths = deaths_global.loc[d_index, str(date)]
    return f"{k_deaths}"


def update_recoveries_kenya():
    k_recoveries = recovered_global.loc[r_index, str(date)]
    return f"{k_recoveries}"


def header_for_the_page():
    division = html.Div(
        children=[
            html.Div(
                className="col-xs-1 text-center p-4 font-weight-bolder",
                style={
                    'margin-top': '0.75rem',
                },
                children=[
                    html.P(
                        "CORONA VIRUS DISEASE KENYA DASHBOARD: HEAT MAP AND DATA ANALYSIS TOOL",
                        style={
                            'font-size': '195%',
                            'font-weight': 'bolder',
                            'letter-spacing': '2.2px',
                        },
                    ),
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
                        className='row rounded-lg',
                        style={
                            "background": "black",
                            "margin-left": "2%",
                            "margin-right": "2%",
                            "text-align": "center",
                            "width": "90%",
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
                                    html.P(show_24_hours_c(), className='hrs-24', id='c-hrs-element'),
                                    html.H1(update_kenya_confirmed(), className='cases-num', id='cases-element'),
                                    html.P("POSITIVE CASES", className='cases-text'),
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
                                    html.P(show_24_hours_r(), className='hrs-24', id="r-hrs-element"),
                                    html.H1(update_recoveries_kenya(), className='recovered-num', id='recovered-element'),
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
                                    html.P(show_24_hours_d(), className='hrs-24', id='d-hrs-element'),
                                    html.H1(update_kenya_deaths(), className='deaths-num', id='deaths-element'),
                                    html.P("DEATHS", className='deaths-text'),
                                ]
                            ),
                        ]
                    ),

                ]

            ),
        ]
    )

    return division


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
            country_cases[country] = (
                confirmed_global.loc[index, date],
                deaths_global.loc[index, date]
            )
        elif country not in country_cases and not pd.isnull(confirmed_global.loc[index, "Province/State"]):
            country_cases[country + ", " + (confirmed_global.loc[index, "Province/State"])] = (
                confirmed_global.loc[index, date],
                deaths_global.loc[index, date]
            )
    return country_cases


def get_global_results():
    # Returns number of cases confirmed, recovered, died
    init_c = init_d = init_r = 0
    today_c, today_d, today_r = list(confirmed_global.head(0))[-1], list(deaths_global.head(0))[-1], list(recovered_global.head(0))[-1]
    results_c, results_d, results_r = confirmed_global[today_c], deaths_global[today_d], recovered_global[today_r]
    for con in results_c:
        if con is None:
            continue
        init_c += con
    for death in results_d:
        if death is None:
            continue
        init_d += death
    for recov in results_r:
        if recov is None:
            continue
        init_r += recov

    return init_c, init_d, init_r


def get_today(csv_file):
    # Takes in a pd data frame
    # Returns the current date
    latest_date = list(csv_file.head(0))[-1]
    return latest_date


def get_prev_date(csv_file):
    # Takes in a pd dataframe
    # Returns a previous date from today
    prev_date = list(csv_file.head(0))[-2]
    return prev_date


def data_without_zeros(x, y):
    # Inputs a list of x and y axis
    # Returns x and y axis from when the first case was reported
    for index, axis in enumerate(y):
        if axis != 0:
            break
    return x[index:], y[index:]


def get_first_date(country_region):
    # Input a selected country
    # Returns the row index and the column index of first case
    for index, series in confirmed_global.iterrows():
        if not pd.isnull(series['Province/State']) and series['Country/Region'] == country_region:
            series['Country/Region'] = series['Country/Region'] + ", " + series['Province/State']
            country_region = country_region + ", " + series['Province/State']
        if series['Country/Region'] == country_region:
            for col_index, date in enumerate(series[4:]):
                if date != 0:
                    return index, col_index + 4


def normalize_axis(axis):
    # takes in a list of values
    # Returns mean normalize values
    axis = np.array(axis)
    axis_norm = (axis - axis.mean())/(axis.std())
    return axis_norm.tolist(), axis.mean(), axis.std()


def get_axes(row, col, data):
    y_axis = []
    for y in data.iloc[row, col:]:
        y_axis.append(y)
    x_axis = list(range(len(y_axis)))
    return x_axis, y_axis


def get_counties_and_cases():
    today = get_today(kenya_data)
    county_cases = {}
    for index, county in enumerate(kenya_data["County"]):
        county_cases[county] = kenya_data.loc[index, today]
    return county_cases


c_index, d_index, r_index = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
counties_constituencies_coords = counties_with_constituencies()
date = get_today(confirmed_global)
cases_in_each_county = county_and_cases()
ke_date = get_today(kenya_data)
list_cases_in_each_county = []
for case in cases_in_each_county.items():
    list_cases_in_each_county.append([case[0], case[1]])
sorted_list = sorted(list_cases_in_each_county, key=lambda x: x[1], reverse=True)
with_text['Text'] = with_text['Country/Region'] + '<br>Cases: ' + (with_text[date]).astype(str)
with_text_d['Text'] = '<br>Deaths: ' + (with_text_d[date]).astype(str)
with_text_r['Text'] = '<br>Recoveries: ' + (with_text_r[date]).astype(str)


def card_template(i_d, header='Card header', title='Card Title', footer='Stay Home, Stay Safe'):
    return \
        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.H5(title, className='card-title'),
                    dcc.Graph(figure=graph_fig(i_d), id=i_d),
                ]
            ),
            dbc.CardFooter(footer),
        ]


def graph_fig(i_d):
    if i_d == 'graph0':
        y_data = [
            kenya_cases['cases'],
            italy_cases['cases'],
            india_cases['cases'],
            brazil_cases['cases'],
            south_africa_cases['cases'],
        ]
        x_data = [
            kenya_x_axis, italy_x_axis, india_x_axis, brazil_x_axis, south_africa_x_axis
        ]
        names = [
            'Kenya_covid_19_cases',
            "Italy_covid_19_cases",
            "India_covid_19_cases",
            "Brazil_covid_19_cases",
            "South_Africa_Covid_19_cases",
        ]
    elif i_d == 'graph1':
        y_data = [
            kenya_cases['cases_normalised'],
            italy_cases['cases_normalised'],
        ]
        x_data = [
            kenya_x_axis,
            italy_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "Italy_covid_19_cases",
        ]
    elif i_d == 'graph2':
        y_data = [
            kenya_cases['cases_normalised'],
            india_cases['cases_normalised'],
        ]
        x_data = [
            kenya_x_axis,
            india_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "India_covid_19_cases",
        ]
    elif i_d == 'graph3':
        y_data = [
            kenya_cases['cases_normalised'],
            brazil_cases['cases_normalised'],
        ]
        x_data = [
            kenya_x_axis,
            brazil_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "Brazil_covid_19_cases",
        ]
    elif i_d == 'graph4':
        y_data = [
            kenya_cases['cases_normalised'],
            south_africa_cases['cases_normalised'],
        ]
        x_data = [
            kenya_x_axis,
            south_africa_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "South_Africa_covid_19_cases",
        ]
    elif i_d == 'graph5':
        y_data = [
            kenya_cases['cases'],
            italy_cases['cases'],
            india_cases['cases'],
            brazil_cases['cases'],
            south_africa_cases['cases'],
        ]
        x_data = [
            kenya_x_axis,
            italy_x_axis,
            india_x_axis,
            brazil_x_axis,
            south_africa_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "Italy_covid_19_cases",
            "India_covid_19_cases",
            "Brazil_covid_19_cases",
            "South_Africa_Covid_19_cases",
        ]
    elif i_d == 'graph6':
        y_data = [
            kenya_cases['cases'],
            italy_cases['cases'],
        ]
        x_data = [
            kenya_x_axis,
            italy_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "Italy_covid_19_cases",
        ]
    elif i_d == 'graph7':
        y_data = [
            kenya_cases['cases'],
            india_cases['cases'],
        ]
        x_data = [
            kenya_x_axis,
            india_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "India_covid_19_cases",
        ]
    elif i_d == 'graph8':
        y_data = [
            kenya_cases['cases'],
            brazil_cases['cases'],
        ]
        x_data = [
            kenya_x_axis,
            brazil_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "Brazil_covid_19_cases",
        ]
    elif i_d == 'graph9':
        y_data = [
            kenya_cases['cases'],
            south_africa_cases['cases'],
        ]
        x_data = [
            kenya_x_axis,
            south_africa_x_axis,
        ]
        names = [
            "Kenya_covid_19_cases",
            "South_Africa_covid_19_cases",
        ]
    # fig = {
    #     'data': [
    #         {'x': x_data[i], 'y': y_data[i], 'type': 'line', 'name': names[i]}
    #         for i in range(len(y_data))
    #     ]
    # }
    fig = go.Figure()
    for i in range(len(x_data)):
        fig.add_trace(
            go.Scatter(
                x=x_data[i], y=y_data[i], name=names[i],
            )
        ),
        fig.update_layout(
            xaxis_title='Number of Days',
            yaxis_title='Cases',
        )

    return fig


headers = [
    'Comparison Graph (Normalised with Population)',
    'Comparison Graph (Normalised with Population)',
    'Comparison Graph (Normalised with Population)',
    'Comparison Graph (Normalised with Population)',
    'Comparison Graph (Without Normalization)',
    'Comparison Graph (Without Normalization)',
    'Comparison Graph (Without Normalization)',
    'Comparison Graph (Without Normalization)',
    'Comparison Graph (Without Normalization)',
    'Comparison Graph (Without Normalization)',
]
titles = [
    "Kenya, Italy, Brazil, South_Africa and India",
    "Kenya and Italy",
    "Kenya and India",
    "Kenya and Brazil",
    "Kenya and South Africa",
    "Kenya, Italy, Brazil, South_Africa and India",
    "Kenya and Italy",
    "Kenya and India",
    "Kenya and Brazil",
    "Kenya and South_Africa"
]
card_content = [card_template('graph' + str(i), headers[i], titles[i]) for i in range(10)]

mapbox_access_token = "pk.eyJ1IjoiY29sbGlucy1lbWFzaSIsImEiOiJjazl6aTgzdn" \
                      "UwOGJrM2dxcmNqdzBpYWJhIn0.KyaoBCDDKFxe3ofQNd-fKw"


# Layout for dash application
layout1 = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    children=[
                        dbc.Col(
                            className='rounded-lg four columns',
                            style={
                                'background': 'black',
                                'height': '450px',
                                'flex-grow': '1',
                            },
                            children=[
                                html.Div(
                                    style={
                                        'background': 'black',
                                    },
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
                                                            id='county-summary',
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
                                                                for i in kenya_data['County']
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
                                    ],
                                ),
                            ],
                            width=3,
                        ),
                        dbc.Col(
                            className='rounded-lg eight columns',
                            style={
                                'height': '450px', 'margin-left': '0%', 'padding-left': '0px', 'padding-right':'0px'
                            },
                            children=[
                                html.Div(
                                    children=[
                                        dcc.Graph(id='map-graph'),
                                    ],
                                ),
                            ],
                            width=6
                        ),
                        dbc.Col(
                            className='rounded-lg four',
                            style={
                                'background': 'black',
                                'height': '450px',
                            },
                            children=[
                                html.Div(
                                    children=[
                                        html.H2("GLOBAL"),
                                        html.P(id='total-cases'),
                                        html.P(id="total-deaths"),
                                        html.P(id="total-recovered"),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    className='heading-county-summary four',
                                                    children=[
                                                        html.H2("COUNTRIES"),
                                                    ]
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.Div(
                                                            className="county-summary-parag four",
                                                            children=[
                                                                html.P(id='global-summary'),
                                                            ]
                                                        ),
                                                    ],
                                                ),

                                            ]
                                        ),
                                    ]

                                ),
                            ],
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
    if county in all_const:
        constituencies = [const for const in all_const[county]]
        return [{"label": i, "value": i} for i in constituencies]
    else:
        return []


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
    cases_in_each_country = country_and_cases()
    sorted_countries = OrderedDict(sorted(cases_in_each_country.items(), key=lambda x: x[1][0], reverse=True))

    table_header = [
        html.Thead(
            html.Tr(
                children=[
                    html.Th("COUNTRY"),
                    html.Th("POSITIVE", className='cases-yellow'),
                    html.Th("DEATHS", className='cases-red')
                ],
            )
        )
    ]

    rows = []

    for country, compound in sorted_countries.items():
        row = html.Tr(
                [
                    html.Td(country),
                    html.Td(compound[0], className='cases-yellow'),
                    html.Td(compound[1], className='cases-red')
                ]
            )

        rows.append(row)

    table_body = [
        html.Tbody(
            rows
        )
    ]

    return dbc.Table(
        table_header + table_body,
        bordered=False,
        className='data-tables',
        dark=True,
        hover=True,
        responsive=True,
        striped=True,
    )


# Shows the summary of all the counties
@app.callback(
    Output("county-summary", "children"),
    [Input("county-dropdown", "value")]
)
def show_kenya_summary(_):
    counties = get_counties_and_cases()
    sorted_counties = OrderedDict(sorted(counties.items(), key=lambda x: x[1], reverse=True))

    table_header = [
        html.Thead(
            html.Tr(
                children=[
                    html.Th("COUNTY"),
                    html.Th("POSITIVE CASES", className='cases-yellow'),
                ],
                style={'color': 'primary'}
            )
        )
    ]

    rows = [
        html.Tr(
            [
                html.Td(county),
                html.Td(c, className='cases-yellow'),
            ]
        ) for county, c in sorted_counties.items()
    ]

    table_body = [
        html.Tbody(
            rows
        )
    ]

    return dbc.Table(
        table_header + table_body,
        bordered=False,
        className='data-tables',
        dark=True,
        hover=True,
        responsive=True,
        striped=True,
    )


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
    if county:
        for index, c in enumerate(kenya_data['County']):
            if c == county:
                break
        zoom = 8.0
        lat_initial = kenya_data['Lat'].loc[index]
        long_initial = kenya_data['Long'].loc[index]
    if county and subcounty:
        zoom = 11.0
        lat_initial = counties_constituencies_coords[county][subcounty]["Lat"]
        long_initial = counties_constituencies_coords[county][subcounty]["Long"]

    numbers = kenya_data[ke_date]
    sizes = list(numbers)
    for size in range(len(sizes)):
        if sizes[size] > 700:
            sizes[size] = 15
        elif sizes[size] > 500:
            sizes[size] = 13
        elif sizes[size] > 100:
            sizes[size] = 12
        elif sizes[size] > 60:
            sizes[size] = 10
        else:
            sizes[size] = 8

    return go.Figure(
        data=[
            # Data for all regions
            go.Scattermapbox(
                lat=confirmed_global["Lat"],
                lon=confirmed_global["Long"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=with_text['Text'] + with_text_d['Text'],
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
                    size=sizes,
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


layout2 = html.Div(
    [
        html.Div(
            [
                html.Div(
                    style={
                        'margin-top': '3%',
                        'margin-bottom': '3%',
                        'margin-right': '3%',
                        'margin-left': '3%',
                    },
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(card_content[0], color='primary', inverse=True, )),
                                dbc.Col(dbc.Card(card_content[2], color='secondary', inverse=True)),
                            ],
                            className='mb-4',
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(card_content[1], color='success', inverse=True)),
                                dbc.Col(dbc.Card(card_content[3], color='primary', inverse=True)),
                            ],
                            className='mb-4',
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(card_content[4], color='primary', inverse=True)),
                                dbc.Col(dbc.Card(card_content[5], color='secondary', inverse=True)),
                            ],
                            className='mb-4',
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(card_content[6], color='success', inverse=True)),
                                dbc.Col(dbc.Card(card_content[7], color='dark', inverse=True)),
                            ],
                            className='mb-4',
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(card_content[8], color='success', inverse=True)),
                                dbc.Col(dbc.Card(card_content[9], color='secondary', inverse=True)),
                            ],
                            className='mb-4',
                        ),
                    ],
                )
            ]
        ),
    ]
)


card = dbc.Card(
    children=[
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="KENYA NEWS", tab_id="kenya-news"),
                    dbc.Tab(label="GLOBAL NEWS", tab_id="global-news"),
                ],
                id="card-tabs-app3",
                card=True,
                active_tab="kenya-news",
            )
        ),
        dbc.CardBody(
            html.Div(
                id="card-content-app3", className="card-text"
            ),
        ),
    ],
)


@app.callback(
    Output("card-content-app3", "children"),
    [Input("card-tabs-app3", "active_tab")]
)
def tab_content_app3(active_tab):
    if active_tab == 'kenya-news':
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            style={
                                'color': 'black',
                                'height': '500px',
                                'overflow-y': 'scroll',
                                'overflow-x': 'hidden',
                                'width': '100%',
                            },
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            children=[
                                                html.H1('WHAT IS COVID-19?'),
                                                html.P(
                                                    "Coronavirus disease (COVID-19) is an infectious disease caused by a"
                                                    " newly discovered coronavirus."),
                                                html.P("Most people infected with the COVID-19 virus will experience "
                                                       "mild to moderate respiratory illness and recover without "
                                                       "requiring special treatment.  Older people, and those with "
                                                       "underlying medical problems like cardiovascular disease, "
                                                       "diabetes, chronic respiratory disease, and cancer are more "
                                                       "likely to develop serious illness."),
                                                html.P("The best way to prevent and slow down transmission is be well "
                                                       "informed about the COVID-19 virus, the disease it causes and "
                                                       "how it spreads. Protect yourself and others from infection by "
                                                       "washing your hands or using an alcohol based rub frequently and"
                                                       " not touching your face"),
                                                html.H1("NOTE:"),
                                                html.P("Seek immediate medical attention if you have serious symptoms."),
                                                html.P("Always call before visiting your doctor or health facility."),
                                                html.P(
                                                    "On average it takes 5–6 days from when someone is infected with "
                                                    "the virus for symptoms to show, however it can take up to 14 days."),
                                            ], width=4, className='mb-4'
                                        ),
                                        dbc.Col(
                                            [
                                                html.H1("SYMPTOMS"),
                                                html.P(
                                                    "MOST COMMON SYMPTOMS:",
                                                    style={"font-weight": "bold"}
                                                ),
                                                html.P("-Fever"),
                                                html.P("-Dry Cough"),
                                                html.P("-Tiredness"),
                                                html.P(
                                                    "LESS COMMON SYMPTOMS:",
                                                    style={"font-weight": "bold"}
                                                ),
                                                html.P("-Aches and pains"),
                                                html.P("-Sore throat"),
                                                html.P("-loss of taste or smell"),
                                                html.P("-Diarrhoea"),
                                                html.P("-Conjunctivitis"),
                                                html.P("-A rash on skin, or discolouration of fingers or toes"),
                                                html.P(
                                                    "SERIOUS SYMPTOMS:",
                                                    style={"font-weight": "bold"}
                                                ),
                                                html.P("-difficulty breathing or shortness of breath"),
                                                html.P("-chest pain or pressure"),
                                                html.P("-loss of speech or movement"),

                                            ], width=4, className='mb-4'
                                        ),
                                        dbc.Col(
                                            [
                                                html.H1("STAY HOME, WASH HANDS, SAVE LIVES"),
                                                html.P(
                                                    "STOP COVID-19 SPREAD:",
                                                    style={"font-weight": "bold"}
                                                ),
                                                html.P("1. Stay home for as long as you can"),
                                                html.P("2. If you have to get out, keep a safe distance"),
                                                html.P("3. Wash hands and sanitize as often as you can"),
                                                html.P("4. Cover your cough with elbow"),
                                                html.P("5. Follow government directives at all times."),
                                                html.P("6. SICK? call ahead."),
                                                html.P(
                                                    "NEED HELP?:",
                                                    style={"font-weight": "bold"}
                                                ),
                                                html.P("REDCROSS: 1199"),
                                                html.P("CALL CENTER: 719 or *719#"),
                                                html.P(
                                                    "REMEMBER:",
                                                    style={"font-weight": "bold"}
                                                ),
                                                html.P('"If you treat this disease normally, it will treat you abnormally"'),
                                                html.P(" ~ CS Mutahi Kagwe", style={'font-style': 'italic'}),
                                                html.P('"I can gerrit, you can gerrit, anybody can gerrit!"'),
                                                html.P(" ~ CS Mutahi Kagwe", style={'font-style': 'italic'}),
                                            ], width=4, className='mb-4'
                                        ),
                                    ], align='start'
                                ),

                            ],
                        ),
                    ]
                )
            ]
        )
    else:
        return 'Sorry, No news yet'


def ke_card_template(i_d, header, title):
    ke_card_temp = [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.H5(title, className='card-title'),
                dcc.Graph(figure=ke_fig(i_d), id=i_d),
            ]
        )
    ]
    return ke_card_temp


def ke_fig(i_d):
    if i_d == 'confirmed-graph':
        x, y = ke_axes_confirmed()
        name = 'KE Confirmed Cases'
    elif i_d == 'recoveries-graph':
        x, y = ke_axes_recoveries()
        name = 'KE Confirmed Recoveries '
    elif i_d == 'deaths-graph':
        x, y = ke_axes_deaths()
        name = 'KE confirmed Deaths'
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x, y=y, name=name, line=dict(color='firebrick', width=4),
        )
    ),
    fig.update_layout(
        xaxis_title='Number of Days',
        yaxis_title='Cases confirmed',
    )
    return fig


ke_headers = ['KENYAN CASES', 'KENYAN CASES', 'KENYAN CASES']
ke_titles = ['Confirmed', 'Recoveries', 'Deaths']
ids = ['confirmed-graph', 'recoveries-graph', 'deaths-graph']
ke_graphs = [ke_card_template(i_d, ke_header, ke_title) for i_d, ke_header, ke_title in zip(ids, ke_headers, ke_titles)]


app.layout = html.Div(
    className='bg-dark',
    children=[
        header_for_the_page(),
        html.Div(
            dbc.Card(
                className='bg-dark',
                children=[
                    dbc.CardHeader(
                        children=[
                            dbc.Tabs(
                                [
                                    dbc.Tab(label='HOME', tab_id='home', className='text-primary'),
                                    dbc.Tab(label='GRAPHS', tab_id='graphs', className='text-success'),
                                    dbc.Tab(label='NEWS', tab_id='news', className='text-info')
                                ],
                                id='card-tabs',
                                card=True,
                                active_tab='home',
                            ),

                        ],
                        style={'background': 'black'},
                    ),
                    dbc.CardBody(
                        html.Div(id='card-content', className='card-text'),
                    ),
                ],
                style={
                    "margin-left": "4%",
                    "margin-right": "4%",
                    "border": "none",
                },
            ),
        ),
        html.Div(
            style={
                "margin-left": "4%",
                "margin-right": "4%",
            },
            className='text-center',
            children=[
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(ke_graphs[0], color='primary', inverse=True, className='twelve columns'), width=4),
                        dbc.Col(dbc.Card(ke_graphs[1], color='secondary', inverse=True, className='twelve columns'), width=4),
                        dbc.Col(dbc.Card(ke_graphs[2], color='info', inverse=True, className='twelve columns'), width=4),
                    ]
                ),
            ]
        ),
    ]
)


@app.callback(
    Output('card-content', 'children'),
    [
        Input('card-tabs', 'active_tab')
    ]
)
def tab_content(active_tab):
    if active_tab == 'home':
        return layout1
    elif active_tab == 'graphs':
        return layout2
    elif active_tab == 'news':
        return card


if __name__ == "__main__":
    app.run_server(debug=True)