from sqlmodel import Session, select
from models import Parcel, ParcelCreate, DeliveryOrder, Vendor
from datetime import date


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


# VENDOR SERVICE
def get_or_create_vendor(session: Session, name: str, subscription_type: str):
    vendor = session.exec(select(Vendor).where(Vendor.name == name)).first()
    if not vendor:
        vendor = Vendor(name=name, subscription_type=subscription_type)
        session.add(vendor)
        session.commit()
        session.refresh(vendor)
    return vendor

# DELIVERY ORDER SERVICE
def create_delivery_order(session: Session, vendor_id: int, order_date: date) -> DeliveryOrder:
    order = DeliveryOrder(order_date=order_date, vendor_id=vendor_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_delivery_orders_by_filters(session: Session, vendor_id=None, target_date=None):
    query = select(DeliveryOrder)
    if vendor_id:
        query = query.where(DeliveryOrder.vendor_id == vendor_id)
    if target_date:
        query = query.where(DeliveryOrder.order_date == target_date)
    return session.exec(query).all()
