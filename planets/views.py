from django.core.exceptions import ValidationError
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from datetime               import datetime, timedelta

from planets.models         import Planet, Accomodation, AccomodationImage
from .utils                 import check_valid_date

class PlanetListView(View):
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

        filter_set = {
            filter_options.get(key): value\
                for (key, value) in request.GET.items()\
                     if filter_options.get(key)
        }

        booking = Q()

        if check_in and check_out:

            if check_in >= check_out:
                return JsonResponse({'message':'INVALID_DATE'}, status=400)

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

        planets_list = [{
            'id'                : planet.id,
            'name'              : planet.name,
            'thumbnail'         : planet.thumbnail,
            'galaxy'            : planet.galaxy.name,
            'theme'             : planet.theme.name,
            'image'             : [image.image_url for image in planet.planetimage_set.all()],
            'accomodation_info' : [{
                'min_of_people' : accomodation.min_of_people,
                'max_of_people' : accomodation.max_of_people,
                'price'         : accomodation.price
            } for accomodation in planet.accomodation_set.all()]
        } for planet in planets]

        return JsonResponse({'planets_list':planets_list}, status=200)

class PlanetDetailView(View):
    def get(self, request, planet_id, accomodation_id):
        try:
            check_in  = request.GET.get('check-in')
            check_out = request.GET.get('check-out')

            chosen_accomodation        = Accomodation.objects.get(id = accomodation_id, planet_id = planet_id)
            chosen_accomodation_images = AccomodationImage.objects.select_related('accomodation__planet').filter(accomodation = chosen_accomodation)

            accomodation_information = {
                'id'            : chosen_accomodation.id,
                'name'          : chosen_accomodation.name,
                'stays'         : None,
                'price'         : None,
                'images'        : [accomodation_image.image_url for accomodation_image in chosen_accomodation_images],
                'description'   : chosen_accomodation.description,
                'min_of_people' : chosen_accomodation.min_of_people,
                'max_of_people' : chosen_accomodation.max_of_people,
                'num_of_bed'    : chosen_accomodation.num_of_bed,
                'invalid_dates' : None
            }

            accomodation_information = check_valid_date(accomodation_information, check_in, check_out, chosen_accomodation)

            return JsonResponse({'result' : accomodation_information}, status = 200)

        except Accomodation.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_ACCOMODATION'}, status = 400)
        
        except ValidationError as error:
            return JsonResponse({'message' : error.message}, status = 400)