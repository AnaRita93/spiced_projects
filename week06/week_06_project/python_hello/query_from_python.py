
from sqlalchemy import create_engine
import os

print('\nEXECUTING THE QUERY SCRIPT\n')

# connect to a database
username=${pingudb_user}
password=${pingudb_password}
#password = os.getenv('RDS_PASSWORD')
port = '5432'
host = 'database'
database = 'pingudb'

connection_string = f"postgres://{username}:{password}@{host}:{port}/{database}"
print(connection_string)

conn = create_engine(connection_string, echo=True)
print(conn)

# execute queries
query = """
CREATE TABLE IF NOT EXISTS penguins (
    name VARCHAR(20)
);
"""
result = conn.execute(query)

conn.execute("INSERT INTO penguins VALUES ('Skipper');")
conn.execute("INSERT INTO penguins VALUES ('Kowalski');")
conn.execute("INSERT INTO penguins VALUES ('Rico');")
conn.execute("INSERT INTO penguins VALUES ('Private');")
