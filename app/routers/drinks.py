
from fastapi import APIRouter, Query
from app.models import drink_prices, user_points
from app.price_engine import update_prices

router = APIRouter()

@router.get("/update-prices")
def update_drink_prices():
    updated = update_prices()
    return {"updated_prices": updated}

@router.post("/order-drink")
def order_drink(user_id: str = Query(...), drink: str = Query(...)):
    if drink not in drink_prices:
        return {"error": "Drink not found."}
    
    price = drink_prices[drink]
    points = int(price)
    user_points[user_id] = user_points.get(user_id, 0) + points

    return {
        "message": f"{drink} ordered",
        "price": price,
        "points_earned": points,
        "user_total_points": user_points[user_id]
    }
