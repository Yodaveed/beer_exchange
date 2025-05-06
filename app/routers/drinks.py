from fastapi import APIRouter
from datetime import datetime
from app.price_engine import update_price
from app.models import User, Order

router = APIRouter()

# Simulate one drink
mock_drinks = [
    {
        "id": 1,
        "name": "Juicy IPA",
        "base_price": 6.00,
        "current_price": 6.00,
        "min_price": 4.00,
        "max_price": 9.00,
        "total_orders": 10,
        "last_ordered_at": datetime.utcnow()
    }
]

@router.get("/update-prices")
def update_all_prices():
    for drink in mock_drinks:
        update_price(drink)
        # Simulate a user
mock_user = User(id=1, name="Test User", points=0)

# Track orders in memory
order_log = []
futures_log = []


@router.post("/order-drink")
def order_drink(drink_id: int):
    # Find the drink
    drink = next((d for d in mock_drinks if d["id"] == drink_id), None)
    if not drink:
        return {"error": "Drink not found"}

    # Simulate an order
    order = Order(
        user_id=mock_user.id,
        drink_id=drink_id,
        price_at_purchase=drink["current_price"],
        points_earned=int(drink["current_price"])  # 1 point per $1
    )

    # Update drink stats
    drink["total_orders"] += 1
    drink["last_ordered_at"] = datetime.utcnow()

    # Update user points
    mock_user.points += order.points_earned

    # Log the order
    order_log.append(order)

    return {
        "message": f"{drink['name']} ordered",
        "price": order.price_at_purchase,
        "points_earned": order.points_earned,
        "user_total_points": mock_user.points
    }

    return {"drinks": mock_drinks}
@router.get("/user-points")
def get_user_points():
    return {
        "user_id": mock_user.id,
        "points": mock_user.points
    }
@router.post("/lock-in-price")
def lock_in_price(drink_id: int):
    # Find the drink
    drink = next((d for d in mock_drinks if d["id"] == drink_id), None)
    if not drink:
        return {"error": "Drink not found"}

    # Check user points
    lock_cost = 5
    if mock_user.points < lock_cost:
        return {"error": "Not enough points to lock in price."}

    # Deduct points
    mock_user.points -= lock_cost

    # Create a locked price
    lock = {
        "user_id": mock_user.id,
        "drink_id": drink_id,
        "locked_price": drink["current_price"],
        "locked_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(hours=1),
        "used": False
    }

    futures_log.append(lock)

    return {
        "message": f"{drink['name']} locked at ${drink['current_price']:.2f} for 1 hour",
        "remaining_points": mock_user.points
    }
