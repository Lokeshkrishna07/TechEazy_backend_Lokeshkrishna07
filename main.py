from fastapi import FastAPI, Depends, HTTPException
from models import ParcelCreate, Parcel
from service import create_parcel, get_all_parcels, get_parcel_by_tracking_id
from database import create_db_and_tables, get_session
from sqlmodel import Session
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

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
