
import random

drink_prices = {
    "Juicy IPA": 6.00,
    "Amber Ale": 5.00,
    "Stout": 5.50,
    "Sour": 6.50,
    "Pilsner": 4.50,
}

def update_prices():
    for drink in drink_prices:
        change = random.uniform(-0.5, 0.5)
        drink_prices[drink] = max(3.0, round(drink_prices[drink] + change, 2))
    return drink_prices
