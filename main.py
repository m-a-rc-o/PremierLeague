from dash import Input, Output
from dash.exceptions import PreventUpdate

from dashboard_sections import *
from functions import list_of_teams
from visualizations import create_graphics

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Premier League Statistics"

app.layout = html.Div(
    children=[
        create_header(app),
        create_menu(app),
        create_chart_section(app),
    ]
)


@app.callback(
    Output("season-selector", "options"),
    Input("team-selector", "value")
)
def set_season_options(selected_team):
    return get_valid_seasons_options(selected_team, seasons)


@app.callback(
    Output("radar-chart-gen", "figure"),
    Output("bar-chart-match-avg", "figure"),
    Input("team-selector", "value"),
    Input("season-selector", "value")
)
def update_chart_section(selected_team, selected_season):
    if selected_team in list_of_teams(selected_season, teams):
        return create_graphics(selected_team, selected_season)
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run(debug=True)
