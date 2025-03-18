from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL) # Creates a connection to the database.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # Helps create new database sessions.
Base = declarative_base() # This creates a base class for defining ORM models. All database models should inherit from Base.

def get_db():
    db = SessionLocal()  # Creates a new database session
    try: 
        yield db # This is a generator function that yields a session to be used in request handlers (commonly used in FastAPI).
    except:
        db.close() # Ensures the session is closed after use