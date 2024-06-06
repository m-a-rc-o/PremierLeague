-- INVALID MATCHES

-- Counting the total number of invalid matches

SELECT COUNT(*) AS TotalInvalidMatches
FROM matches
WHERE COALESCE(Date,
               Home,
               ExpectedGoalsHome,
               HomeGoals,
               AwayGoals,
               ExpectedGoalsAway,
               Away,
               Attendance,
               Venue) IS NULL;

-- Storing the number of invalid matches for each season in a new table

CREATE TABLE invalid_matches (
    SeasonID int NOT NULL PRIMARY KEY,
    NumberOfInvalidMatches int
);

INSERT INTO invalid_matches
SELECT SeasonID,
       COUNT(*) AS NumberOfInvalidMatches
FROM seasons
LEFT JOIN matches
ON seasons.Season = matches.Season
WHERE COALESCE(Date,
               Home,
               ExpectedGoalsHome,
               HomeGoals,
               AwayGoals,
               ExpectedGoalsAway,
               Away,
               Attendance,
               Venue) IS NULL
GROUP BY SeasonID;

-- Deleting the empty rows from the matches table

DELETE
FROM matches
WHERE COALESCE(Date,
               Home,
               ExpectedGoalsHome,
               HomeGoals,
               AwayGoals,
               ExpectedGoalsAway,
               Away,
               Attendance,
               Venue) IS NULL;