from drf_yasg import openapi

class WishListSwaager:
    offset = openapi.Parameter('offset', openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER)
    limit  = openapi.Parameter('limit', openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER)