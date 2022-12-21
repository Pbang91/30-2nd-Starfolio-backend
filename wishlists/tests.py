import json
from datetime import datetime, timedelta

import bcrypt
import jwt

from rest_framework.test import APITestCase, APIClient

from users.models import User
from planets.models import Galaxy, PlanetTheme, Planet, Accomodation
from wishlists.models import WishList
from starfolio.settings import SECRET_KEY, ALGORITHM

class WishListTest(APITestCase):
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):
        password = bcrypt.hashpw("test1234!".encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

        cls.user = User.objects.create(
            id       = 1,
            name     = 'testman',
            password = password,
            email    = 'test@test.com',
            kakao_id = 1234567891111
        )

        cls.f_client = APIClient()

        token = jwt.encode({'id' : cls.user.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

        cls.f_client.credentials(HTTP_AUTHORIZATION=token)

        Galaxy.objects.create(
            id   = 1,
            name = '우리은하'
        )

        PlanetTheme.objects.create(
            id   = 1,
            name = '불'
        )

        Planet.objects.bulk_create([
            Planet(
                id        = 1,
                name      = '멋진행성',
                thumbnail = 'https://wonderful.img/test1.jpg',
                theme_id  = 1,
                galaxy_id = 1
            ),
            Planet(
                id        = 2,
                name      = '이쁜행성',
                thumbnail = 'https://beautiful.img/test1.jpg',
                theme_id  = 1,
                galaxy_id = 1
            )
        ])

        Accomodation.objects.create(
            id            = 1,
            name          = '멋진숙소',
            price         = 100000.00,
            min_of_people = 2,
            max_of_people = 4,
            num_of_bed    = 2,
            description   = "편안합니다.",
            planet_id     = 1
        )

        WishList.objects.create(
            id        = 1,
            user_id   = 1,
            planet_id = 1
        )

    def test_success_wishlist_create(self):
        '''
        장바구니 저장
        '''
        data = {'planet_id' : 2}
        
        response = self.f_client.post('/api/wishlists', data=json.dumps(data), content_type='application/json')

        created_at = response.json()['created_at']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                'id' : 2,
                'user' : 1,
                'planet' : {
                    'id' : 2,
                    'name' : '이쁜행성',
                    'thumbnail' : 'https://beautiful.img/test1.jpg',
                    'theme' : {
                        'name' : '불'
                    },
                    'galaxy' : {
                        'name' : '우리은하'
                    },
                    'planetimage_set' : [],
                    'accomodation_set' : []
                },
                'created_at' : created_at
            }
        )

    def test_success_wishlist_exist_wish_view(self):
        '''
        장바구니 보기
        '''
        response = self.f_client.get('/api/wishlists')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id' : 1,
                    'planet' : {
                        'id' : 1,
                        'name' : '멋진행성',
                        'thumbnail' : 'https://wonderful.img/test1.jpg',
                        'galaxy' : {
                            'name' : '우리은하'
                        },
                        'theme' : {
                            'name' : '불'
                        },
                        'planetimage_set' : [],
                        'accomodation_set' : [
                            {
                                'min_of_people' : 2,
                                'max_of_people' : 4,
                                'price' : '100000.00'
                            }
                        ]
                    }
                }
            ]
        )
    
    def test_success_wishlist_non_exist_wish_view(self):
        WishList.objects.all().delete()
        
        response = self.f_client.get('/api/wishlists')

        self.assertEqual(response.status_code, 204)


    def test_fail_wishlist_create_due_to_invlid_planet(self):
        data = {
            'planet_id' : 555
        }

        response = self.f_client.post('/api/wishlists', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Inavlid Planet'
            }
        )

    def test_fail_wishlist_create_due_to_invlid_request(self):
        data = {
            "planet_idddddd" : 2
        }

        response = self.f_client.post('/api/wishlists', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Inavlid Required Value'
            }
        )

    