from pydantic import BaseModel, EmailStr
from typing import List

class FitnessClass(BaseModel):
    id              : int
    name            : str
    datetime        : str
    instructor      : str
    available_slots : int

class FitnessClassResponse(BaseModel):
    classes: List[FitnessClass]    


class BookingDetails(BaseModel):
    class_id        : int
    client_name     : str
    client_email    : EmailStr
    client_timezone : str
    slots_reqd      : int

class BookedDetails(BaseModel):
    booking_id : int
    booked_name : str
    booked_email : EmailStr
    slots_booked : int
    booked_class : int
    class_time : str
    class_name : str

    
class BookingResponse(BaseModel):
    details: List[BookedDetails]   