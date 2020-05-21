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
