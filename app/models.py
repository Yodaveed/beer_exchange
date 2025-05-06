from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User schema
class User(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    points: int = 0
    joined_at: datetime = datetime.utcnow()

# Order schema
class Order(BaseModel):
    user_id: int
    drink_id: int
    price_at_purchase: float
    timestamp: datetime = datetime.utcnow()
    points_earned: int = 0
