import pandas as pd
import pygal
from pygal.style import CleanStyle

from mysql_connection import mysql_engine

# Define the queries
league_statistics_query = 'SELECT * FROM LeagueStatistics'
points_vs_positions_query = 'SELECT * FROM PointsVsPositions'
final_positions_query = 'SELECT * FROM FinalPositions'
matches_query = 'SELECT * FROM matches'

# Store the tables in different DataFrames
league_statistics = pd.read_sql(league_statistics_query, con=mysql_engine)
points_vs_positions = pd.read_sql(points_vs_positions_query, con=mysql_engine)
final_positions = pd.read_sql(final_positions_query, con=mysql_engine)
matches = pd.read_sql(matches_query, con=mysql_engine)

# Set appropriate indices for the DataFrames
league_statistics.set_index('Team', inplace=True)
final_positions.set_index(['Team', 'SeasonID'], inplace=True)
points_vs_positions.set_index('SeasonID', inplace=True)


# Define useful functions
def home_results(team, result):
    """Count the number of wins, draws or losses in the team's home matches."""
    if result.lower() == "wins":
        return matches[(matches['Home'] == team) & (matches['HomeGoals'] > matches['AwayGoals'])].shape[0]
    elif result.lower() == "draws":
        return matches[(matches['Home'] == team) & (matches['HomeGoals'] == matches['AwayGoals'])].shape[0]
    elif result.lower() == "losses":
        return matches[(matches['Home'] == team) & (matches['HomeGoals'] < matches['AwayGoals'])].shape[0]
    else:
        print("Invalid argument. Returned None.")
        return None


def away_results(team, result):
    """Count the number of wins, draws or losses in the team's home matches."""
    if result.lower() == "wins":
        return matches[(matches['Away'] == team) & (matches['HomeGoals'] < matches['AwayGoals'])].shape[0]
    elif result.lower() == "draws":
        return matches[(matches['Away'] == team) & (matches['HomeGoals'] == matches['AwayGoals'])].shape[0]
    elif result.lower() == "losses":
        return matches[(matches['Away'] == team) & (matches['HomeGoals'] > matches['AwayGoals'])].shape[0]
    else:
        print("Invalid argument. Returned None.")
        return None


def get_season_id(season):
    """Get the SeasonID for the given season."""
    try:
        return points_vs_positions[points_vs_positions['Season'] == season].index[0]
    except IndexError:
        print("Season " + season + " not found.")
        return None


def try_get_season_id(season):
    """Get the SeasonID for the given season.
       If the season is invalid, ask the user to enter a valid season.
    """
    season_id = None

    while season_id is None:
        season_id = get_season_id(season)
        if season_id is None:
            season = input("Please enter a valid season: ")

    return season_id


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
    wins = league_statistics.at[team, 'TotalWins']
    draws = league_statistics.at[team, 'TotalDraws']
    losses = league_statistics.at[team, 'TotalLosses']
    results = [wins, draws, losses]
    percentages = {
        'home wins': str(round(home_results(team, 'wins') / sum(results) * 100, 2)) + '%',
        'away wins': str(round(away_results(team, 'wins') / sum(results) * 100, 2)) + '%',
        'home draws': str(round(home_results(team, 'draws') / sum(results) * 100, 2)) + '%',
        'away draws': str(round(away_results(team, 'draws') / sum(results) * 100, 2)) + '%',
        'home losses': str(round(home_results(team, 'losses') / sum(results) * 100, 2)) + '%',
        'away losses': str(round(away_results(team, 'losses') / sum(results) * 100, 2)) + '%'
    }

    # Adding data to the pie chart
    pie_chart.add('Wins', [{'value': home_results(team, 'wins'), 'label': 'Home:' + percentages['home wins']},
                           {'value': away_results(team, 'wins'), 'label': 'Away:' + percentages['away wins']}])
    pie_chart.add('Draws', [{'value': home_results(team, 'draws'), 'label': 'Home:' + percentages['home draws']},
                            {'value': away_results(team, 'draws'), 'label': 'Away:' + percentages['away draws']}])
    pie_chart.add('Losses', [{'value': home_results(team, 'losses'), 'label': 'Home:' + percentages['home losses']},
                             {'value': away_results(team, 'losses'), 'label': 'Away:' + percentages['away losses']}])

    # Rendering chart in the browser
    pie_chart.render_in_browser()


def show_positions(teams, starting_from, to, fill=False):
    """Create a line chart showing the final positions of the given teams
    between the given start and end seasons."""
    # Matching the given seasons to their SeasonID
    start = try_get_season_id(starting_from)
    stop = try_get_season_id(to)

    # Obtaining the seasons list
    seasons = [points_vs_positions.at[i, 'Season'] for i in range(start, stop - 1, -1)]

    # Obtaining list with number of teams in the specified seasons
    number_of_teams = []
    for i in range(start, stop - 1, -1):
        number_of_teams.append(points_vs_positions.at[i, 'NumberOfTeams'])

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
                position = final_positions.loc[team, seasonID]['Position']
                positions.append(position)
            except KeyError:
                positions.append(None)
        line_chart.add(team, positions)

    # Rendering chart in the browser
    line_chart.render_in_browser()
