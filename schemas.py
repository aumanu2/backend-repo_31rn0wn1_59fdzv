"""
Database Schemas for Umrah/Hajj Super App

Each Pydantic model represents a MongoDB collection. The collection name is the lowercase
of the class name (e.g., Booking -> "booking").
"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# Core user and profiles
class User(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    country: Optional[str] = None
    is_active: bool = True

class Traveler(BaseModel):
    user_id: Optional[str] = Field(None, description="Reference to User")
    full_name: str
    passport_no: Optional[str] = None
    nationality: Optional[str] = None

# Catalog: packages, accommodations, transport, guides, ziyarat points
class Package(BaseModel):
    title: str
    description: Optional[str] = None
    city: Literal["Makkah", "Madinah", "Jeddah", "Taif"]
    nights: int
    price: float
    rating: Optional[float] = None
    images: List[str] = []
    includes_flights: bool = False

class Accommodation(BaseModel):
    name: str
    city: Literal["Makkah", "Madinah", "Jeddah", "Taif"]
    distance_to_haram_m: Optional[int] = None
    price_per_night: float
    rating: Optional[float] = None
    amenities: List[str] = []
    images: List[str] = []

class Transport(BaseModel):
    provider: str
    type: Literal["taxi", "car", "bus", "van", "private"]
    route: str  # e.g., "Jeddah → Makkah"
    price: float
    seats: Optional[int] = None
    licensed_for_hajj: bool = True

class Guide(BaseModel):
    name: str
    languages: List[str] = []
    city: Literal["Makkah", "Madinah", "Jeddah", "Taif"]
    rating: Optional[float] = None
    verified: bool = True
    services: List[str] = []

class Ziyarat(BaseModel):
    name: str
    city: Literal["Makkah", "Madinah", "Jeddah", "Taif"]
    lat: float
    lng: float
    description: Optional[str] = None
    image: Optional[str] = None

# Bookings and reviews
class Booking(BaseModel):
    user_id: str
    booking_type: Literal["flight", "accommodation", "transport", "package", "guide"]
    item_id: Optional[str] = None
    details: dict = {}
    total_amount: float
    currency: Literal["SAR", "USD", "PKR", "AED"] = "SAR"
    status: Literal["pending", "confirmed", "cancelled"] = "pending"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Review(BaseModel):
    user_id: str
    item_type: Literal["accommodation", "transport", "package", "guide"]
    item_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class Notification(BaseModel):
    user_id: str
    title: str
    message: str
    read: bool = False
    send_at: Optional[datetime] = None

# Worship tracker
class Worship(BaseModel):
    user_id: str
    type: Literal["prayer", "quran", "dua"]
    value: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Group travel
class Group(BaseModel):
    leader_user_id: str
    name: str
    member_user_ids: List[str] = []
    shared_payment: bool = False

class Message(BaseModel):
    group_id: str
    sender_user_id: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
