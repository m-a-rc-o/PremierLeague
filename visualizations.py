import pygal
from pygal.style import CleanStyle
import plotly.express as px

import functions as f


# Define functions to generate plots
def pie_chart_results(team, inner_radius=.2):
    """Create a pie chart containing the results of the given team."""
    # Creating a pie chart object
    pie_chart = pygal.Pie(half_pie=True,
                          inner_radius=inner_radius,
                          style=CleanStyle(),
                          width=600,
                          height=400
                          )

    # Setting the title
    pie_chart.title = team + ' Results'

    # Preparing the data
    wins = f.league_statistics.at[team, 'TotalWins']
    draws = f.league_statistics.at[team, 'TotalDraws']
    losses = f.league_statistics.at[team, 'TotalLosses']
    results = [wins, draws, losses]
    percentages = {
        'home wins': str(round(f.home_results(team, 'wins') / sum(results) * 100, 2)) + '%',
        'away wins': str(round(f.away_results(team, 'wins') / sum(results) * 100, 2)) + '%',
        'home draws': str(round(f.home_results(team, 'draws') / sum(results) * 100, 2)) + '%',
        'away draws': str(round(f.away_results(team, 'draws') / sum(results) * 100, 2)) + '%',
        'home losses': str(round(f.home_results(team, 'losses') / sum(results) * 100, 2)) + '%',
        'away losses': str(round(f.away_results(team, 'losses') / sum(results) * 100, 2)) + '%'
    }

    # Adding data to the pie chart
    pie_chart.add('Wins', [{'value': f.home_results(team, 'wins'), 'label': 'Home:' + percentages['home wins']},
                           {'value': f.away_results(team, 'wins'), 'label': 'Away:' + percentages['away wins']}])
    pie_chart.add('Draws', [{'value': f.home_results(team, 'draws'), 'label': 'Home:' + percentages['home draws']},
                            {'value': f.away_results(team, 'draws'), 'label': 'Away:' + percentages['away draws']}])
    pie_chart.add('Losses', [{'value': f.home_results(team, 'losses'), 'label': 'Home:' + percentages['home losses']},
                             {'value': f.away_results(team, 'losses'), 'label': 'Away:' + percentages['away losses']}])

    # Rendering chart in the browser
    pie_chart.render_in_browser()


def show_positions(teams, starting_from, to, fill=False):
    """Create a line chart showing the final positions of the given teams
    between the given start and end seasons."""
    # Matching the given seasons to their SeasonID
    start = f.try_get_season_id(starting_from)
    stop = f.try_get_season_id(to)

    # Obtaining the seasons list
    seasons = [f.points_vs_positions.at[i, 'Season'] for i in range(start, stop - 1, -1)]

    # Obtaining list with number of teams in the specified seasons
    number_of_teams = []
    for i in range(start, stop - 1, -1):
        number_of_teams.append(f.points_vs_positions.at[i, 'NumberOfTeams'])

    # Obtaining max number of teams in the specified seasons
    max_teams = max(number_of_teams)

    # Define the graph settings
    settings = pygal.config.Config()
    settings.width = 600
    settings.height = 400
    settings.inverse_y_axis = True
    settings.x_label_rotation = 45
    settings.y_labels = list(range(1, max_teams + 1))
    settings.fill = fill
    settings.show_x_guides = True
    settings.show_y_guides = False

    # Creating a line chart object with the specified settings
    line_chart = pygal.Line(config=settings,
                            style=CleanStyle(opacity=.2)
                            )

    # Setting plot title and axes titles
    line_chart.title = 'Positions in the Premier League'
    line_chart.x_title = 'Season'
    line_chart.y_title = 'Position'

    # Setting seasons as x_labels
    line_chart.x_labels = seasons

    # Adding data to the line chart
    for team in teams:
        positions = []
        for seasonID in range(start, stop - 1, -1):
            try:
                position = f.final_positions.at[(team, seasonID), 'Position']
                positions.append(position)
            except KeyError:
                positions.append(None)
        line_chart.add(team, positions)

    # Rendering chart in the browser
    line_chart.render_in_browser()


def radar_chart(df, title, fields: list, labels: list, values_range="short", fill=True):
    """Create a radar chart showing the requested statistics
    of the team in the given season."""
    # Obtain the numerical values
    values = df[fields].to_numpy()

    # Set the radial range of the chart
    ranges = {"short": values.max() + 1,
              "long": round(values.max() + 10, -1)
              }
    r_min = 0
    r_max = ranges[values_range]

    # Create the chart
    fig = px.line_polar(r=values[0],
                        theta=labels,
                        line_close=True,
                        title=title,
                        height=625,
                        range_r=(r_min, r_max)
                        )

    # Update the chart's layout
    fig.update_layout(title_x=0.5,
                      title_font_family="Lato",
                      title_font_color="black",
                      title_font_size=37,
                      title_font_weight="bold",
                      font_family="Lato",
                      font_size=17
                      )

    # Fill the chart if requested
    if fill:
        fig.update_traces(fill="toself", line_width=1.5)

    return fig


def create_graphics(team, season):
    """Create the graphics for the dashboard"""
    # Check if the season is valid and obtain the seasonID
    # If the season is not valid, return None and None
    try:
        season_id = f.points_vs_positions.index[f.points_vs_positions['Season'] == season].tolist()[0]
    except IndexError:
        print("Season " + season + " not found.")
        return None, None

    # Check if the team participated in the league in the given season
    # If not return None, None
    try:
        df = f.data.loc[(team, season_id), :].to_frame(name=team).T
    except KeyError:
        print("Team " + team + " did not participate in the league in this season.")
        return None, None

    # Define the general statistics, their labels and the title
    gen_stats = ["GoalsScored", "GoalsConceded", "Wins%", "Draws%", "Losses%"]
    gen_stats_labels = ["Goals Scored", "Goals Conceded", "Wins (%)", "Draws (%)", "Losses (%)"]
    gen_title = "General: " + team + ", " + season

    # Define the match average statistics, their labels and the title
    match_avg_stats = ["GoalsScored/match", "GoalsConceded/match", "ShotsOnTarget/match",
                       "FoulsConceded/match", "YellowCards/match",
                       "Corners/match", "FreeKicks/match"]
    match_avg_labels = ["Goals Scored", "Goals Conceded", "Shots on Target",
                        "Fouls Conceded", "Yellow Cards",
                        "Corners", "Free Kicks"]
    match_avg_title = "Match Average: " + team + ", " + season

    # Create the radar charts
    fig_1 = radar_chart(df,
                        gen_title,
                        gen_stats,
                        gen_stats_labels,
                        values_range="long",
                        )

    fig_2 = radar_chart(df,
                        match_avg_title,
                        match_avg_stats,
                        match_avg_labels,
                        )

    return fig_1, fig_2
