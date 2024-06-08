-- DATA CLEANING

-- Removing seasons with null IDs from 'seasons'
DELETE
FROM seasons
WHERE SeasonID IS NULL;

-- Removing teams with null IDs from 'teams'
DELETE
FROM teams
WHERE TeamID IS NULL;

-- Adding descriptive names for columns in 'matches'
ALTER TABLE matches
RENAME COLUMN xG TO ExpectedGoalsHome;

ALTER TABLE matches
RENAME COLUMN `Home Goals` TO HomeGoals;

ALTER TABLE matches
RENAME COLUMN `Away Goals` TO AwayGoals;

ALTER TABLE matches
RENAME COLUMN `xG.1` TO ExpectedGoalsAway;

-- Adding descriptive names for columns in 'seasonstats'
ALTER TABLE seasonstats
RENAME COLUMN W TO Wins;

ALTER TABLE seasonstats
RENAME COLUMN D TO Draws;

ALTER TABLE seasonstats
RENAME COLUMN L TO Losses;

ALTER TABLE seasonstats
RENAME COLUMN GF TO GoalsScored;

ALTER TABLE seasonstats
RENAME COLUMN GA TO GoalsConceded;

ALTER TABLE seasonstats
RENAME COLUMN Pts TO Points;

ALTER TABLE seasonstats
RENAME COLUMN Sh TO Shots;

ALTER TABLE seasonstats
RENAME COLUMN SoT TO ShotsOnTarget;

ALTER TABLE seasonstats
RENAME COLUMN FK TO FreeKicks;

ALTER TABLE seasonstats
RENAME COLUMN PK TO PenaltyKicksGoals;

ALTER TABLE seasonstats
RENAME COLUMN Cmp TO PassesCompleted;

ALTER TABLE seasonstats
RENAME COLUMN Att TO PassesAttempted;

ALTER TABLE seasonstats
RENAME COLUMN `Cmp%` TO PassCompletionRate;

ALTER TABLE seasonstats
RENAME COLUMN CK TO CornerKicks;

ALTER TABLE seasonstats
RENAME COLUMN CrdY TO YellowCards;

ALTER TABLE seasonstats
RENAME COLUMN CrdR TO RedCards;

ALTER TABLE seasonstats
RENAME COLUMN Fls TO FoulsConceded;

ALTER TABLE seasonstats
RENAME COLUMN OG TO OwnGoals;

ALTER TABLE seasonstats
RENAME COLUMN PKcon TO PenaltiesConceded;
