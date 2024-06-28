import pandas as pd

from mysql_connection import mysql_engine

# Define the queries
league_statistics_query = "SELECT * FROM LeagueStatistics"
points_vs_positions_query = "SELECT * FROM PointsVsPositions"
final_positions_query = "SELECT * FROM FinalPositions"
matches_query = "SELECT * FROM matches"
data_query = """
                    SELECT s.*, fp.Position, pvp.*, s.Season AS Season_ FROM seasonstats s JOIN FinalPositions fp 
                    ON s.Season = fp.Season AND s.Team = fp.Team JOIN PointsVsPositions pvp ON s.Season = pvp.Season 
                    ORDER BY Season_ 
                    """

# Store the tables in different DataFrames
league_statistics = pd.read_sql(league_statistics_query, con=mysql_engine)
points_vs_positions = pd.read_sql(points_vs_positions_query, con=mysql_engine)
final_positions = pd.read_sql(final_positions_query, con=mysql_engine)
matches = pd.read_sql(matches_query, con=mysql_engine)
data = pd.read_sql(data_query, con=mysql_engine).drop(columns="Season").rename(columns={"Season_": "Season"})

# Set appropriate indices for the DataFrames
league_statistics.set_index("Team", inplace=True)
final_positions.set_index(["Team", "SeasonID"], inplace=True)
points_vs_positions.set_index("SeasonID", inplace=True)
data.set_index(["Team", "SeasonID"], inplace=True)

# Add matches played column to data
data["MatchesPlayed"] = data["Wins"] + data["Draws"] + data["Losses"]

# Add wins, draws and losses percentage columns to data
data["Wins%"] = round(data["Wins"] / data["MatchesPlayed"] * 100, 2)
data["Draws%"] = round(data["Draws"] / data["MatchesPlayed"] * 100, 2)
data["Losses%"] = round(data["Losses"] / data["MatchesPlayed"] * 100, 2)

# Add columns containing average season statistics for the teams
data["GoalsScored/match"] = data["GoalsScored"] / data["MatchesPlayed"]
data["GoalsConceded/match"] = data["GoalsConceded"] / data["MatchesPlayed"]
data["Shots/match"] = data["Shots"] / data["MatchesPlayed"]
data["ShotsOnTarget/match"] = data["ShotsOnTarget"] / data["MatchesPlayed"]
data["FoulsConceded/match"] = data["FoulsConceded"] / data["MatchesPlayed"]
data["PassesAttempted/match"] = data["PassesAttempted"] / data["MatchesPlayed"]
data["PassesCompleted/match"] = data["PassesCompleted"] / data["MatchesPlayed"]
data["Corners/match"] = data["CornerKicks"] / data["MatchesPlayed"]
data["FreeKicks/match"] = data["FreeKicks"] / data["MatchesPlayed"]
data["YellowCards/match"] = data["YellowCards"] / data["MatchesPlayed"]


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
    """Count the number of wins, draws or losses in the team's away matches."""
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
        return points_vs_positions.index[points_vs_positions['Season'] == season].tolist()[0]
    except IndexError:
        print("Season " + season + " not found.")
        return None


def try_get_season_id(season):
    """
    Get the SeasonID for the given season.
    If the season is invalid, ask the user to enter a valid season.
    """
    season_id = None

    while season_id is None:
        season_id = get_season_id(season)
        if season_id is None:
            season = input("Please enter a valid season: ")

    return season_id


def list_of_seasons(team: str) -> list[str]:
    """Get the list of seasons in which
    the given team participated in the PL."""
    seasons = []
    for i in range(125):
        try:
            season = final_positions.at[(team, i), "Season"]
            seasons.append(season)
        except KeyError:
            continue

    return seasons


def get_valid_seasons_options(team: str, all_seasons: list[str]) -> list[dict]:
    """Get the list of valid seasons options for a given team."""
    valid_seasons = list_of_seasons(team)
    valid_seasons_options = [{"label": season, "value": season} for season in all_seasons]
    for item in valid_seasons_options:
        if item["value"] in valid_seasons:
            item["disabled"] = False
        else:
            item["disabled"] = True

    return valid_seasons_options


def list_of_teams(season: str, all_teams: list[str]) -> list[str]:
    """Get the list of teams that participated
    in the league in the given season."""
    list_of_indices = final_positions.index.tolist()
    season_id = try_get_season_id(season)
    participating_teams = []

    for team in all_teams:
        index = (team, season_id)
        if index in list_of_indices:
            participating_teams.append(team)

    return participating_teams


def get_data(team: str, season: str, fields: list[str], labels: list[str]):
    """Get all the requested stats for the team in the given season."""
    # Obtain the season_id and the DataFrame
    season_id = try_get_season_id(season)
    df = data.loc[(team, season_id), :].to_frame(name=team).T

    # Obtain the numerical values
    values = df[fields].to_numpy()[0]

    # Obtain a boolean mask with the null fields
    null_fields = [df[fields].isnull().at[team, field] for field in fields]

    # Create dictionary with valid fields among those requested
    updated_quantities = {labels[i]: values[i] for i in range(len(values)) if not null_fields[i]}
    new_values = [round(value, 2) for value in list(updated_quantities.values())]
    new_labels = list(updated_quantities.keys())

    return new_values, new_labels


def other_teams(team: str, season: str, all_teams: list[str]) -> dict[str, int]:
    """Get the list of the two teams preceding and following
    the requested team in the given season (if they exist)."""
    # Find the participating teams and the season_id
    participating_teams = list_of_teams(season, all_teams)
    season_id = try_get_season_id(season)

    # Obtain the position of the given team
    given_team_position = final_positions.at[(team, season_id), "Position"]

    # Obtain the other team's positions (including the position of the given team)
    positions = [(given_team_position - i) for i in range(2, -3, -1)]

    requested_teams = dict()
    for team in participating_teams:
        try:
            position = final_positions.at[(team, season_id), "Position"]
            if position in positions:
                requested_teams[team] = position
            else:
                continue
        except KeyError:
            continue

    # Order the dictionary by value
    ordered_teams = dict()
    for i in positions:
        for key, value in requested_teams.items():
            if value == i:
                ordered_teams[key] = value

    return ordered_teams
