# delivery/services.py
from ..utils import calculate_delivery_price

def estimate_price(request: 'schemas.EstimatePriceRequest') -> float:
    return calculate_delivery_price(
        pickup_lat=request.pickup_lat,
        pickup_lon=request.pickup_lon,
        dropoff_lat=request.dropoff_lat,
        dropoff_lon=request.dropoff_lon,
        weight=request.weight,
        send_code=request.send_code
    )