import jwt

from django.http        import JsonResponse

from .models            import User
from starfolio.settings import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            if 'Authorization' not in request.headers:
                return JsonResponse({"message" : "NO_AUTHORIZATION"}, status = 401)
            
            access_token = request.headers.get('Authorization')           
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user_id      = payload['id']
            request.user = User.objects.get(id = user_id)

            return func(self, request, *args, **kwargs)
        
        except User.DoesNotExist:
            return JsonResponse({"mesaage" : "INVALID_USER"}, status = 401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)

        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({"message" : "EXPIRED_TOKEN"}, status = 401)
        
        except KeyError:
           return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    return wrapper