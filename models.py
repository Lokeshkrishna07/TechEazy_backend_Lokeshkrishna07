from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from typing import Optional, List
from enum import Enum
from datetime import date

class SubscriptionType(str, Enum):
    NORMAL = "NORMAL"
    PRIME = "PRIME"
    VIP = "VIP"

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    subscription_type: SubscriptionType
    orders: List["DeliveryOrder"] = Relationship(back_populates="vendor")

class DeliveryOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: date
    vendor_id: int = Field(foreign_key="vendor.id")
    vendor: Optional[Vendor] = Relationship(back_populates="orders")
    parcels: List["Parcel"] = Relationship(back_populates="delivery_order")


class Parcel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tracking_id: str
    sender: str
    recipient: str
    status: str
    delivery_order_id: Optional[int] = Field(default=None, foreign_key="deliveryorder.id")
    delivery_order: Optional[DeliveryOrder] = Relationship(back_populates="parcels")

# For creation input
class ParcelCreate(SQLModel):
    tracking_id: str
    sender: str
    recipient: str
    status: str

#DTO
class DeliveryOrderDTO(SQLModel):
    order_date: date
    vendor_name: str
    total_orders: int
    file_link: Optional[str]
