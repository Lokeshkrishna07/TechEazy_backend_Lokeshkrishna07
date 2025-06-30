from sqlmodel import Session, select
from models import Parcel, ParcelCreate

def create_parcel(session: Session, parcel_data: ParcelCreate) -> Parcel:
    parcel = Parcel(**parcel_data.dict())
    session.add(parcel)
    session.commit()
    session.refresh(parcel)
    return parcel

def get_all_parcels(session: Session):
    return session.exec(select(Parcel)).all()

def get_parcel_by_tracking_id(session: Session, tracking_id: str):
    return session.exec(select(Parcel).where(Parcel.tracking_id == tracking_id)).first()
