from dash import Dash, html, dcc, Input, Output
import dash_vtk
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

cone = dash_vtk.Algorithm(
    id='vtk-algorithm',
    vtkClass='vtkConeSource',
    state={'resolution': 10},
)

cone_representation = dash_vtk.GeometryRepresentation(
    children=[cone],
    property={'color': [1, 0, 0]},
)

cone_view = dash_vtk.View(
    id='geometry-view',
    children=[cone_representation],
)

scene = html.Div(
    style={'height': '100%', 'width': '100%'},
    children=[cone_view],
)

controls = dbc.Card(
    [
        dbc.CardHeader('Controls'),
        dbc.CardBody(
            [
                html.P('Resolution:'),
                dcc.Slider(
                    id='slider-resolution',
                    min=10,
                    max=100,
                    step=1,
                    value=10,
                    marks={10: 'min', 20: '20', 30: '30', 40: '40', 50: '50',
                            60: '60', 70: '70', 80: '80', 90: '90', 100: 'max'},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
                html.Br(),
            ]
        )
    ]
)

board = dbc.Row(
    children=[
        dbc.Col(width=4, children=[controls]),
        dbc.Col(width=8, children=[scene]),
    ],
    style={'height': '100%'},
)

app.layout = dbc.Container(
    fluid=True,
    style={'marginTop': '15px', 'height': 'calc(100vh - 30px)'},
    children=[board],
)

@app.callback(
    [Output('vtk-algorithm', 'state'), Output('geometry-view', 'triggerResetCamera')],
    [Input('slider-resolution', 'value')],
)
def update_cone(slider_val):
    new_state = {'resolution': slider_val}
    return new_state, 1

if __name__ == '__main__':
    app.run(debug=True)