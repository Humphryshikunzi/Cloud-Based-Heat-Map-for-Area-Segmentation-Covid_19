import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_application.utils import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


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
kenya_days  = len(kenya_cases['cases'])
italy_days  = len(italy_cases['cases'])
india_days  = len(india_cases['cases'])
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
    fig = {
        'data': [
            {'x': x_data[i], 'y': y_data[i], 'type': 'line', 'name': names[i]}
            for i in range(len(y_data))
        ]
    }

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


layout = html.Div(
    [
        dcc.Location('url', refresh=False),
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
                        dbc.Col(dbc.Card(card_content[0], color='primary', inverse=True,)),
                        dbc.Col(dbc.Card(card_content[2], color='secondary', inverse=True)),
                    ],
                    className='mb-4',
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(card_content[1], color='success', inverse=True)),
                        dbc.Col(dbc.Card(card_content[3], color='dark', inverse=True)),
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
                        dbc.Col(dbc.Card(card_content[9], color='dark', inverse=True)),
                    ],
                    className='mb-4',
                ),
            ],
        )
    ]
)
