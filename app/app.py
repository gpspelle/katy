from flask_socketio import emit
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app, server, socketio
from flask_login import logout_user, current_user
from views import login, login_fd, logout
from views import katy

from settings import *
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO)

@socketio.on("launch")
def launch():
    print(" [-] Received majelan")
    socketio.emit("launch_firework")

@socketio.on("connect")
def test_connect():
    print(" [.] Client connected")

@socketio.on("disconnect")
def test_disconnect():
    print(" [x] Client disconnected")

tabs = ['katy']

logging.info(" [.] Initalizing layouts")

katy.generate_layout()

logging.info(" [.] Final steps and we're ready")
header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src='assets/dash-logo-stripe.svg',
                className='logo'
            )
        ]
    )
)

app.validation_layout = html.Div([
    login.layout,
    logout.layout,
    katy.layout,
])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    'background-color': "#2D2F3E",
    'font-family': 'Circular Std', 
    'font-weight': 'bold', 
    'color': 'white'
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "22rem",
}

sidebar = html.Div(
    [
        html.Div([
            html.Img(
                src=app.get_asset_url("majelan-logo.png"),
                id="majelan-logo",
                    style={
                        "height": "110px",
                        "width": "auto",
                        "margin-bottom": "0px",
                    },
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Katy", href="/katy/katy", id="katy")),
                ],
                vertical=True,
                pills=True,
            ),
        ], style=SIDEBAR_STYLE),
        html.Div(
            className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ], 
            style={'position': 'fixed',
                "padding": "2rem 1rem",
                "width": "16rem",
                'bottom': '0',
                'left': '0',
                'color': 'white'
        })
    ],
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id='url', refresh=False), content])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    Output("katy", "disabled"),
    [Input("url", "pathname")],
)
def toggle_disabled_links(pathname):
    if ENV == "dev": 
        return False
    elif current_user.is_authenticated:
        return False
    else:
        return True
    
@app.callback(
    Output("katy", "active"),
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == '/katy/katy':
        return True
    else:
        return False


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if ENV == "dev": 
        if pathname == '/katy/':
            return [sidebar, katy.layout]
        elif pathname == '/katy/login':
            return [sidebar, katy.layout]
        elif pathname == '/katy/logout':
            return logout.layout
        elif pathname == '/katy/katy':
            return [sidebar, katy.layout]
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
    else:
        if pathname == '/katy/':
            return [login.layout]
        elif pathname == '/katy/login':
            return [sidebar, login.layout]
        elif pathname == '/katy/logout':
            if current_user.is_authenticated:
                logout_user()
                return logout.layout
            else:
                return logout.layout
        elif pathname == '/katy/katy':
            if current_user.is_authenticated:
                return [sidebar, katy.layout]
            else:
                return login.layout
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )

@app.callback(
    [Output('user-name', 'children'),
     Output('logout', 'children')],
    [Input('page-content', 'children')])
def go_to_platform(input1):
    if current_user.is_authenticated:
        return html.Div('User: ' + current_user.username), dcc.Link('Logout', href='/katy/logout')
    else:
        return '', ''


if __name__ == '__main__':
    if ENV == "production":
        socketio.run(server, host="147.135.137.147", port=5000)
        #app.run_server(host="147.135.137.147", debug=True, port=5000)
    else:
        socketio.run(server)
        #app.run_server(host="127.0.0.1", debug=True, port=5000)
