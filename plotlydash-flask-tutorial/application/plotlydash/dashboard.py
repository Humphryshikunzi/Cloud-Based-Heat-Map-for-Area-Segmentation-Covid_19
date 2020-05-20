"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from plotly import graph_objs as go 
from plotly.graph_objs import *
from .layout import html_layout


# Download Covid 19 data from data.humdata.org for analysis

confirmed_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv")
deaths_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv")
recovered_global = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv")


def Get_Country_Index():
    '''
      a dictionary with indexes for the Countries
    '''
  
    country_indexes = { 'Brazil' : 28,  'India' : 131, 'Italy' : 137, 'Kenya' : 142 , 'South Africa' : 200}
    
    return country_indexes
print(Get_Country_Index())

def Get_Country_Population():
    '''
    return the population of each country used in this project
    
    '''
    countries_population = { 'Brazil' : 217301365 ,  'India' : 1350716488,  'Italy' : 60472125, 'Kenya' : 53629525 , 'South Africa' : 59220561}
    return countries_population

def Get_Country_Cases(country_population, index_of_country = 142):
    '''
     This function gets an index of the country, with default of 142 for Kenya, and does as what the inline documentation
     says
     
    '''

    # get the total cases for a Country from the dowloaded data, using index for the Country, with default Kenya(142)
    get_covid = confirmed_global.iloc[[index_of_country]]

    # convert to 2D array
    get_covid_to_2D_array = np.array(get_covid)

    # convert to 1D array
    get_covid_to_1_array =  get_covid_to_2D_array[0]

    # get rid of lon, lat, Country, State and index
    get_covid_to_1_array_cleaned = np.array(get_covid_to_1_array[4:])

    # get the day the fisrt case was reported
    get_first_day = np.argmax(get_covid_to_1_array_cleaned > 0)

    # reduce the array to include elements only for days when the day first case was reported
    get_covid_cases = get_covid_to_1_array_cleaned[get_first_day:]

    # Normalise the final data
    get_covid_cases_normalised = (get_covid_cases / country_population)*100000

     # return a dictionary of cases for good visualization and normalised for plotting
    final_cases = {'cases' : get_covid_cases, 'cases_normalised': get_covid_cases_normalised }
    return  final_cases


# cases for each country, initial values and normalised

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

def create_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=[
                             '/static/dist/css/styles.css',
                             'https://fonts.googleapis.com/css?family=Lato'
                             ]
                         )

      # Custom HTML layout
    dash_app.index_string = html_layout



    # Create Layout
    dash_app.layout = html.Div(children=[
    html.H2('Comparing cases of Covid 19 in Kenya and Other Countries when Normalised'),
    html.H4('Normalization has been done, dividing everything by each coutry\'s population and multiplying everything by 100000'),
     dcc.Graph(id = "Graph Zero", figure ={
        'data' : [
            { 'x' : kenya_x_axis, 'y' :kenya_cases['cases_normalised'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
            { 'x' : italy_x_axis, 'y' : italy_cases['cases_normalised'], 'type' : 'line', 'name' : 'Italy_covid_19_cases'},          
            { 'x' : india_x_axis, 'y' : india_cases['cases_normalised'], 'type' : 'line', 'name' : 'India_covid_19_cases'},  
            { 'x' : brazil_x_axis, 'y' : brazil_cases['cases_normalised'], 'type' : 'line', 'name' : 'Brazil_covid_19_cases'},
            { 'x' : south_africa_x_axis, 'y' : south_africa_cases['cases_normalised'], 'type' : 'line', 'name' : 'South_Africa_Covid_19_cases'},  
        ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya against Italy, Brazil, South_Africa and India'
       }
       
    })
    ,
    dcc.Graph(id = "Graph 1", figure ={
        'data' : [
            { 'x' : kenya_x_axis, 'y' :kenya_cases['cases_normalised'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
            { 'x' :italy_x_axis, 'y' : italy_cases['cases_normalised'], 'type' : 'line', 'name' : 'Italy_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and Italy'
       }
       
    })
    ,
     dcc.Graph(id = "Graph 2", figure ={
        'data' : [
             { 'x' :kenya_x_axis, 'y' : kenya_cases['cases_normalised'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
             { 'x' : india_x_axis, 'y' :india_cases['cases_normalised'], 'type' : 'line', 'name' : 'India_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and India'
       }
       
    }),
     dcc.Graph(id = "Graph 3", figure ={
        'data' : [
             { 'x' : kenya_x_axis, 'y' : kenya_cases['cases_normalised'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
             { 'x' : brazil_x_axis, 'y' : brazil_cases['cases_normalised'], 'type' : 'line', 'name' : 'Brazil_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and Brazil'
       }
       
    }),
     dcc.Graph(id = "Graph 4", figure ={
        'data' : [
             { 'x' : kenya_x_axis, 'y' : kenya_cases['cases_normalised'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
             { 'x' : south_africa_x_axis, 'y' : south_africa_cases['cases_normalised'], 'type' : 'line', 'name' : 'South_Africa_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and South_Africa'
       }
       
    }),
     html.H2('Comparing cases of Covid 19 in Kenya and Other Countries'),
     dcc.Graph(id = "Graph 0.1", figure ={
        'data' : [
            { 'x' : kenya_x_axis, 'y' :kenya_cases['cases'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
            { 'x' : italy_x_axis, 'y' : italy_cases['cases'], 'type' : 'line', 'name' : 'Italy_covid_19_cases'},          
            { 'x' : india_x_axis, 'y' : india_cases['cases'], 'type' : 'line', 'name' : 'India_covid_19_cases'},  
            { 'x' : brazil_x_axis, 'y' : brazil_cases['cases'], 'type' : 'line', 'name' : 'Brazil_covid_19_cases'},
            { 'x' : south_africa_x_axis, 'y' : south_africa_cases['cases'], 'type' : 'line', 'name' : 'South_Africa_Covid_19_cases'},  
        ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya against Italy, Brazil, South_Africa and India'
       }
       
    })
    ,
    dcc.Graph(id = "Graph 1.1", figure ={
        'data' : [
            { 'x' : kenya_x_axis, 'y' :kenya_cases['cases'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
            { 'x' :italy_x_axis, 'y' : italy_cases['cases'], 'type' : 'line', 'name' : 'Italy_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and Italy'
       }
       
    })
    ,
     dcc.Graph(id = "Graph 2.1", figure ={
        'data' : [
             { 'x' :kenya_x_axis, 'y' : kenya_cases['cases'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
             { 'x' : india_x_axis, 'y' :india_cases['cases'], 'type' : 'line', 'name' : 'India_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and India'
       }
       
    }),
     dcc.Graph(id = "Graph 3.1", figure ={
        'data' : [
             { 'x' : kenya_x_axis, 'y' : kenya_cases['cases'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
             { 'x' : brazil_x_axis, 'y' : brazil_cases['cases'], 'type' : 'line', 'name' : 'Brazil_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and Brazil'
       }
       
    }),
     dcc.Graph(id = "Graph 4.1", figure ={
        'data' : [
             { 'x' : kenya_x_axis, 'y' : kenya_cases['cases'], 'type' : 'line', 'name' : 'Kenya_covid_19_cases'},
             { 'x' : south_africa_x_axis, 'y' : south_africa_cases['cases'], 'type' : 'line', 'name' : 'South_Africa_covid_19_cases'},          
       ],
         'layout' : {
           'title' : 'Comparison between Covid 19 cases in Kenya and South_Africa'
       }
       
    })

])
    return dash_app.server


