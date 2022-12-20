import uuid
from enum import Enum
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ValidationError

from users.utils import login_decorator
from planets.models import Accomodation
from bookings.models import Booking

from .utils import check_validation_request
from .serializer import BookingSerializer

class BookingStatusEnum(Enum):
    PENDING   = 1
    PAID      = 2
    RESERVED  = 3
    CANCELLED = 4

class BookingView(APIView):
    @login_decorator
    def get(self, request):
        try:
            my_stay = request.GET.get('my-stay')

            if not my_stay:
                raise ValidationError('Invalid Filter')

            limit  = int(request.GET.get('limit', 3))
            offset = int(request.GET.get('offset', 0))
            today  = datetime.today().strftime("%Y-%m-%d")
            user   = request.user

            q = Q(user=user)

            filtering_set = {
                'booking-info' : Q(start_date__gte=today),
                'history'      : Q(start_date__lt=today)
            }

            q &= filtering_set[my_stay]

            bookings = Booking.objects.filter(q)[offset:offset+limit]

            serializer = BookingSerializer(bookings, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status=status.HTTP_400_BAD_REQUEST)
    
    @login_decorator
    def post(self, request):
        try:
            data = request.data
            user = request.user
            
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date   = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            
            data = check_validation_request(request_data=data)

            q = Q()

            q &= Q(user_id=user.id)
            q &= Q(start_date__range=(start_date, end_date-timedelta(days=1)))\
                 | Q(end_date__range=(start_date+timedelta(days=1), end_date))

            if Booking.objects.filter(q):
                return JsonResponse({'message':'Already Booked Accomodation'}, status=status.HTTP_400_BAD_REQUEST)

            save_data = {
                'booking_number' : str(uuid.uuid4()),
                'start_date' : start_date,
                'end_date' : end_date,
                'number_of_adults' : data["number_of_adults"],
                'number_of_children' : data["number_of_children"],
                'user_request' : data.get('user_request', None),
                'price' : data['total_price'],
                'user_id' : user.id,
                'booking_status_id' : BookingStatusEnum.PENDING.value,
                'planet_id' : data['planet_id'],
                'accomodation_id' : data['accomodation_id']
            }
            
            serializer = BookingSerializer(data=save_data)

            if serializer.is_valid():
                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            
            elif not serializer.is_valid():
                raise ValidationError(serializer.errors)
        
        except Accomodation.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Accomodation'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return JsonResponse({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return JsonResponse({'message':'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

    @login_decorator
    #TODO 추후 관리자페이지에서 status 업데이트 진행
    def patch(self, request, booking_id):
        try:
            data = request.data
            user = request.user
            
            booking_status : str = data.get('status')
            
            if booking_status:
                convert_status : int = BookingStatusEnum[booking_status.upper()].value
                data['booking_status'] = convert_status

            booking = Booking.objects.get(user=user, id=booking_id)
            
            data['accomodation_id']    = booking.accomodation.id
            data['number-of-adults']   = data.get('number-of-adults', booking.number_of_adults)
            data['number-of-children'] = data.get('number-of-children', booking.number_of_children)

            data = check_validation_request(request_data=data)

            serializer = BookingSerializer(booking, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                
                return Response(data=serializer.data, status=status.HTTP_200_OK)

        except (Booking.DoesNotExist, Accomodation.DoesNotExist):
            return JsonResponse({'message':'Invalid Booking Information'}, status=status.HTTP_404_NOT_FOUND)

        except KeyError:
            return JsonResponse({'message':'Invalid Request Value'}, status=400)

    @login_decorator
    def delete(self, request):
        user        = request.user
        booking_ids = request.GET.getlist('booking-ids')
        bookings    = Booking.objects.filter(user=user, id__in=booking_ids)
            
        if not bookings:
            return JsonResponse({'message':'Invalid Booking Information'}, status=status.HTTP_400_BAD_REQUEST)

        bookings.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
        
