import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

layout = None

def generate_layout():
    print("Generating katy layout")
    global layout

    layout = html.Div(className="firework")
