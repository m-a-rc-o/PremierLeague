-- Show the ranking (according to points) in a given season (up to season 1975/1976)

DELIMITER //
CREATE PROCEDURE PointsRankingWithGoalAvg (IN SeasonID int)
BEGIN
    SELECT seasons.Season,
           ROW_NUMBER() OVER (ORDER BY Points DESC,
                             ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) DESC,
                             GoalsScored DESC) AS Position,
           Team,
           Points,
           GoalsScored,
           GoalsConceded,
           (GoalsScored-GoalsConceded) AS GoalDifference,
           ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) AS GoalAverage
    FROM seasonstats
    JOIN seasons
    ON seasonstats.Season = seasons.Season
    WHERE SeasonID = SeasonID;
END //

-- Show the ranking (according to points) in a given season (starting from season 1975/1976)

DELIMITER //
CREATE PROCEDURE PointsRankingWithGoalDiff (IN SeasonID int)
BEGIN
    SELECT seasons.Season,
           ROW_NUMBER() OVER (ORDER BY Points DESC,
                             (GoalsScored-GoalsConceded) DESC,
                             GoalsScored DESC) AS Position,
           Team,
           Points,
           GoalsScored,
           GoalsConceded,
           (GoalsScored-GoalsConceded) AS GoalDifference,
           ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) AS GoalAverage
    FROM seasonstats
    JOIN seasons
    ON seasonstats.Season = seasons.Season
    WHERE SeasonID = SeasonID;
END //

-- Show the ranking (according to goals scored) in a given season (up to season 1975/1976)

DELIMITER //
CREATE PROCEDURE GoalsScoredRankingWithGoalAvg (IN SeasonID int)
BEGIN
    SELECT seasons.Season,
           ROW_NUMBER() OVER (ORDER BY GoalsScored DESC,
                             Points DESC,
                             ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) DESC) AS GoalsScoredRanking,
           Team,
           Points,
           GoalsScored,
           ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) AS GoalAverage
    FROM seasonstats
    JOIN seasons
    ON seasonstats.Season = seasons.Season
    WHERE SeasonID = SeasonID;
END //

-- Show the ranking (according to goals scored) in a given season (starting from season 1975/1976)

DELIMITER //
CREATE PROCEDURE GoalsScoredRankingWithGoalDiff (IN SeasonID int)
BEGIN
    SELECT seasons.Season,
           ROW_NUMBER() OVER (ORDER BY GoalsScored DESC,
                             Points DESC,
                             (GoalsScored-GoalsConceded) DESC) AS GoalsScoredRanking,
           Team,
           Points,
           GoalsScored,
           (GoalsScored-GoalsConceded) AS GoalDifference
    FROM seasonstats
    JOIN seasons
    ON seasonstats.Season = seasons.Season
    WHERE SeasonID = SeasonID;
END //

-- Show the ranking (according to goals conceded) in a given season (up to season 1975/1976)

DELIMITER //
CREATE PROCEDURE GoalsConcededRankingWithGoalAvg (IN SeasonID int)
BEGIN
    SELECT seasons.Season,
           ROW_NUMBER() OVER (ORDER BY GoalsConceded,
                             Points DESC,
                             ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) DESC) AS GoalsConcededRanking,
           Team,
           Points,
           GoalsConceded,
           ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) AS GoalAverage
    FROM seasonstats
    JOIN seasons
    ON seasonstats.Season = seasons.Season
    WHERE SeasonID = SeasonID;
END //

-- Show the ranking (according to goals conceded) in a given season (starting from season 1975/1976)

DELIMITER //
CREATE PROCEDURE GoalsConcededRankingWithGoalDiff (IN SeasonID int)
BEGIN
    SELECT seasons.Season,
           ROW_NUMBER() OVER (ORDER BY GoalsConceded,
                             Points DESC,
                             (GoalsScored-GoalsConceded) DESC) AS GoalsConcededRanking,
           Team,
           Points,
           GoalsConceded,
           (GoalsScored-GoalsConceded) AS GoalDifference
    FROM seasonstats
    JOIN seasons
    ON seasonstats.Season = seasons.Season
    WHERE SeasonID = SeasonID;
END //

