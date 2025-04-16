from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# All ORM models will inherit from this class 