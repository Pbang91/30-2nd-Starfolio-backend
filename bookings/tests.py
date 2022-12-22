import json
from datetime import datetime, timedelta

import jwt
import bcrypt

from rest_framework.test import APITestCase, APIClient

from users.models import User
from planets.models import Planet, Accomodation, Galaxy, PlanetTheme
from bookings.models import BookingStatus, Booking
from starfolio.settings import SECRET_KEY, ALGORITHM

class BookingTest(APITestCase):
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

        Planet.objects.create(
            id        = 1,
            name      = '멋진행성',
            thumbnail = 'https://wonderful.img/test1.jpg',
            theme_id  = 1,
            galaxy_id = 1
        )

        Accomodation.objects.create(
            id            = 1,
            name          = '멋진숙소',
            price         = 10000,
            min_of_people = 2,
            max_of_people = 4,
            num_of_bed    = 2,
            description   = "멋져요.",
            planet_id     = 1
        )

        BookingStatus.objects.create(
            id     = 1,
            status = 'PENDING'
        )       

        Booking.objects.create(
            id                 = 1,
            booking_number     = 5678,
            start_date         = '2022-12-01',
            end_date           = '2022-12-10',
            number_of_adults   = 1,
            number_of_children = 1,
            user_request       = '조용한 곳을 부탁드립니다.',
            price              = 20000,
            user_id            = 1,
            booking_status_id  = 1,
            planet_id          = 1,
            accomodation_id    = 1
        )

        Booking.objects.create(
            id                 = 2,
            booking_number     = 495912305902135,
            start_date         = '2022-10-10',
            end_date           = '2022-10-15',
            number_of_adults   = 1,
            number_of_children = 1,
            user_request       = '청소 부탁드려요.',
            price              = 30000,
            user_id            = 1,
            booking_status_id  = 1,
            planet_id          = 1,
            accomodation_id    = 1
        )

        Booking.objects.create(
            id                 = 3,
            booking_number     = 11222444525,
            start_date         = '2023-01-01',
            end_date           = '2023-01-20',
            number_of_adults   = 1,
            number_of_children = 1,
            user_request       = '새해맞이',
            price              = 30000,
            user_id            = 1,
            booking_status_id  = 1,
            planet_id          = 1,
            accomodation_id    = 1
        )

    def test_success_booking_accomodation(self):
        '''
        Book New Accomodation
        '''
        booking = {
            'booking_number'     : 1,
            'start_date'         : '2023-01-22',
            'end_date'           : '2023-01-25',
            'number_of_adults'   : 1,
            'number_of_children' : 1,
            'user_request'       : '깨끗하게 부탁드려요.',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 1
        }

        response = self.f_client.post('/api/bookings', json.dumps(booking), content_type='application/json')

        booking_number = response.json()['booking_number']

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {   
                'id' : 4,
                'booking_number': booking_number,
                'start_date': '2023-01-22',
                'end_date': '2023-01-25',
                'number_of_adults': 1,
                'number_of_children': 1,
                'user_request': '깨끗하게 부탁드려요.',
                'accomodation_id': 1,
                'booking_status_id': 1,
                'planet_id': 1,
                'price': '10000.00'
            }
        )

    def test_success_booking_accomodation_list_with_filter_history(self):
        '''
        Get Booked Accomodation Information
        '''
        response = self.f_client.get('/api/bookings?my-stay=history')
        
        booking_number1 = str(Booking.objects.get(id=1).booking_number)
        booking_number2 = str(Booking.objects.get(id=2).booking_number)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id' : 1,
                    'booking_number' : booking_number1,
                    'start_date' : '2022-12-01',
                    'end_date' : '2022-12-10',
                    'number_of_adults': 1,
                    'number_of_children': 1,
                    'user_request': '조용한 곳을 부탁드립니다.',
                    'price': '20000.00',
                    'booking_status_id': 1,
                    'accomodation_id': 1,
                    'planet_id': 1,
                },
                {
                    'id' : 2,
                    'booking_number' : booking_number2,
                    'start_date' : '2022-10-10',
                    'end_date' : '2022-10-15',
                    'number_of_adults': 1,
                    'number_of_children': 1,
                    'user_request': '청소 부탁드려요.',
                    'price': '30000.00',
                    'booking_status_id': 1,
                    'accomodation_id': 1,
                    'planet_id': 1,
                }
            ]
        )
    
    def test_success_booking_accomodation_list_with_filter_booked(self):
        response = self.f_client.get('/api/bookings?my-stay=booking-info')

        booking_number = str(Booking.objects.get(id=3).booking_number)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id' : 3,
                    'booking_number' : booking_number,
                    'start_date' : '2023-01-01',
                    'end_date' : '2023-01-20',
                    'number_of_adults': 1,
                    'number_of_children': 1,
                    'user_request': '새해맞이',
                    'price': '30000.00',
                    'booking_status_id': 1,
                    'accomodation_id': 1,
                    'planet_id': 1,
                }
            ]
        )

    def test_success_booking_accomodation_update(self):
        '''
        Update Booked Accomodation Information
        '''
        booking = {
            'start_date' : '2022-12-02',
            'end_date' : '2022-12-10',
            'number_of_adults' : 2
        }

        response = self.f_client.patch('/api/bookings/1', json.dumps(booking), content_type='application/json')
    
        booking_number = response.json()['booking_number']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id' : 1,
                'booking_number' : booking_number,
                'start_date' : '2022-12-02',
                'end_date' : '2022-12-10',
                'number_of_adults': 2,
                'number_of_children': 1,
                'user_request': '조용한 곳을 부탁드립니다.',
                'price': '20000.00',
                'booking_status_id': 1,
                'accomodation_id': 1,
                'planet_id': 1,
            }
        )

    def test_success_booking_accomodation_cancel(self):
        '''
        Cancel Booked Accomodation
        '''
        response = self.f_client.delete('/api/bookings?booking-ids=1')
        
        self.assertEqual(response.status_code, 204)
    
    '''
    아래 테스트 코드는 저장 직전 DB확인을 위한 테스트 코드. serializer와 물려 있기때문에
    한 개가 주석처리되어 있으면, 다른 한개도 주석처리되어야 함
    '''
    # def test_fail_bookin_accomodation_due_to_already_booked_other_people(self):
    #     booking = {
    #         'booking_number'     : 1,
    #         'start_date'         : '2023-05-22',
    #         'end_date'           : '2023-05-25',
    #         'number_of_adults'   : 1,
    #         'number_of_children' : 1,
    #         'user_request'       : '깨끗하게 부탁드려요.',
    #         'total_price'        : 10000,
    #         'planet_id'          : 1,
    #         'accomodation_id'    : 1
    #     }

    #     response = self.f_client.post('/api/bookings', json.dumps(booking), content_type='application/json')

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(
    #         response.json(),
    #         {
    #             'message':'Already Booked Accomodation'
    #         }
    #     )

    def test_fail_booking_accomodation_due_to_invalid_people(self):
        '''
        Book New Accomodation Fail
        '''
        booking = {
            'start_date'         : '2023-03-22',
            'end_date'           : '2023-03-23',
            'number_of_adults'   : 10,
            'number_of_children' : 1,
            'user_request'       : '테스트',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 1
        }
        response = self.f_client.post('/api/bookings', json.dumps(booking), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Invalid Num Of People'
            }
        )

    def test_fail_booking_accomodation_due_to_already_booked(self):
        booking = {
            'start_date'         : '2022-12-01',
            'end_date'           : '2022-12-10',
            'number_of_adults'   : 1,
            'number_of_children' : 1,
            'user_request'       : '테스트',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 1
        }
        response = self.f_client.post('/api/bookings', json.dumps(booking), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Already Booked Accomodation'
            }
        )

    def test_fail_booking_accomodation_due_to_invalid_accomodation(self):
        booking = {
            'start_date'         : '2023-03-22',
            'end_date'           : '2023-03-23',
            'number_of_adults'   : 10,
            'number_of_children' : 1,
            'user_request'       : '테스트',
            'total_price'        : 10000,
            'planet_id'          : 1,
            'accomodation_id'    : 200000
        }
        response = self.f_client.post('/api/bookings', json.dumps(booking), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Invalid Accomodation'
            }
        )
    
    def test_fail_booking_accomodation_due_to_invalid_request(self):
        booking = {
            'accomodation_id'    : 1
        }
        response = self.f_client.post('/api/bookings', json.dumps(booking), content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Invalid Request'
            }
        )
    
    def test_fail_booking_accomodation_list_due_to_invalid_filter(self):
        '''
        Get Booked Accomodation Information Fail
        '''
        response = self.f_client.get('/api/bookings')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message': 'Invalid Filter'
            }
        )

    def test_fail_booking_accomodation_update_due_to_invalid_id(self):
        '''
        Update Booked Accomodation Information Fail
        '''
        booking = {
            'start_date' : '2022-12-02',
            'end_date' : '2022-12-10'
        }

        response = self.f_client.patch('/api/bookings/200', json.dumps(booking), content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {
                'message':'Invalid Booking Information'
            }
        )

    def test_fail_booking_accomodation_cancel_due_to_invalid_ids(self):
        '''
        Cancel Booked Accomodation Fail
        '''
        response = self.f_client.delete('/api/bookings?booking-ids=10&booking-ids=5&booking-ids=6')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message':'Invalid Booking Information'
            }
        )