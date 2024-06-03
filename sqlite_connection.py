import pandas as pd
import sqlite3

database_path = '/Users/marcovasallucci/PycharmProjects/PremierLeague/identifier.sqlite'
conn = sqlite3.connect(database_path)

query = 'SELECT * FROM main.matches'
df = pd.read_sql_query(query, conn)
print(df.head())
