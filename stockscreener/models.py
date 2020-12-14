from sqlalchemy import Boolean, Column, ForeignKey, Numeric, Integer, String, Sequence, Table, MetaData
from sqlalchemy.orm import relationship

from database import Base

# class Stock(Base):
#     __tablename__ = "stocks"

#     id = Column(Integer, primary_key=True, index=True)
#     symbol = Column(String, unique=True, index=True)
#     price = Column(Numeric(10, 2))
#     forward_pe = Column(Numeric(10, 2))
#     forward_eps = Column(Numeric(10, 2))
#     dividend_yield = Column(Numeric(10, 2))
#     ma50 = Column(Numeric(10, 2))
#     ma200 = Column(Numeric(10, 2))
meta = MetaData()
class dailyData(Base):
    __tablename__ = 'Candle stick'
    #__table_args__ = {'sqlite_autoincrement': True}
    response_id = Column(Integer,primary_key=True,index=True)
    beg_time = Column(String)
    end_time = Column(String)
    symbol = Column(String)
    event = Column(String)
    vol = Column(Numeric(10)) 
    acc_vol = Column(Numeric(10))
    off_open_price = Column(Numeric(10))
    vwap = Column(Numeric(10))
    o = Column(Numeric(10))
    high = Column(Numeric(10))
    low = Column(Numeric(10))
    close = Column(Numeric(10))
    avg = Column(Numeric(10))

    
    #symbol = Column(String, unique=True, index=True)
    # forward_pe = Column(Numeric(10, 2))
    # forward_eps = Column(Numeric(10, 2))
    # dividend_yield = Column(Numeric(10, 2))
    # ma50 = Column(Numeric(10, 2))
    # ma200 = Column(Numeric(10, 2))