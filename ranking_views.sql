-- DROP ANY EXISTING VIEWS OR TABLES

DROP VIEW IF EXISTS PointsRanking;
DROP VIEW IF EXISTS GoalsScoredRanking;
DROP VIEW IF EXISTS GoalsConcededRanking;
DROP TABLE IF EXISTS FinalPositions;

-- CREATE VIEW WITH POINTS RANKING
-- Use the goal average criterion for seasons up to 1975/1976
CREATE VIEW PointsRanking AS
SELECT Season,
       ROW_NUMBER() OVER (PARTITION BY Season
                         ORDER BY Points DESC,
                         ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) DESC,
                         GoalsScored DESC,
                         Team) AS Position, -- Here we order by team to make sure that Arsenal comes before Blackburn in season 1907/1908
       Team,
       Points,
       GoalsScored,
       GoalsConceded,
       (GoalsScored-GoalsConceded) AS GoalDifference,
       ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) AS GoalAverage
FROM seasonstats
WHERE Season <= '1975/1976'

UNION

-- Use the goal difference criterion starting from season 1976/1977
SELECT Season,
       ROW_NUMBER() OVER (PARTITION BY Season
                         ORDER BY Points DESC,
                         (GoalsScored-GoalsConceded) DESC,
                         GoalsScored DESC) AS Position,
       Team,
       Points,
       GoalsScored,
       GoalsConceded,
       (GoalsScored-GoalsConceded) AS GoalDifference,
       ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) AS GoalAverage
FROM seasonstats
WHERE Season >= '1976/1977';

-- CREATE VIEW WITH GOALS SCORED RANKING
-- Use the goal average criterion for seasons up to 1975/1976
CREATE VIEW GoalsScoredRanking AS
SELECT Season,
       ROW_NUMBER() OVER (PARTITION BY Season
                         ORDER BY GoalsScored DESC,
                         Points DESC,
                         ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) DESC,
                         Team) AS GoalsScoredRanking, -- Here we order by team to make sure that Arsenal comes before Blackburn in season 1907/1908
       Team
FROM seasonstats
WHERE Season <= '1975/1976'

UNION

-- Use the goal difference criterion starting from season 1976/1977
SELECT Season,
       ROW_NUMBER() OVER (PARTITION BY Season
                         ORDER BY GoalsScored DESC,
                         Points DESC,
                         (GoalsScored-GoalsConceded) DESC) AS Position,
       Team
FROM seasonstats
WHERE Season >= '1976/1977';

-- CREATE VIEW WITH GOALS CONCEDED RANKING
-- Use the goal average criterion for seasons up to 1975/1976
CREATE VIEW GoalsConcededRanking AS
SELECT Season,
       ROW_NUMBER() OVER (PARTITION BY Season
                         ORDER BY GoalsConceded,
                         Points DESC,
                         ROUND((CAST(GoalsScored AS float)/CAST(GoalsConceded AS float)), 3) DESC,
                         Team) AS GoalsConcededRanking, -- Here we order by team to make sure that Arsenal comes before Blackburn in season 1907/1908
       Team
FROM seasonstats
WHERE Season <= '1975/1976'

UNION

-- Use the goal difference criterion starting from season 1976/1977
SELECT Season,
       ROW_NUMBER() OVER (PARTITION BY Season
                         ORDER BY GoalsConceded,
                         Points DESC,
                         (GoalsScored-GoalsConceded) DESC) AS Position,
       Team
FROM seasonstats
WHERE Season >= '1976/1977';

-- CREATE THE FINAL POSITIONS TABLE

CREATE TABLE FinalPositions (
    SeasonID int,
    Season text,
    Team text,
    Points int,
    GoalsScored int,
    GoalsConceded int,
    Position int,
    GoalsScoredRanking int,
    GoalsConcededRanking int,
    GoalDifference int,
    GoalAverage float
);

-- Insert data from the views
INSERT INTO FinalPositions
SELECT s.SeasonID,
       PR.Season,
       PR.Team,
       PR.Points,
       PR.GoalsScored,
       PR.GoalsConceded,
       PR.Position,
       GSR.GoalsScoredRanking,
       GCR.GoalsConcededRanking,
       PR.GoalDifference,
       PR.GoalAverage
FROM pointsranking AS PR
JOIN seasons AS s
ON PR.Season = s.Season
JOIN goalsscoredranking AS GSR
ON PR.Season = GSR.Season
AND PR.Team = GSR.Team
JOIN goalsconcededranking AS GCR
ON PR.Season = GCR.Season
AND PR.Team = GCR.Team
ORDER BY PR.Season, PR.Position;
