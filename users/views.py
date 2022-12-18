import requests
from datetime import datetime, timedelta

import jwt

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from users.models import User
from starfolio.settings import SECRET_KEY, ALGORITHM

from .utils import login_decorator
from .serializer import KakaoLogInSerializer, RenewalingTokenSerializer, LogOutSerializer

class KakaoLogInView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(responses={200 : KakaoLogInSerializer, 201 : KakaoLogInSerializer, 400 : "Invalid User", 401 : "Unauthorized User", 500 : "Internal Server Error"}, tags=["User"], operation_summary="Kakao Login")
    def get(self, request):
        try:
            kakao_access_token = request.headers.get('Authorization')

            if not kakao_access_token:
                return JsonResponse(data={'message' : 'Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)
            
            kakao_user_info_api = 'https://kapi.kakao.com/v2/user/me'
            user_info_response  = requests.get(kakao_user_info_api, headers={'Authorization' : f'Bearer {kakao_access_token}'}, timeout=2).json()
            
            if user_info_response.get('code') == -401:
                return Response(data={'message' : 'Unauthorized User'}, status=status.HTTP_401_UNAUTHORIZED)

            kakao_id = user_info_response['id']
            name     = user_info_response['properties']['nickname']
            email    = user_info_response['kakao_account']['email']
            
            user, is_created = User.objects.get_or_create(
                    kakao_id = kakao_id,
                    defaults = {'name' : name, 'email' : email}
            )

            refresh_token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(weeks=2)}, SECRET_KEY, ALGORITHM)

            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            
            data = {
                'refresh_token' : refresh_token,
                'name'          : name,
                'email'         : email
            }
            
            serializer = KakaoLogInSerializer(user, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status_code)
            
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except KeyError:
            return JsonResponse(data={'message' : 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    @login_decorator
    @swagger_auto_schema(responses={200 : LogOutSerializer, 400 : "Invalid User", 401 : "Unauthorized User", 500 : "Internal Server Error"}, tags=["User"], operation_summary="Renewal Refresh Token")
    def get(self, request):
        try:
            user = request.user
            data = {'refresh_token' : None}

            serializer = LogOutSerializer(user, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
            else:
                return JsonResponse(data=serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except KeyError:
            return JsonResponse(data={'message' : 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)


class RenewalingToken(APIView):
    @login_decorator
    @swagger_auto_schema(responses={201 : RenewalingTokenSerializer, 400 : "Invalid User", 401 : "Unauthorized User", 500 : "Internal Server Error"}, tags=["User"], operation_summary="Renewal Refresh Token")
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return JsonResponse(data={'message' : 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user

            if user.refresh_token == refresh_token:
                refresh_token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(weeks=2)}, SECRET_KEY, ALGORITHM)
                
                data = {"refresh_token" : refresh_token}
            
                serializer = RenewalingTokenSerializer(user, data=data)
                
                if serializer.is_valid():
                    serializer.save()
                    
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                
                else:
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            else:
                raise User.DoesNotExist
        
        except KeyError:
            return JsonResponse(data={'message' : 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return JsonResponse(data={"message" : "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return JsonResponse(data={'message' : 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)