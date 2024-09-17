from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

# Customer model
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)

# Campaign model
class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    start_date = Column(DateTime)
