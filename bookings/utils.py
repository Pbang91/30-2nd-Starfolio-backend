from decimal import Decimal

from django.core.exceptions import ValidationError

from planets.models import Accomodation

def check_validation_request(request_data):
    SURCHARGE_RATE = 0.1

    accomodation = Accomodation.objects.get(id=request_data['accomodation_id'])
    
    number_of_adults   = request_data.get('number_of_adults', 1)
    number_of_children = request_data.get('number_of_children', 0)
    num_of_people      = number_of_adults+number_of_children
    
    total_price      = Decimal(request_data.get('total_price', 0))
    additional_price = accomodation.price*Decimal(SURCHARGE_RATE)

    if num_of_people > accomodation.max_of_people:
        raise ValidationError('Invalid Num Of People')

    if num_of_people > accomodation.min_of_people:
        total_price += (num_of_people-accomodation.min_of_people)*additional_price
    
    request_data['number_of_adults'] = number_of_adults
    request_data['number_of_children'] = number_of_children
    request_data['total_price'] = total_price

    return request_data