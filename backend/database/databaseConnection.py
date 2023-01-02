from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sql_database_url="postgresql://postgres:root@localhost:5432/rentswipe"

engine=create_engine(sql_database_url)

sessionLocal=sessionmaker(autocommit=False,bind=engine)

base=declarative_base()