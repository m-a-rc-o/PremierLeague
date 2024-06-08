import pandas as pd
from sqlalchemy import create_engine

import configuration as config

query = 'SELECT Venue FROM matches'

mysql_engine = create_engine(config.connection_string)

df = pd.read_sql(query, con=mysql_engine)

print(df.head())
