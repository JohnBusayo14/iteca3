# utils.py
import math

def calculate_delivery_price(pickup_lat: float, pickup_lon: float, dropoff_lat: float, dropoff_lon: float, weight: float, send_code: bool) -> float:
    # Constants
    BASE_FEE = 5.00
    RATE_PER_KM = 0.50
    SEND_CODE_SURCHARGE = 2.00
    MINIMUM_PRICE = 10.00

    # Haversine formula to calculate distance between two points (in kilometers)
    R = 6371.0  # Earth's radius in kilometers
    lat1 = math.radians(pickup_lat)
    lon1 = math.radians(pickup_lon)
    lat2 = math.radians(dropoff_lat)
    lon2 = math.radians(dropoff_lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    # Calculate weight-based rate
    if weight <= 5:
        rate_per_kg = 1.00
    elif weight <= 10:
        rate_per_kg = 1.50
    else:
        rate_per_kg = 2.00

    # Calculate costs
    distance_cost = distance * RATE_PER_KM
    weight_cost = weight * rate_per_kg
    surcharge = SEND_CODE_SURCHARGE if send_code else 0.0

    # Total price
    total_price = BASE_FEE + distance_cost + weight_cost + surcharge

    # Ensure minimum price
    return max(total_price, MINIMUM_PRICE)