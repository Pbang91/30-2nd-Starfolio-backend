import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import jwt
import bcrypt

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from starfolio.settings import SECRET_KEY, ALGORITHM

from .models import User

class KakaoLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('kakao_login')
        
        password = bcrypt.hashpw("test1234!".encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
        cls.user = User.objects.create(
                id = 1,
                name = 'testman',
                password  = password,
                email = 'test@test.com',
                kakao_id = 1234567891111
        )

        cls.f_client = APIClient()

        token = jwt.encode({'id' : cls.user.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

        cls.f_client.credentials(HTTP_AUTHORIZATION=token)

    @patch('users.views.requests')
    def test_success_user_login_with_kakao_exists_user(self, moked_request):
        class MockedResponse:
            def json(self):
                return {
                    'id' : 1234567891111,
                    'kakao_account' : {
                        'email' : 'test@test.com'
                    },
                    'properties' : {
                        'nickname' : 'testman'
                    }
                }
        
        moked_request.get = MagicMock(return_value = MockedResponse())
        
        response = self.f_client.get(self.url)
        
        access_token  = response.json()['access_token']
        refresh_token = response.json()['refresh_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {   
                'access_token'  : access_token,
                'refresh_token' : refresh_token,
                'name'          : 'testman',
                'email'         : 'test@test.com'
            }
        )
    
    @patch('users.views.requests')
    def test_success_user_login_with_kakao_new_user(self, moked_requset):
        class MockedResponse:
            def json(self):
                return {
                    'id' : 15155151515,
                    'kakao_account' : {
                        'email' : 'newtest@test.com'
                    },
                    'properties' : {
                        'nickname' : 'new-testman'
                    }
                }
        
        moked_requset.get = MagicMock(return_value = MockedResponse())
        
        headers  = {'HTTP_Authorization' : 'fake_kkkktoken'}
        response = self.client.get(self.url, **headers, content_type='application/json')

        access_token  = response.json()['access_token']
        refresh_token = response.json()['refresh_token']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {   
                'access_token'  : access_token,
                'refresh_token' : refresh_token,
                'name'          : 'new-testman',
                'email'         : 'newtest@test.com'
            }
        )

    @patch('users.views.requests')
    def test_fail_user_login_due_to_invalid_token(self, moked_requset):
        class MockedResponse:
            def json(self):
                return {
                    'code' : -401
                }
        
        moked_requset.get = MagicMock(return_value = MockedResponse())
        
        headers  = {'HTTP_Authorization' : 'Invalid Token'}
        response = self.client.get(self.url, **headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Unauthorized User'
            }
        )

class LogOutTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('logout')
        
        password = bcrypt.hashpw("test1234!".encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
        cls.user = User.objects.create(
                id = 1,
                name = 'testman',
                password  = password,
                email = 'test@test.com',
                kakao_id = 1234567891111
        )

        cls.f_client = APIClient()

        token = jwt.encode({'id' : cls.user.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

        cls.f_client.credentials(HTTP_AUTHORIZATION=token)
    
    def test_success_user_logout(self):
        response = self.f_client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'access_token' : None,
                'refresh_token' : None
            }
        )
    
    def test_fail_user_logout_due_to_unauthorized_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                "message" : "Unauthorized User"
            }
        )

class RenewalingTokenTest(APITestCase):
    maxDiff: int = None

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('refresh')

        password = bcrypt.hashpw("test1234!".encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
        
        cls.user = User.objects.create(
                id = 1,
                name = 'testman',
                password  = password,
                email = 'test@test.com',
                kakao_id = 1234567891111
        )

        cls.refresh_token = jwt.encode({'id' : cls.user.id, 'exp' : datetime.utcnow() + timedelta(weeks=2)}, SECRET_KEY, ALGORITHM)

        cls.user.refresh_token = cls.refresh_token
        cls.user.save()

        access_token = jwt.encode({'id' : cls.user.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)
        
        cls.f_client = APIClient()

        cls.f_client.credentials(HTTP_AUTHORIZATION=access_token)

    def test_success_renewal_refresh_token(self):
        refresh_token = self.refresh_token
        
        data = {
            "refresh_token" : refresh_token
        }
    
        response = self.f_client.post(self.url, data=json.dumps(data), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'access_token' : response.json()['access_token'],
                'refresh_token' : response.json()['refresh_token']
            }
        )
    
    def test_fail_renewal_refresh_token_due_to_data(self):
        data = {
            "reffff" : self.refresh_token
        }

        response = self.f_client.post(self.url, data=json.dumps(data), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : "Invalid Data"
            }
        )
    
    def test_fail_renewal_refresh_token_due_to_unathroized_access_token(self):
        refresh_token = self.refresh_token
        
        data = {
            "refresh_token" : refresh_token
        }

        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Unauthorized User'
            }
        )
    
    def test_fail_renewal_refresh_token_due_to_unathroized_refresh_token(self):
        data = {
            "refresh_token" : "fake_refresh_token"
        }

        response = self.f_client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Invalid User'
            }
        )