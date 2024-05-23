from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
Base = declarative_base()
Session = sessionmaker(bind=engine)