
drink_prices = {
    "Juicy IPA": 6.00,
    "Amber Ale": 5.00,
    "Stout": 5.50,
    "Sour": 6.50,
    "Pilsner": 4.50,
}

user_points = {}
from datetime import datetime, timedelta

locked_futures = []  # each entry: dict with user_id, drink, price, expires_at

def lock_price(user_id, drink, price):
    expires_at = datetime.utcnow() + timedelta(hours=1)
    locked_futures.append({
        "user_id": user_id,
        "drink": drink,
        "locked_price": price,
        "expires_at": expires_at
    })
