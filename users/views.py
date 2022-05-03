import requests, jwt

from datetime           import datetime, timedelta

from django.views       import View
from django.http        import JsonResponse
from django.db          import transaction

from starfolio.settings import SECRET_KEY, ALGORITHM
from users.models       import User

class KakaoLogInView(View):
    def get(self, request):
        try:
            kakao_access_token  = request.headers.get('Authorization')           
            kakao_user_info_api = 'https://kapi.kakao.com/v2/user/me'
            user_info_response  = requests.get(kakao_user_info_api, headers={'Authorization' : f'Bearer {kakao_access_token}'}, timeout=2).json()

            if user_info_response.get('code') == -401:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)

            kakao_id = user_info_response['id']
            name     = user_info_response['properties']['nickname']
            email    = user_info_response['kakao_account']['email']
            
            access_token  = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
            refresh_token = jwt.encode({'id' : user.id, 'exp' : datetime.utcnow() + timedelta(weeks=2)}, SECRET_KEY, ALGORITHM)

            user, is_created = User.objects.get_or_create(
                    kakao_id      = kakao_id,
                    refresh_token = refresh_token,
                    defaults      = {'name' : name, 'email' : email}
            )
            
            data = {
                'access_token'  : access_token,
                'refresh_token' : refresh_token,
                'name'          : name,
                'email'         : email
            }
            
            return JsonResponse({'message' : 'SUCCESS', 'data' : data}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class RenewalingToken(View):
    def post(self, request):
        try:
            refresh_token  = request.headers.get('Authorization')

            if not refresh_token:
                raise KeyError
                
            payload = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
            user_id = payload['id']
            user = User.objects.get(id = user_id, refresh_token = refresh_token)

            if user:
                with transaction.atomic():
                    access_token  = jwt.encode({'id' : user_id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
                    refresh_token = jwt.encode({'id' : user_id, 'exp' : datetime.utcnow() + timedelta(weeks=2)}, SECRET_KEY, ALGORITHM)

                    data = {
                        "access_token"  : access_token,
                        "refresh_token" : refresh_token
                    }

                    user.refresh_token = refresh_token
                    user.save()

                    return JsonResponse({"message" : "SUCCESS", "data" : data}, status = 200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({"message" : "UNAUTHORIZED_USER"}, status = 401)

        