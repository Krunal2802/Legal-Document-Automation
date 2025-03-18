from app.database import engine
from sqlalchemy import inspect
inspector = inspect(engine)
print(inspector.get_table_names()) # gives the tables list which are in the curent engine of PostgreSQL