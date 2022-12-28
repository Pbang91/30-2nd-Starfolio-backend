from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from users.utils import login_decorator
from wishlists.models import WishList

from .swagger import WishListSwaager
from .serializers import WishListSerializer, WishListDetailSerializer, WishSerializer

class WishListView(APIView):
    @swagger_auto_schema(request_body=WishSerializer, responses={201 : WishListSerializer, 400 : "Invalid Reason Message"}, tags=["WishList"])
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
    
    @swagger_auto_schema(manual_parameters=[WishListSwaager.limit, WishListSwaager.offset],
                         responses={201 : WishListSerializer, 400 : "Invalid Reason Message"}, tags=["WishList"])
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