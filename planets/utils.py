from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

def check_valid_date(check_in, check_out, serializer_data):
    if check_in and check_out:    
        check_in              = datetime.strptime(check_in,"%Y-%m-%d")
        check_out             = datetime.strptime(check_out, "%Y-%m-%d")
        stays                 = (check_out - check_in).days
        hope_date             = [datetime.strftime(check_in+timedelta(days=stay), "%Y-%m-%d") for stay in range(stays)]    
        date_invalidity_check = [date for date in hope_date if date in serializer_data.get('invalid_dates')]
        
        if date_invalidity_check:
            raise ValidationError("Invalid Date")

        serializer_data['stays'] = stays
        serializer_data['price'] = float(serializer_data.get("price")) * stays

    elif not check_in or check_out:
        serializer_data['stays'] = None
        serializer_data['price'] = None
        
    return serializer_data