# Dash app initialization
import dash
# User management initialization
import os
import dash_bootstrap_components as dbc
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config

from flask_socketio import SocketIO, emit
import flask

# external JavaScript files
external_scripts = [
    'https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js'
]

app = dash.Dash(
    __name__,
    url_base_pathname='/katy/',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=external_scripts
)

server = app.server
server.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(server)

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# config
server.config.update(
    SECRET_KEY=os.urandom(16),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
class User(UserMixin, base):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
