from codebase.data import fitness_activities,bookings,clients
from codebase.config import lower_bound,upper_bound

from fastapi import HTTPException,status
import random


def reduce_slots(class_data,booking):

    """Reduces available slots within a given class, 
    using data received after booking
    """

    slots_booked = booking["slots_booked"]
    for index, cls in enumerate(fitness_activities):
        if cls["id"] == class_data["id"]:
            updated_data = cls.copy()
            updated_data["available_slots"] -= slots_booked

            fitness_activities.pop(index)
            fitness_activities.insert(index, updated_data)
            print("fitness_activities updated")

    print("Updated fitness_activities is - ", fitness_activities)
    return fitness_activities



def validate_booking(class_data, booking_data):

    """Checks if booking is present with client_email. 
        If yes, throws error
        Else returns new_booking created
    """
    
    client_email = booking_data['client_email']
    booking_present = [booking for booking in bookings if booking.get('booked_email') == client_email]
   
    if booking_present:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST
                            ,detail=f"Booking already present with email {client_email}.")
    else:
        new_booking = {"booked_name": booking_data['client_name'],
                       "booked_email": booking_data['client_email'],
                       "slots_booked": booking_data['slots_reqd'],
                       "booked_class" : class_data['id'],
                       "booking_id" : random.randint(lower_bound,upper_bound)}
        bookings.append(new_booking)
        print('Bookings list updated. Current values are -', bookings)
        reduce_slots(class_data,new_booking)

    return new_booking


def check_for_slots(class_data, booking_data):

    """ Fn checks if requested slots are available for that class.
        If yes, proceeds with booking validation.
        Else throws error.
    """
    booking_details = []
    available_slots = class_data["available_slots"]
    print("Booking data is", booking_data)

    if class_data["available_slots"] == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No slots available for the selected class.",
        )

    elif booking_data["slots_reqd"] > class_data["available_slots"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {available_slots} slot available",
        )

    else:
         booking_details = validate_booking(class_data,booking_data)


    return booking_details
