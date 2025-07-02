from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from database import get_session, create_db_and_tables
from service import *
from models import *
from auth import create_access_token, get_current_user
from typing import List
from datetime import date

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# JWT LOGIN
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "admin":
        token = create_access_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Invalid login")

# Create parcel in memory
@app.post("/parcels", response_model=Parcel)
def create_parcel_api(parcel: ParcelCreate, session: Session = Depends(get_session)):
    return create_parcel(session, parcel)

@app.get("/parcels", response_model=List[Parcel])
def get_all_api(session: Session = Depends(get_session)):
    return get_all_parcels(session)

@app.get("/parcels/{tracking_id}", response_model=Parcel)
def get_by_tracking_id(tracking_id: str, session: Session = Depends(get_session)):
    parcel = get_parcel_by_tracking_id(session, tracking_id)
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return parcel

from datetime import datetime

@app.post("/upload-order")
def upload_order_file(
    vendor_name: str = Form(...),
    subscription_type: SubscriptionType = Form(...),
    order_date: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: str = Depends(get_current_user)
):
    # ✅ Convert order_date string (e.g. '2025-07-02') to date object
    parsed_order_date = datetime.strptime(order_date, "%Y-%m-%d").date()

    vendor = get_or_create_vendor(session, vendor_name, subscription_type)
    order = create_delivery_order(session, vendor.id, parsed_order_date)

    lines = file.file.read().decode("utf-8").splitlines()
    for line in lines:
        trk, snd, rec, st = line.strip().split(",")
        parcel = Parcel(
            tracking_id=trk,
            sender=snd,
            recipient=rec,
            status=st,
            delivery_order_id=order.id
        )
        session.add(parcel)
    session.commit()
    return {"msg": "Order uploaded", "order_id": order.id}


# Get Delivery Orders for Today
@app.get("/delivery-orders", response_model=List[DeliveryOrderDTO])
def get_orders(
    vendor_id: Optional[int] = None,
    target_date: Optional[date] = date.today(),
    session: Session = Depends(get_session),
    user: str = Depends(get_current_user)
):
    orders = get_delivery_orders_by_filters(session, vendor_id, target_date)
    return [
        DeliveryOrderDTO(
            order_date=order.order_date,
            vendor_name=order.vendor.name,
            total_orders=len(order.parcels),
            file_link=None  # Optional for download
        )
        for order in orders
    ]