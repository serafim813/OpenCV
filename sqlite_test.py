from sqlite import videos_table
from sqlalchemy.sql import select

s = select([videos_table])
result = s.execute()

for row in result:
    print(row)


