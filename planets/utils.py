from django.core.exceptions import ValidationError

from datetime               import datetime, timedelta

from bookings.models        import Booking

def check_valid_date(accomodation_information, check_in, check_out, chosen_accomodation):
    unavailable_bookings = Booking.objects.filter(accomodation    = chosen_accomodation,
                                                  start_date__lte = datetime.today() + timedelta(days=186),
                                                  end_date__gte   = datetime.today()
                                                )

    invalid_dates = []

    for unavailable_booking in unavailable_bookings:
        booked_out_stays = (unavailable_booking.end_date - unavailable_booking.start_date).days
        invalid_dates   += [datetime.strftime(unavailable_booking.start_date+timedelta(days=booked_out_stay), "%Y-%m-%d") for booked_out_stay in range(booked_out_stays)]
    
    accomodation_information['invalid_dates'] = invalid_dates

    if check_in and check_out:    
        check_in              = datetime.strptime(check_in,"%Y-%m-%d")
        check_out             = datetime.strptime(check_out, "%Y-%m-%d")
        stays                 = (check_out - check_in).days
        hope_date             = [datetime.strftime(check_in+timedelta(days=stay), "%Y-%m-%d") for stay in range(stays)]    
        date_invalidity_check = [date for date in hope_date if date in invalid_dates]
        
        if date_invalidity_check:
            raise ValidationError("INVALID_DATE")

        accomodation_information['stays'] = stays
        accomodation_information['price'] = chosen_accomodation.price * stays
        
    return accomodation_information