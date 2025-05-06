from datetime import datetime, timedelta

def update_price(drink):
    now = datetime.utcnow()

    # Drop price if no one has ordered in 30 min
    if drink["last_ordered_at"] and (now - drink["last_ordered_at"]) > timedelta(minutes=30):
        drink["current_price"] = max(drink["current_price"] - 0.25, drink["min_price"])

    # Raise price every 5 orders
    elif drink["total_orders"] % 5 == 0:
        drink["current_price"] = min(drink["current_price"] + 0.25, drink["max_price"])

    return drink
