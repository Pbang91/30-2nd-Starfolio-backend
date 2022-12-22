from drf_yasg import openapi

class PlanetSwaager:
    check_in  = openapi.Parameter('check-in', openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING)
    check_out = openapi.Parameter('check-out', openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING)
    sort      = openapi.Parameter('sort', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)
    offset    = openapi.Parameter('offset', openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER)
    limit     = openapi.Parameter('limit', openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER)
    planet_id = openapi.Parameter('planet_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    accomodation_id = openapi.Parameter('accomodation_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)