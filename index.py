from dash_application.utils import *
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_application.app import app
from dash_application.apps import app1, app2


# Layout for dash application
app.layout = html.Div(
    [
        html.Div(
            dbc.Container(
                [
                    dbc.Button(
                        'HOME', color='primary', size='lg', className='mr-1',
                        href='/home'
                    ),
                    dbc.Button(
                        'GRAPHS', color='primary', size='lg', className='mr-1',
                        href='/graphs'
                    ),
                    dcc.Location('url', refresh=False)
                ]
            )
        ),
        header_for_the_page(),
        html.Div(id='page-content')
    ]
)


@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/graphs/' or pathname == '/graphs':
        return app2.layout
    elif pathname == '/home/' or pathname == '/home' or pathname == '/':
        return app1.layout


if __name__ == "__main__":
    app.run_server(debug=True)
