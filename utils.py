import numpy as np
import pandas as pd
import dash_html_components as html

confirmed_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv")
deaths_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv")
recovered_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv")
with_text = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv")
# confirmed_global = pd.read_csv("assets/time_series_covid19_confirmed_global.csv")
# deaths_global = pd.read_csv("assets/time_series_covid19_deaths_global.csv")
# recovered_global = pd.read_csv("assets/time_series_covid19_recovered_global.csv")
# with_text = pd.read_csv("assets/time_series_covid19_confirmed_global.csv")

confirmed = pd.read_csv("assets/testdata.csv")
confirmed = confirmed.fillna(0)

kenya_data = pd.read_excel("assets/complete_set.xlsx")
ke_with_text = pd.read_excel('assets/complete_set.xlsx')


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


# update number of hours
def show_24_hours_c():
    today = get_today(confirmed_global)
    yesterday = get_prev_date(confirmed_global)
    c_index, _, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = confirmed_global.loc[c_index, today] - confirmed_global.loc[c_index, yesterday]
    return f"+{difference} in past 24hrs"


def show_24_hours_d():
    today = get_today(deaths_global)
    yesterday = get_prev_date(deaths_global)
    _, d_index, _ = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = deaths_global.loc[d_index, today] - deaths_global.loc[d_index, yesterday]
    return f"+{difference} in past 24hrs"


def show_24_hours_r():
    today = get_today(recovered_global)
    yesterday = get_prev_date(recovered_global)
    _, _, r_index = get_kenya_index_from_global(confirmed_global, deaths_global, recovered_global)
    difference = recovered_global.loc[d_index, today] - recovered_global.loc[d_index, yesterday]
    return f"+{difference} in past 24hrs"


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
                                    html.P(show_24_hours_c(), className='hrs-24', id='c-hrs-element'),
                                    html.H1(update_kenya_confirmed(), className='cases-num', id='cases-element'),
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
cases_in_each_country = country_and_cases()
list_cases_in_each_country = []
for cases_c in cases_in_each_country.items():
    list_cases_in_each_country.append([cases_c[0], cases_c[1]])
sorted_countries = sorted(list_cases_in_each_country, key=lambda x: x[1], reverse=True)
with_text['Text'] = with_text['Country/Region'] + '<br>Cases: ' + (with_text[date]).astype(str)