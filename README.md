# Introduction: Premier League
The *Premier League* (PL) is the highest level of the English football league system.
The league was founded in 1922 from the ashes of the old *First Division*, which was England's top-tier football league since 1888.

The dataset, which can be found on [Kaggle](https://www.kaggle.com/datasets/evangora/premier-league-data), is made up of 4 csv files: 'matches.csv', 'seasons.csv', 'seasonstats.csv' and 'teams.csv'.
The information stored in these files refers to 125 football league seasons (First Division from season 1888/1889 to 1991/1992, Premier League from season 1992/1993 to 2023/2024) organized in 4 tables.
The tables can be obtained by importing the respective csv files into a SQL database (here SQLite was used).
Two of the tables ('seasons' and 'teams') provide a unique ID for each season and team, respectively.
The other two tables are 'seasonstats' and 'matches'. The former provides information about each team's statistics (such as wins, draws and losses) in a given season;
the latter, on the other hand, includes match-related statistics for each match played in a given season.

## Possible questions to explore
1. Is a team's final position in the league correlated with the total number of goals **scored** in the season? Can we find the relationship between these two quantities using linear regression? Is the linear approximation good enough?
2. Is a team's final position in the league correlated with the total number of goals **conceded** in the season?
3. How many points, on average, does a team need to *win* the league? How many points, on average, does a team need to *not be relegated* to 2nd division? REMEMBER: seasons with 2 or 3 points per win should be considered separately, and the number of relegated teams should be found for each season.
4. Average statistics (number of seasons played in the PL, number of goals per season, number of yellow and red cards per season, etc...) for each team.
5. Deep analysis of Manchester City's statistics in the season 2023/2024, in which the team won the PL.

## Preliminary operations
### Data cleaning and organization
In the 'data_cleaning.sql' file we apply some minor changes to the 4 tables in order to enhance their readability: in particular we rename most of the columns in the 'matches' and 'seasonstats' tables.

Notice that the 'matches' table contains a lot of empty rows, which we can identify with *invalid matches*; these rows provide only the *Season* information, while all of the other columns have `NULL` values.
We handle these rows in the 'invalid_matches.sql' file. The first query of the file counts the total number of invalid matches, and finds a total of 9961 empty rows distributed across the 125 seasons. 
Then we create a new table, called 'invalid_matches', in which we store information about the number of invalid matches for each season, identified by its unique *SeasonID*.
Finally, we delete all the empty rows from the 'matches' table.

### Obtaining the relevant tables
