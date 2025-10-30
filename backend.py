from fastapi import FastAPI, Query, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
import threading
import random
import uuid
import os

# connected frontend to backend


app = FastAPI(title="Flight Booking Simulator with Dynamic Pricing")

# Allow frontend (HTML/JS) to call backend APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend (index.html and other files)
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))


flights: Dict[int, dict] = {}
flight_locks: Dict[int, threading.Lock] = {}
bookings: Dict[str, dict] = {}

# Create Sample Flights 
def create_sample_flights():
    data = [
        {"id": 1, "airline": "IndiGo", "origin": "HYD", "destination": "BLR", "date": "2025-11-05", "base_price": 3000},
        {"id": 2, "airline": "Air India", "origin": "HYD", "destination": "DEL", "date": "2025-11-10", "base_price": 4500},
        {"id": 3, "airline": "SpiceJet", "origin": "BLR", "destination": "MUM", "date": "2025-11-08", "base_price": 3500},
    ]

    for f in data:
        # Create seat map: 4 rows × 4 seats = 16 total
        f["seats"] = {f"{r}{c}": True for r in range(1, 5) for c in ["A", "B", "C", "D"]}
        flights[f["id"]] = f
        flight_locks[f["id"]] = threading.Lock()

create_sample_flights()



def parse_date(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()

def seats_available(flight: dict) -> int:
    return sum(1 for v in flight["seats"].values() if v)

def generate_pnr() -> str:
    return uuid.uuid4().hex[:8].upper()

def dynamic_price(flight: dict) -> float:
    """Dynamic price based on seat availability and days left."""
    base = flight["base_price"]
    rem = seats_available(flight)
    total = len(flight["seats"])
    rem_pct = rem / total

    # Seat factor
    if rem_pct <= 0.2:
        seat_factor = 1.5
    elif rem_pct <= 0.5:
        seat_factor = 1.2
    else:
        seat_factor = 1.0

    # Time factor
    try:
        days_left = (parse_date(flight["date"]) - datetime.now().date()).days
    except Exception:
        days_left = 30
    if days_left <= 3:
        time_factor = 1.6
    elif days_left <= 10:
        time_factor = 1.2
    else:
        time_factor = 1.0

    # Random demand variation
    demand_factor = 1.0 + random.uniform(-0.05, 0.15)

    price = base * seat_factor * time_factor * demand_factor
    return round(price / 10) * 10


class Passenger(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class CreateBooking(BaseModel):
    flight_id: int
    seat: str
    passenger: Passenger
    simulate_payment_fail: Optional[bool] = Field(False, description="Force payment fail for testing")

class BookingOut(BaseModel):
    pnr: str
    flight_id: int
    seat: str
    passenger: Passenger
    price: float
    status: str
    created_at: str

class FlightOut(BaseModel):
    id: int
    airline: str
    origin: str
    destination: str
    date: str
    base_price: float
    available_seats: int
    dynamic_price: float


@app.get("/api")
def root():
    return {"message": "Flight Booking Simulator API is running!"}

# Get all flights with dynamic prices
@app.get("/flights", response_model=List[FlightOut])
def list_flights():
    result = []
    for f in flights.values():
        result.append(
            FlightOut(
                id=f["id"],
                airline=f["airline"],
                origin=f["origin"],
                destination=f["destination"],
                date=f["date"],
                base_price=f["base_price"],
                available_seats=seats_available(f),
                dynamic_price=dynamic_price(f)
            )
        )
    return result

# View seat map for a specific flight
@app.get("/flights/{flight_id}/seats")
def get_seat_map(flight_id: int):
    flight = flights.get(flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return {"seats": flight["seats"]}

# Create booking
@app.post("/bookings", response_model=BookingOut)
def create_booking(req: CreateBooking):
    flight = flights.get(req.flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    with flight_locks[req.flight_id]:
        # Validate seat
        if req.seat not in flight["seats"]:
            raise HTTPException(status_code=400, detail="Invalid seat")
        if not flight["seats"][req.seat]:
            raise HTTPException(status_code=400, detail="Seat already booked")

        price = dynamic_price(flight)
        pnr = generate_pnr()

        # Simulate payment
        payment_success = not req.simulate_payment_fail and random.random() > 0.1
        status = "CONFIRMED" if payment_success else "FAILED"

        if status == "CONFIRMED":
            flight["seats"][req.seat] = False

        booking = {
            "pnr": pnr,
            "flight_id": req.flight_id,
            "seat": req.seat,
            "passenger": req.passenger.model_dump(),
            "price": price,
            "status": status,
            "created_at": datetime.utcnow().isoformat()
        }

        bookings[pnr] = booking
        return booking

# Cancel booking
@app.delete("/bookings/{pnr}")
def cancel_booking(pnr: str):
    booking = bookings.get(pnr)
    if not booking:
        raise HTTPException(status_code=404, detail="PNR not found")
    if booking["status"] != "CONFIRMED":
        raise HTTPException(status_code=400, detail="Cannot cancel non-confirmed booking")

    flight = flights.get(booking["flight_id"])
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    with flight_locks[booking["flight_id"]]:
        flight["seats"][booking["seat"]] = True

    booking["status"] = "CANCELLED"
    return {"message": f"Booking {pnr} cancelled successfully."}

# Retrieve booking history
@app.get("/bookings", response_model=List[BookingOut])
def booking_history():
    return list(bookings.values())
