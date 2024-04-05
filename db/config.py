from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Replace the placeholders with your PostgreSQL connection details
db_user = 'postgres'
db_password = '1234'
db_host = 'localhost'
db_port = '5432'
db_name = 'auth_py'

# Create the connection string
db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create the engine

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)

Base = declarative_base()