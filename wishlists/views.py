
from pprint import pprint

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http  import JsonResponse

from users.utils      import login_decorator
from planets.models   import Planet
from wishlists.models import WishList

from .serializers import WishListSerializer, WishListDetailSerializer

class WishListView(APIView):
    @login_decorator
    def post(self, request):
        try:
            user = request.user
            data = {
                'user'   : user.id,
                'planet' : request.data['planet_id']
            }

            serializer = WishListSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()

                return Response(data=serializer.data, status=status.HTTP_201_CREATED, content_type="application/json")
            
            else:
                return JsonResponse({'message':'Inavlid Planet'}, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError:
            return JsonResponse({'message':'Inavlid Required Value'}, status=status.HTTP_400_BAD_REQUEST)
    
    @login_decorator
    def get(self, request):
        limit  = int(request.GET.get('limit', 3))
        offset = int(request.GET.get('offset', 0))
        user   = request.user

        wishlists = WishList.objects.filter(user=user).select_related('planet')[offset:offset+limit]

        if not wishlists:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = WishListDetailSerializer(wishlists, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)