import jwt

from django.http import JsonResponse

from rest_framework import status

from starfolio.settings import SECRET_KEY, ALGORITHM

from .models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            if 'Authorization' not in request.headers:
                return JsonResponse({"message" : "Unauthorized User"}, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token = request.headers.get('Authorization')           
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user_id      = payload['id']
            request.user = User.objects.get(id=user_id)

            return func(self, request, *args, **kwargs)
        
        except User.DoesNotExist:
            return JsonResponse({"mesaage" : "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({"message" : "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError:
           return JsonResponse({"message" : "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)

    return wrapper