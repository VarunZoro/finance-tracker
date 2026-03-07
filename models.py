from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable = False)
    category = Column(String, nullable = False)
    type = Column(String, nullable= False)
    date = Column(Date, default=datetime.date.today)
    notes = Column(String, nullable=True)
    
