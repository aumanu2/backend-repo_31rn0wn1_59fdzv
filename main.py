import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import (
    User, Traveler, Package, Accommodation, Transport, Guide,
    Ziyarat, Booking, Review, Notification, Worship, Group, Message
)

app = FastAPI(title="Umrah/Hajj Super App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Umrah/Hajj Super App Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Helper to convert ObjectId to str in results

def serialize_doc(doc: dict):
    if not doc:
        return doc
    doc = dict(doc)
    if doc.get("_id"):
        doc["id"] = str(doc.pop("_id"))
    return doc

# Public catalog endpoints (read-only lists)

@app.get("/catalog/featured")
def get_featured():
    data = {
        "packages": [serialize_doc(d) for d in get_documents("package", limit=6)],
        "accommodations": [serialize_doc(d) for d in get_documents("accommodation", limit=6)],
        "transports": [serialize_doc(d) for d in get_documents("transport", limit=6)],
        "ziyarat": [serialize_doc(d) for d in get_documents("ziyarat", limit=8)],
    }
    return data

# Minimal create endpoints to seed data quickly

@app.post("/admin/seed/package")
def seed_package(pkg: Package):
    inserted_id = create_document("package", pkg)
    return {"id": inserted_id}

@app.post("/admin/seed/accommodation")
def seed_accommodation(acc: Accommodation):
    inserted_id = create_document("accommodation", acc)
    return {"id": inserted_id}

@app.post("/admin/seed/transport")
def seed_transport(tr: Transport):
    inserted_id = create_document("transport", tr)
    return {"id": inserted_id}

@app.post("/admin/seed/ziyarat")
def seed_ziyarat(z: Ziyarat):
    inserted_id = create_document("ziyarat", z)
    return {"id": inserted_id}

# Booking creation (simplified)

@app.post("/bookings")
def create_booking(b: Booking):
    booking_id = create_document("booking", b)
    return {"id": booking_id, "status": b.status}

@app.get("/bookings", response_model=List[dict])
def list_bookings(limit: int = 20):
    docs = get_documents("booking", limit=limit)
    return [serialize_doc(d) for d in docs]

# Notifications (basic create + list)

@app.post("/notifications")
def create_notification(n: Notification):
    nid = create_document("notification", n)
    return {"id": nid}

@app.get("/notifications")
def list_notifications(user_id: Optional[str] = None, limit: int = 20):
    filter_dict = {"user_id": user_id} if user_id else {}
    docs = get_documents("notification", filter_dict, limit)
    return [serialize_doc(d) for d in docs]

# Simple worship tracker

@app.post("/worship")
def add_worship(w: Worship):
    wid = create_document("worship", w)
    return {"id": wid}

@app.get("/worship")
def list_worship(user_id: str, limit: int = 100):
    docs = get_documents("worship", {"user_id": user_id}, limit)
    return [serialize_doc(d) for d in docs]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
