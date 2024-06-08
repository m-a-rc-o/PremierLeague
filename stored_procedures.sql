-- Show the ranking (according to points) in a given season (up to season 1975/1976)

-- CLASSIFICA PUNTI (fino al 1975/1976)

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
WHERE SeasonID = 122;



-- CLASSIFICA PUNTI (a partire dal 1976/1977)

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
WHERE SeasonID = 22;

-- CLASSIFICA GOAL SEGNATI (fino al 1975/1976)

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
WHERE SeasonID = 122;

-- CLASSIFICA GOAL SEGNATI (a partire dal 1976/1977)

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
WHERE SeasonID = 22;

-- CLASSIFICA GOAL SUBITI (fino al 1975/1976)

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
WHERE SeasonID = 122;

-- CLASSIFICA GOAL SUBITI (a partire dal 1976/1977)

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
WHERE SeasonID = 22;
