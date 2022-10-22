from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table
from sqlalchemy import Integer, String
import sqlalchemy as sa
from variables import DB_URL

engine = create_engine(DB_URL,
                       echo=True)

metadata = MetaData(bind=engine)

videos_table = Table('videos', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('number', Integer),
                    Column('time', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
                    Column('frame', sa.BLOB),
                    )

# create tables in database
metadata.create_all()
#videos_table.drop(engine)

