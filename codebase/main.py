from codebase import schema
from codebase.config import default_timezone, date_time_format, lower_bound, upper_bound
from codebase.data import fitness_activities, clients, bookings, sample_tz
from codebase.utils import check_for_slots

from fastapi import FastAPI, Query, HTTPException, status
from pydantic import EmailStr
from typing import List, Optional
from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
import random



app = FastAPI()
ALL_TIMEZONES = available_timezones()


@app.get("/timezones/sample/", tags=['Testing'])
def get_sample_timezones():
    """Returns a demo list of timezones for testing or dropdown population."""
    return {"test_values" :sorted(sample_tz)}

@app.get("/memory", tags=['Testing'])
def get_memory():

    """Returns all data in memory."""

    return {"bookings": bookings, "clients": clients, "classes": fitness_activities}



@app.get("/classes", response_model=schema.FitnessClassResponse, tags=['Fitness Studio - Sweat Syndicate'])
def get_classes(user_timezone: Optional[str] | None = Query(example="Australia/Sydney")):
    """Returns a list of all upcoming fitness classes (name, date/time, instructor, available slots)
    
    Query Parameters:
    - user_timezone (optional): IANA timezone string (e.g., 'Australia/Sydney').
      Defaults to 'Asia/Kolkata' if not provided.
    """

    filtered_list = []
    if not user_timezone:
        user_timezone = default_timezone

    if user_timezone not in ALL_TIMEZONES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect or Unknown timezone.",
        )

    now = datetime.now(ZoneInfo(user_timezone))
    print(f"Now as per {user_timezone} is - ", now)

    for cls in fitness_activities:
        class_dt = datetime.strptime(cls["datetime"], date_time_format)
        class_dt = class_dt.replace(tzinfo=ZoneInfo(user_timezone))
        print("Timezone-aware datetime is -", class_dt)

        if class_dt > now:
            filtered_list.append(cls)
    print("Classes scheduled are -", filtered_list)
    if not filtered_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No class scheduled yet."
        )

    return {"classes" : filtered_list}


@app.post("/book", tags=['Fitness Studio - Sweat Syndicate'])
def create_booking(booking: schema.BookingDetails):

    """Accepts a booking request (class_id,client_name,client_email,client_timezone,slots_reqd)

    Validates if slots are available, and 
    reduces available slots upon successful booking
    """

    class_id = booking.class_id
    name = booking.client_name
    email = booking.client_email
    timezone = booking.client_timezone

    booking = booking.dict()

    #Check if client is new or pre-existing. If new, add them in the list else don't.
    if not any(client["name"] == name and client["email"] == email for client in clients):
        clients.append(
            {"client_id": random.randint(lower_bound,upper_bound), "name": name, "email": email, "timezone": timezone}
        )

    #Get the class data as given in booking.
    class_data = [cls for cls in fitness_activities if cls.get("id") == class_id]

    if not class_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No class with id {class_id} found.")
    else:
        print("Before fn call")
        booking_completed = check_for_slots(class_data[0], booking)


    return {"message":"Booked Successfully!","details": booking_completed}


@app.get("/booking", response_model=schema.BookingResponse, tags=['Fitness Studio - Sweat Syndicate'])
def get_booking(email : EmailStr):

    """Returns all bookings made by a specific email address.
    
     Query Parameters:
      - email - user_email to check for bookings."""

    all_user_bookings = []
    all_user_bookings = [booking for booking in bookings if booking['booked_email'] == email]
    print('All Bookings -',all_user_bookings)

    if not all_user_bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No bookings found with email - {email}")
    
    return {"details": all_user_bookings}



