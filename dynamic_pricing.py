from datetime import datetime
import math

def dynamic_price(base_fare: float, total_seats: int, seats_available: int, departure_time: str, tier: str = "standard") -> float:
    """
    Calculate dynamic flight price based on seat availability, time to departure, and tier.
    """

    # --- 1. Seats factor: fewer seats -> higher price ---
    seat_ratio = seats_available / total_seats
    seat_factor = 1 + (1 - seat_ratio) * 0.5  # up to +50% increase as seats sell out

    # --- 2. Time factor: closer departure -> higher price ---
    now = datetime.now()
    try:
        dep_time = datetime.strptime(departure_time, "%Y-%m-%d")
    except ValueError:
        dep_time = now  # fallback to avoid crash

    days_left = (dep_time - now).days
    if days_left < 0:
        days_left = 0

    # exponential increase if departure is near
    time_factor = 1 + math.exp(-0.1 * days_left) * 0.3  # up to +30%

    # --- 3. Tier-based multiplier ---
    tier_multipliers = {
        "standard": 1.0,
        "flex": 1.15,
        "business": 1.35,
        "premium": 1.5
    }
    tier_factor = tier_multipliers.get(tier.lower(), 1.0)

    # --- 4. Combine all factors ---
    dynamic_fare = base_fare * seat_factor * time_factor * tier_factor

    # --- 5. Round and return ---
    return round(dynamic_fare, 2)
