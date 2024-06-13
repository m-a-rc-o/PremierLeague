# Introduction: Premier League
The *Premier League* (PL) is the highest level of the English football league system.
The league was founded in 1992 from the ashes of the old *First Division*, which was England's top-tier football league since 1888.

The dataset, which can be found on [Kaggle](https://www.kaggle.com/datasets/evangora/premier-league-data), is made up of 4 csv files: 'matches.csv', 'seasons.csv', 'seasonstats.csv' and 'teams.csv'.
The information stored in these files refers to 125 football league seasons (First Division from season 1888/1889 to 1991/1992, Premier League from season 1992/1993 to 2023/2024) organized in 4 tables.
The tables can be obtained by importing the respective csv files into a SQL database (here MySQL was used).
Two of the tables ('seasons' and 'teams') provide a unique ID for each season and team, respectively.
The other two tables are 'seasonstats' and 'matches'. The former provides information about each team's statistics (such as wins, draws and losses) in a given season;
the latter, on the other hand, includes match-related statistics for each match played in a given season.

## Possible questions to explore
1. Is a team's final position in the league correlated with the total number of goals **scored** in the season? Can we find the relationship between these two quantities using linear regression? Is the linear approximation good enough?
2. Is a team's final position in the league correlated with the total number of goals **conceded** in the season?
3. How many points, on average, does a team need to *win* the league? How many points, on average, does a team need to *not be relegated* to 2nd division? REMEMBER: seasons with 2 or 3 points per win should be considered separately, and the number of relegated teams should be found for each season.
4. Average statistics (number of seasons played in the PL, number of goals per season, number of yellow and red cards per season, etc...) for each team.
5. Deep analysis of Manchester City's statistics in the season 2023/2024, in which the team won the PL.

## Project outline
Coming soon...

## Project walkthrough
### Data cleaning and organization
In the 'data_cleaning.sql' file we apply some minor changes to the 4 tables in order to enhance their readability: in particular we rename most of the columns in the 'matches' and 'seasonstats' tables.

Notice that the 'matches' table contains a lot of empty rows, which we can identify with *invalid matches*; these rows provide only the *Season* information, while all of the other columns have `NULL` values.
We handle these rows in the 'invalid_matches.sql' file. The first query of the file counts the total number of invalid matches, and finds a total of 9961 empty rows distributed across the 125 seasons. 
Then we create a new table, called 'invalid_matches', in which we store information about the number of invalid matches for each season, identified by its unique *SeasonID*.
Finally, we delete all the empty rows from the 'matches' table.

### Obtaining the relevant tables
#### Final positions
First of all, we need a table that  provides information about the teams' ranking with respect to *Points*, *GoalsScored* and *GoalsConceded* in every season. We will call this table *FinalPositions*.
A question that naturally arises in this context is how to determine the positions in the ranking of two teams who finish the season with the **same** number of points.
According to the [official Premier League website](https://www.premierleague.com/premier-league-explained), "if any clubs finish with the same number of points, their position in the Premier League table is determined by goal difference, then the number of goals scored, then the team who collected the most points in the head-to-head matches, then who scored most away goals in the head-to-head".
This criterion, however, had only been adopted since the 1976/1977 season; in every season up to 1975/1976, **goal average** (the total number of goals scored divided by the total number of goals conceded) was used instead of goal difference.
In practice, it almost never happens that two teams finish with the same number of points, goal difference (or goal average) AND goals scored, so there is no need to check the head-to-head matches in these cases.
A rapid check shows that this situation has never occurred since 1976/1977 (when the goal difference criterion was used),

```sql
SELECT s1.Season,
       s1.Team AS Team1,
       s2.Team AS Team2,
       s1.Points,
       s1.GoalsScored,
       s1.GoalsConceded,
       (s1.GoalsScored-s1.GoalsConceded) AS GoalDifference
FROM seasonstats AS s1
JOIN seasonstats AS s2
ON s1.Season = s2.Season
AND s1.Points = s2.Points
AND (s1.GoalsScored-s1.GoalsConceded) = (s2.GoalsScored-s2.GoalsConceded)
AND s1.GoalsScored = s2.GoalsScored
AND s1.Team <> s2.Team
WHERE s1.Season >= '1976/1977'
ORDER BY s1.Season;
```

while it only occurred once when the goal average criterion was adopted,

```sql
SELECT s1.Season,
       s1.Team AS Team1,
       s2.Team AS Team2,
       s1.Points,
       s1.GoalsScored,
       s1.GoalsConceded,
       ROUND((CAST(s1.GoalsScored AS float)/CAST(s1.GoalsConceded AS float)), 3) AS GoalAverage
FROM seasonstats AS s1
JOIN seasonstats AS s2
ON s1.Season = s2.Season
AND s1.Points = s2.Points
AND ROUND((CAST(s1.GoalsScored AS float)/CAST(s1.GoalsConceded AS float)), 3) = ROUND((CAST(s2.GoalsScored AS float)/CAST(s2.GoalsConceded AS float)), 3)
AND s1.GoalsScored = s2.GoalsScored
AND s1.Team <> s2.Team
WHERE s1.Season < '1976/1977'
ORDER BY s1.Season;
```
namely in season 1907/1908, when Arsenal and Blackburn both finished the season with 36 points, a goal average of 0.810 and 51 goals scored.
In this case Arsenal finished in the 14th place and Blackburn in the 15th because of the head-to-heads,

```sql
SELECT s1.Season,
       s1.Team AS Home,
       s2.Team AS Away,
       m.HomeGoals,
       m.AwayGoals
FROM seasonstats AS s1
JOIN matches AS m
ON s1.Season = m.Season
AND s1.Team = m.Home
JOIN seasonstats AS s2
ON m.Away = s2.Team
AND s1.Season = s2.Season
AND s1.Points = s2.Points
AND ROUND((CAST(s1.GoalsScored AS float)/CAST(s1.GoalsConceded AS float)), 3) = ROUND((CAST(s2.GoalsScored AS float)/CAST(s2.GoalsConceded AS float)), 3)
AND s1.GoalsScored = s2.GoalsScored
AND s1.Team <> s2.Team
WHERE s1.Season < '1976/1977'
ORDER BY s1.Season;
```

Similarly, for the *GoalsScored* and *GoalsConceded* ranking we choose to classify the teams with the **same** number of goals scored (or conceded)
according to number of points and goal difference (or goal average, for the years before 1976/1977).
In the file 'ranking_views.sql' we create the following views:
- *PointsRanking*, which provides the teams' ranking (according to points) in every season;
- *GoalsScoredRanking*, which provides the teams' ranking (according to number of goals scored) in every season;
- *GoalsConcededRanking*, which provides the teams' ranking (according to number of goals conceded) in every season.

Finally we create the table *FinalPositions* by appropriately joining these views. 

#### PointsVsPositions
Now we need a table, which we will call *PointsVSPositions*, which provides information about the number of points needed to, respectively, win the league and not be relegated to Second Division.
To create this table we need to know, for each season, the number of points of the **2nd classified**, as this number represents a lower limit to the number of points needed to win the league;
we also need the number of points of the **last relegated team** (i.e. the highest ranked team among those that are then relegated), as this constitutes a lower limit to the number of points
needed to remain in First Division.

To obtain this information, we have to be careful about some subtleties:
1. we must distinguish between the seasons in which the two-points-per-win rule was applied and the seasons in which three points were awarded to every win;
2. we must distinguish between seasons with different numbers of participating teams;
3. we must obtain, for each season, the number of teams which were relegated, in order to obtain the ranking of the last relegated team.

The Premier League (or, formerly, the First Division) awards three points for each win since the 1981/1982 season;
this rule was originally adopted to reward a more attacking style of play, and it replaced the old rule (according to which two points were awarded for each win)
which had been used up to the 1980/1981 season.
For the moment, we will concentrate on determining the minimum number of points required to win the league;
we will address the problem of relegated teams later on in the project.

In the file 'points_vs_positions.sql' we create the following views:
- *FirstClassified*, which determines the teams that finish 1st in the league for each season, along with their number of points;
- *SecondClassified*, which performs the same analysis for the teams that finish 2nd;
- *ParticipatingTeams*, which calculates the number of participating teams in each edition of the league.

We then proceed to create the table *PointsVsPositions* by appropriately joining these views.


### Relegated teams
Coming soon...
