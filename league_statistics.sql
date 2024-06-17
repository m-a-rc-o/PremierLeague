-- DROP ANY EXISTING VIEWS AND TABLES
DROP VIEW IF EXISTS GeneralStatistics;
DROP VIEW IF EXISTS WinsDrawsLosses;
DROP VIEW IF EXISTS Winners;
DROP VIEW IF EXISTS TitlesWon;
DROP VIEW IF EXISTS AvgPoints_2;
DROP VIEW IF EXISTS AvgPoints_3;
DROP VIEW IF EXISTS HomeStatistics;
DROP VIEW IF EXISTS AwayStatistics;
DROP TABLE IF EXISTS LeagueStatistics;

-- CREATE VIEWS
-- Some general statistics
CREATE VIEW GeneralStatistics AS
SELECT s.Team,
       COUNT(DISTINCT s.Season) AS SeasonsPlayed,
       AVG(fp.Position) AS AvgPosition,
       SUM(s.GoalsScored) AS TotalGoalsScored,
       SUM(s.GoalsConceded) AS TotalGoalsConceded,
       AVG(s.GoalsScored) AS AvgGoalsScoredPerSeason,
       AVG(s.GoalsConceded) AS AvgGoalsConcededPerSeason
FROM seasonstats AS s
JOIN FinalPositions AS fp
ON s.Season = fp.Season
AND s.Team = fp.Team
GROUP BY Team;

-- Total wins, draws and losses
CREATE VIEW WinsDrawsLosses AS
SELECT Team,
       SUM(Wins) AS TotalWins,
       SUM(Draws) AS TotalDraws,
       SUM(Losses) AS TotalLosses
FROM seasonstats
GROUP BY Team;

-- Winners of the league
CREATE VIEW Winners AS
SELECT Team,
       COUNT(DISTINCT Season) AS TitlesWon
FROM FinalPositions
WHERE Position = 1
GROUP BY Team;

-- Number of titles won by each team
CREATE VIEW TitlesWon AS
SELECT t.Team,
       CASE
           WHEN t.Team IN (SELECT Team FROM Winners) THEN w.TitlesWon
           ELSE 0
       END AS TitlesWon
FROM teams AS t
LEFT JOIN Winners AS w
ON t.Team = w.Team;

-- Average number of points (seasons with 2 pts per win)
CREATE VIEW AvgPoints_2 AS
SELECT Team,
       AVG(s.Points) AS AvgPoints_2ppw
FROM seasonstats AS s
JOIN PointsVsPositions AS pvp
ON s.Season = pvp.Season
WHERE pvp.PointsPerWin = 2
GROUP BY Team;

-- Average number of points (seasons with 3 pts per win)
CREATE VIEW AvgPoints_3 AS
SELECT Team,
       AVG(s.Points) AS AvgPoints_3ppw
FROM seasonstats AS s
JOIN PointsVsPositions AS pvp
ON s.Season = pvp.Season
WHERE pvp.PointsPerWin = 3
GROUP BY Team;

-- Total matches played,
-- average number of goals scored, conceded
-- and average goal difference as home team
CREATE VIEW HomeStatistics AS
SELECT Home AS Team,
       COUNT(*) AS TotalHomeMatchesPlayed,
       AVG(HomeGoals) AS AvgScored,
       AVG(AwayGoals) AS AvgConceded,
       AVG(HomeGoals-AwayGoals) AS AvgGoalDifference
FROM matches
GROUP BY Team;

-- Total matches played,
-- average number of goals scored, conceded
-- and average goal difference as away team
CREATE VIEW AwayStatistics AS
SELECT Away AS Team,
       COUNT(*) AS TotalAwayMatchesPlayed,
       AVG(AwayGoals) AS AvgScored,
       AVG(HomeGoals) AS AvgConceded,
       AVG(AwayGoals-HomeGoals) AS AvgGoalDifference
FROM matches
GROUP BY Team;

-- CREATE THE LEAGUE STATISTICS TABLE
CREATE TABLE LeagueStatistics (
    Team text,
    SeasonsPlayed int,
    TitlesWon int,
    AvgPosition float,
    TotalWins int,
    TotalDraws int,
    TotalLosses int,
    TotalGoalsScored int,
    TotalGoalsConceded int,
    AvgScoredPerSeason float,
    AvgConcededPerSeason float,
    AvgPoints_2ppw float,
    AvgPoints_3ppw float,
    Home_MatchesPlayed int,
    Home_AvgScored float,
    Home_AvgConceded float,
    Home_AvgGoalDiff float,
    Away_MatchesPlayed int,
    Away_AvgScored float,
    Away_AvgConceded float,
    Away_AvgGoalDiff float
);

-- Insert data from the views
INSERT INTO LeagueStatistics
SELECT gs.Team,
       gs.SeasonsPlayed,
       tw.TitlesWon,
       gs.AvgPosition,
       wdl.TotalWins,
       wdl.TotalDraws,
       wdl.TotalLosses,
       gs.TotalGoalsScored,
       gs.TotalGoalsConceded,
       gs.AvgGoalsScoredPerSeason,
       gs.AvgGoalsConcededPerSeason,
       ap2.AvgPoints_2ppw,
       ap3.AvgPoints_3ppw,
       hs.TotalHomeMatchesPlayed,
       hs.AvgScored,
       hs.AvgConceded,
       hs.AvgGoalDifference,
       aws.TotalAwayMatchesPlayed,
       aws.AvgScored,
       aws.AvgConceded,
       aws.AvgGoalDifference
FROM GeneralStatistics AS gs
JOIN WinsDrawsLosses AS wdl
ON gs.Team = wdl.Team
JOIN TitlesWon AS tw
ON gs.Team = tw.Team
LEFT JOIN AvgPoints_2 AS ap2
ON gs.Team = ap2.Team
LEFT JOIN AvgPoints_3 AS ap3
ON gs.Team = ap3.Team
JOIN HomeStatistics AS hs
ON gs.Team = hs.Team
JOIN AwayStatistics AS aws
ON gs.Team = aws.Team;
