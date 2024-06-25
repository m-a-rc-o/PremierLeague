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
