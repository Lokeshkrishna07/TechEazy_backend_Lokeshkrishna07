from sqlmodel import SQLModel, Field
from typing import Optional

class Parcel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tracking_id: str
    sender: str
    recipient: str
    status: str

# For creation input
class ParcelCreate(SQLModel):
    tracking_id: str
    sender: str
    recipient: str
    status: str
