from fastapi import APIRouter, Query
from app.models import drink_prices, user_points, locked_futures, lock_price
from app.price_engine import update_prices
from datetime import datetime

router = APIRouter()

@router.get("/update-prices")
def update_drink_prices():
    updated = update_prices()
    return {"updated_prices": updated}

@router.post("/order-drink")
def order_drink(user_id: str = Query(...), drink: str = Query(...)):
    if drink not in drink_prices:
        return {"error": "Drink not found."}

    # Check if user has an active lock-in for this drink
    locked_price = None
    now = datetime.utcnow()

    for lock in locked_futures:
        if lock["user_id"] == user_id and lock["drink"] == drink:
            if lock["expires_at"] > now:
                locked_price = lock["locked_price"]
                break

    price_used = locked_price if locked_price is not None else drink_prices[drink]
    points = int(price_used)
    user_points[user_id] = user_points.get(user_id, 0) + points

    return {
        "message": f"{drink} ordered",
        "price_used": price_used,
        "used_locked_price": locked_price is not None,
        "points_earned": points,
        "user_total_points": user_points[user_id]
    }

@router.post("/lock-in-price")
def lock_in_price(user_id: str = Query(...), drink: str = Query(...)):
    if drink not in drink_prices:
        return {"error": "Drink not found"}

    # Check if user has enough points
    if user_id not in user_points or user_points[user_id] < 5:
        return {"error": "Not enough points to lock in a price"}

    # Deduct points and lock price
    price = drink_prices[drink]
    user_points[user_id] -= 5
    lock_price(user_id, drink, price)

    return {
        "message": f"{drink} locked in at ${price:.2f} for 1 hour",
        "remaining_points": user_points[user_id]
    }
@router.get("/futures")
def get_futures(user_id: str = Query(None)):
    now = datetime.utcnow()
    active_futures = []

    for lock in locked_futures:
        if lock["expires_at"] > now:
            if user_id is None or lock["user_id"] == user_id:
                active_futures.append({
                    "user_id": lock["user_id"],
                    "drink": lock["drink"],
                    "locked_price": lock["locked_price"],
                    "expires_at": lock["expires_at"].isoformat()
                })

    return {"active_futures": active_futures}
