import pandas as pd
import sqlite3

import configuration as config

conn = sqlite3.connect(config.database_path)

query = 'SELECT Venue FROM matches'
df = pd.read_sql_query(query, conn)
print(df.head())
