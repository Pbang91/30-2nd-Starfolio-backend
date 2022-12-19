from datetime import datetime, timedelta

from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from planets.models import Planet, Accomodation

from .utils import check_valid_date
from .serializer import PlanetSerializer, PlanetDetailSerializer

class PlanetsView(APIView):
    def get(self, request):
        check_in  = request.GET.get('check-in')
        check_out = request.GET.get('check-out')
        sort      = request.GET.get('sort', 'id')
        limit     = int(request.GET.get('limit', 10))
        offset    = int(request.GET.get('offset', 0))

        filter_options = {
            'galaxy'    : 'galaxy_id',
            'theme'     : 'theme_id',
            'searching' : 'name__icontains',
            'people'    : 'accomodation__max_of_people__gte',
            'min-price' : 'accomodation__price__gte',
            'max-price' : 'accomodation__price__lte'
        }

        filter_set = {filter_options.get(key) : value for key, value in request.GET.items() if filter_options.get(key)}

        booking = Q()

        if check_in and check_out:
            if check_in >= check_out:
                return JsonResponse({'message':'Invalid Date'}, status=status.HTTP_400_BAD_REQUEST)

            check_in  = datetime.strptime(check_in, '%Y-%m-%d')
            check_out = datetime.strptime(check_out, '%Y-%m-%d')

            booking |= Q(booking__start_date__range=(check_in, check_out-timedelta(days=1)))
            booking |= Q(booking__end_date__range=(check_in+timedelta(days=1), check_out))

        sort_type = {
            'id'   : 'id',
            'new'  : '-created_at',
            'desc' : '-accomodation__price',
            'asc'  : 'accomodation__price' 
        }

        planets = Planet.objects.prefetch_related('accomodation_set')\
                                .prefetch_related('booking_set')\
                                .filter(**filter_set)\
                                .exclude(booking)\
                                .order_by(sort_type[sort])[offset:offset+limit]

        serializer = PlanetSerializer(planets, many=True)


        return Response(data=serializer.data, status=status.HTTP_200_OK)

class PlanetDetailView(APIView):
    def get(self, request, planet_id, accomodation_id):
        try:
            check_in  = request.GET.get('check-in')
            check_out = request.GET.get('check-out')

            accomodation = Accomodation.objects.prefetch_related('accomodationimage_set').select_related('planet').get(id=accomodation_id, planet_id=planet_id)

            serializer = PlanetDetailSerializer(accomodation)

            new_serializer_data = check_valid_date(check_in, check_out, serializer.data)

            return Response(data=new_serializer_data, status=status.HTTP_200_OK)

        except Accomodation.DoesNotExist:
            return JsonResponse({'message' : 'Invalid Accomodation'}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status=status.HTTP_400_BAD_REQUEST)