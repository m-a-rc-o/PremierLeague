-- DROP ANY EXISTING VIEWS OR TABLES

DROP VIEW IF EXISTS FirstClassified;
DROP VIEW IF EXISTS SecondClassified;
DROP VIEW IF EXISTS ParticipatingTeams;
DROP TABLE IF EXISTS PointsVsPositions;

-- CREATE VIEW THAT SHOWS THE FIRST CLASSIFIED IN EACH SEASON
CREATE VIEW FirstClassified AS
SELECT Season,
       Team,
       Position,
       Points
FROM FinalPositions
WHERE Position = 1;

-- CREATE VIEW THAT SHOWS THE SECOND CLASSIFIED IN EACH SEASON
CREATE VIEW SecondClassified AS
SELECT Season,
       Team,
       Position,
       Points
FROM FinalPositions
WHERE Position = 2;

-- CREATE VIEW THAT COUNTS THE NUMBER OF PARTICIPATING TEAMS IN EACH SEASON
CREATE VIEW ParticipatingTeams AS
SELECT Season, COUNT(DISTINCT Team) AS NumberOfTeams
FROM seasonstats
GROUP BY Season;

-- CREATE THE POINTS VS POSITIONS TABLE
CREATE TABLE PointsVsPositions (
    SeasonID int,
    Season text,
    NumberOfTeams int,
    First text,
    PointsFirst int,
    Second text,
    PointsSecond int,
    PointsPerWin int
);

-- Insert data from the views
INSERT INTO PointsVsPositions
SELECT s.SeasonID,
       fc.Season,
       pt.NumberOfTeams,
       fc.Team,
       fc.Points,
       sc.Team,
       sc.Points,
       CASE
           WHEN fc.Season <= '1980/1981' THEN 2
           ELSE 3
       END
FROM FirstClassified AS fc
JOIN seasons AS s
ON fc.Season = s.Season
JOIN SecondClassified AS sc
ON fc.Season = sc.Season
JOIN ParticipatingTeams AS pt
ON fc.Season = pt.Season
ORDER BY fc.Season;
