from sqlalchemy import create_engine

from configuration import connection_string

# Create a connection to the database
mysql_engine = create_engine(connection_string)
