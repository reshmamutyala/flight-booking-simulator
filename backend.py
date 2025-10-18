from fastapi import FastAPI,Query,BackgroundTasks

app = FastAPI(title="Flight Booking Simulator with Dynamic Pricing")

# --- Sample flight data ---
flights = [
    {"id": 1, "airline": "IndiGo", "origin": "HYD", "destination": "BLR", "date": "2025-10-18", "price": 3200},
    {"id": 2, "airline": "Air India", "origin": "HYD", "destination": "DEL", "date": "2025-10-20", "price": 4500},
    {"id": 3, "airline": "SpiceJet", "origin": "BLR", "destination": "MUM", "date": "2025-11-01", "price": 2700},
]

# --- Route to get all flights ---
from typing import List,Optional
@app.get("/flights")
def get_all_flights():
    return {"flights": flights}
@app.get("/flights/search")
def search_flights(
    origin: Optional[str] = Query(None, description="Origin airport code, e.g. HYD"),
    destination: Optional[str] = Query(None, description="Destination airport code, e.g. DEL"),
    date: Optional[str] = Query(None, description="Flight date in YYYY-MM-DD format"),
):
    results = flights

    # Filter step-by-step if provided
    if origin:
        results = [f for f in results if f["origin"].lower() == origin.lower()]
    if destination:
        results = [f for f in results if f["destination"].lower() == destination.lower()]
    if date:
        results = [f for f in results if f["date"] == date]

    return {"results": results, "count": len(results)}
from pydantic import BaseModel,Field
class Flight(BaseModel):
    id: int
    airline: str
    origin: str = Field(..., min_length=3, max_length=3, description="Origin airport code (e.g. HYD)")
    destination: str = Field(..., min_length=3, max_length=3, description="Destination airport code (e.g. DEL)")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date in YYYY-MM-DD format")
    price: float = Field(..., gt=0, description="Ticket price (must be positive)")
flights = [
    Flight(id=1, airline="IndiGo", origin="HYD", destination="BLR", date="2025-10-18", price=3200),
    Flight(id=2, airline="Air India", origin="HYD", destination="DEL", date="2025-10-20", price=4500),
    Flight(id=3, airline="SpiceJet", origin="BLR", destination="MUM", date="2025-11-01", price=2700),
    Flight(id=4, airline="Vistara", origin="DEL", destination="HYD", date="2025-10-18", price=4100),
]

#  Get all flights (with optional sorting by price)
@app.get("/flight", response_model=List[Flight])
def get_all_flights(sort_by: Optional[str] = Query(None, description="Use 'price' to sort by ticket price")):
    if sort_by == "price":
        return sorted(flights, key=lambda f: f.price)
    return flights
# Flight model
from datetime import date,timedelta
import random
class Flight(BaseModel):
    id: int
    airline: str
    origin: str
    destination: str
    date: str
    duration: int
    price: float

# Simulated external airline APIs
def indigo_api():
    return [Flight(
        id=101,
        airline="IndiGo",
        origin="HYD",
        destination="BLR",
        date=str(date.today() + timedelta(days=1)),
        duration=75,
        price=random.randint(3000, 4000)
    )]

def airindia_api():
    return [Flight(
        id=102,
        airline="Air India",
        origin="HYD",
        destination="DEL",
        date=str(date.today() + timedelta(days=2)),
        duration=140,
        price=random.randint(4000, 5000)
    )]

def spicejet_api():
    return [Flight(
        id=103,
        airline="SpiceJet",
        origin="BLR",
        destination="MUM",
        date=str(date.today() + timedelta(days=3)),
        duration=95,
        price=random.randint(2500, 3500)
    )]

# Aggregate flights from all simulated APIs
def get_all_flights_data():
    flights = []
    flights.extend(indigo_api())
    flights.extend(airindia_api())
    flights.extend(spicejet_api())
    return flights

# Endpoint to get all flights
@app.get("/flights", response_model=List[Flight])
def get_all_flights():
    return get_all_flights_data()
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import asyncio
from dynamic_pricing import dynamic_price  # import function from separate file

app = FastAPI(title="Flight Booking with Dynamic Pricing")

# Request model
class FlightPricing(BaseModel):
    id: int
    airline: str
    base_fare: float
    total_seats: int
    seats_available: int       
    departure_time: str
    tier: Optional[str] = "standard"
    dynamic_price: Optional[float] = None

# POST endpoint for dynamic pricing
@app.post("/dynamic_pricing")
def calculate_dynamic_price(data: FlightPricing):
    price = dynamic_price(
        base_fare=data.base_fare,
        total_seats=data.total_seats,
        seats_available=data.seats_available,
        departure_time=data.departure_time,
        tier=data.tier
    )
    return {
        "message": "Dynamic price calculated successfully",
        "base_fare": data.base_fare,
        "new_price": price
    }
import asyncio
import random
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Import your dynamic pricing function
from dynamic_pricing import dynamic_price

# --- FlightPricing model ---
class FlightPricing(BaseModel):
    id: int
    airline: str
    base_fare: float
    total_seats: int
    seats_available: int
    departure_time: str  # YYYY-MM-DD
    tier: Optional[str] = "standard"
    dynamic_price: Optional[float] = None
    price_history: List[float] = []

    model_config = {"frozen": False}  # allow mutation

# --- Sample flights ---
flights: List[FlightPricing] = [
    FlightPricing(id=1, airline="IndiGo", base_fare=3000, total_seats=100, seats_available=40, departure_time="2025-10-20"),
    FlightPricing(id=2, airline="Air India", base_fare=4500, total_seats=120, seats_available=40, departure_time="2025-10-22"),
    FlightPricing(id=3, airline="SpiceJet", base_fare=2700, total_seats=90, seats_available=40, departure_time="2025-10-25"),
]

# --- Background simulation ---
async def simulate_demand(flights: List[FlightPricing]):
    while True:
        for flight in flights:
            # Simulate random bookings
            if flight.seats_available > 0:
                booked = random.randint(0, 2)
                flight.seats_available -= booked
                if flight.seats_available < 0:
                    flight.seats_available = 0

            # Update dynamic price using imported function
            flight.dynamic_price = dynamic_price(
                base_fare=flight.base_fare,
                total_seats=flight.total_seats,
                seats_available=flight.seats_available,
                departure_time=flight.departure_time,
                tier=flight.tier
            )

            # Append to price history
            flight.price_history.append(flight.dynamic_price)

        await asyncio.sleep(5)

# --- FastAPI with lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(simulate_demand(-flights))
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            # This is normal, so just ignore
            pass
app = FastAPI(title="Flight Simulator with Dynamic Pricing & Fare History", lifespan=lifespan)

# --- Endpoints ---
@app.get("/flights", response_model=List[FlightPricing])
def get_flights():
    return flights

@app.get("/flights/{flight_id}/history")
def get_fare_history(flight_id: int):
    flight = next((f for f in flights if f.id == flight_id), None)
    if not flight:
        return {"error": "Flight not found"}
    return {
        "flight_id": flight.id,
        "airline": flight.airline,
        "price_history": flight.price_history
    }
