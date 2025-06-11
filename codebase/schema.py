from pydantic import BaseModel, EmailStr

class FitnessClass(BaseModel):
    id              : int
    name            : str
    datetime        : str
    instructor      : str
    available_slots : int


class BookingDetails(BaseModel):
    class_id        : int
    client_name     : str
    client_email    : EmailStr
    client_timezone : str
    slots_reqd      : int