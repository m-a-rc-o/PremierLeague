from dash import Dash, html, dcc

from functions import league_statistics, final_positions, get_valid_seasons_options

# Define the external stylesheets
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Create lists containing all the teams and the seasons
teams = league_statistics.index.tolist()
seasons = final_positions.Season.unique().tolist()


def create_header(app: Dash) -> html.Div:
    """Create a header for the app."""
    return html.Div(
        children=[
            html.P("🏴󠁧󠁢󠁥󠁮󠁧󠁿", className="header-emoji"),
            html.H1("Premier League", className="header-title"),
            html.P("Analyzing the statistics "
                   "of England's top football league", className="header-description"),
        ],
        className="header",
    )


def create_dropdown_menu(app: Dash, name: str, items: list, season_options=False) -> html.Div:
    """Create a dropdown menu for the menu section.
    If the dropdown menu chooses the seasons,
    show only the valid seasons."""
    if season_options:
        options = get_valid_seasons_options(teams[0], items)
    else:
        options = [{"label": item, "value": item} for item in items]

    return html.Div(
        children=[
            html.Div(name, className="menu-title"),
            dcc.Dropdown(
                id=name.lower() + "-selector",
                options=options,
                value=options[0]["value"],
                clearable=False,
                className="dropdown"
            )
        ]
    )


def create_menu(app: Dash) -> html.Div:
    """Create a menu for the app."""
    return html.Div(
        children=[
            create_dropdown_menu(app, "Team", teams),
            create_dropdown_menu(app, "Season", seasons, season_options=True)
        ],
        className="menu"
    )


def create_chart_section(app: Dash) -> html.Div:
    """Create the chart section for the app."""
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id="radar-chart-gen",
                    )
                ],
                className="card"
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="bar-chart-match-avg",
                    )
                ],
                className="card"
            )
        ],
        className="wrapper"
    )
