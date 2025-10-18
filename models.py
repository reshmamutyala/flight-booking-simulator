from sqlalchemy import Column, Integer, String, Float
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    flight_id = Column(String, primary_key=True, index=True)
    flight_no = Column(String, index=True)
    origin = Column(String)
    destination = Column(String)
    departure_time = Column(String)
    arrival_time = Column(String)
    base_fare = Column(Float)
    dynamic_price = Column(Float)
    seats_available = Column(Integer)
    total_seats = Column(Integer)
    airline_tier = Column(String)
