from uuid import uuid4

import bcrypt

from rest_framework.test import APITestCase, APIClient

from users.models import User
from bookings.models import Booking, BookingStatus

from .models import Accomodation, AccomodationImage, Planet, PlanetImage, PlanetTheme, Galaxy

class PlanetListTest(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        
        Galaxy.objects.bulk_create([
            Galaxy(
                id   = 1,
                name = '우리은하'
            ),
            Galaxy(
                id   = 2,
                name = '안드로메다'
            )
        ])

        PlanetTheme.objects.bulk_create([
            PlanetTheme(
                id   = 1,
                name = '얼음'
            ),
            PlanetTheme(
                id   = 2,
                name = '불'
            )
        ])

        Planet.objects.bulk_create([
            Planet(
                id        = 1,
                name      = '이쁜행성',
                thumbnail = 'https://test.server/thumbnail1.jpg',
                theme_id  = 1,
                galaxy_id = 1
            ),
            Planet(
                id        = 2,
                name      = '멋진행성',
                thumbnail = 'https://test.server/thumbnail2.jpg',
                theme_id  = 2,
                galaxy_id = 2
            )
        ])

        PlanetImage.objects.bulk_create([
            PlanetImage(
                id        = 1,
                image_url = 'testurl/testurl/test1.jpg',
                planet_id = 1
            ),
            PlanetImage(
                id        = 2,
                image_url = 'testurl/testurl/test2.jpg',
                planet_id = 1
            ),
            PlanetImage(
                id        = 3,
                image_url = 'testurl/testurl/test3.jpg',
                planet_id = 2
            )
        ])

        Accomodation.objects.bulk_create([
            Accomodation(
                id            = 1,
                name          = '이쁜숙소',
                price         = 2500000.00,
                min_of_people = 2,
                max_of_people = 4,
                num_of_bed    = 2,
                description   = '엄청 이쁜 숙소입니다.',
                planet_id     = 1
            ),
            Accomodation(
                id            = 2,
                name          = '멋진호텔',
                price         = 200000.00,
                min_of_people = 4,
                max_of_people = 8,
                num_of_bed    = 4,
                description   = '큽니다.',
                planet_id     = 2
            )
        ])

    def test_success_planet_list_view_without_any_condition(self):
        response = self.client.get('/api/planets')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            [
                {
                    'id' : 1,
                    'name' : '이쁜행성',
                    'galaxy' : {
                        'name' : '우리은하'
                    },
                    'theme' : {
                        'name' : '얼음'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test1.jpg'
                        },
                        {
                            'image_url' : 'testurl/testurl/test2.jpg'
                        }
                    ],
                    'thumbnail' : 'https://test.server/thumbnail1.jpg',
                    'accomodation_set' : [
                        {
                            'max_of_people': 4,
                            'min_of_people': 2,
                            'price': '2500000.00'
                        }
                    ]
                },
                {
                    'id' : 2,
                    'name' : '멋진행성',
                    'galaxy' : {
                        'name' : '안드로메다'
                    },
                    'theme' : {
                        'name' : '불'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test3.jpg'
                        }
                    ],
                    'thumbnail' : 'https://test.server/thumbnail2.jpg',
                    'accomodation_set' : [
                        {
                            'max_of_people': 8,
                            'min_of_people': 4,
                            'price': '200000.00'
                        }
                    ]
                }
            ]
        )

    def test_success_planet_list_view_with_galaxy_filter(self):
        response = self.client.get('/api/planets?galaxy=2&theme=2&people=5')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            [
                {
                    'id' : 2,
                    'name' : '멋진행성',
                    'thumbnail' : 'https://test.server/thumbnail2.jpg',
                    'galaxy' : {
                        'name' : '안드로메다'
                    },
                    'theme' : {
                        'name' : '불'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test3.jpg'
                        }
                    ],
                    'accomodation_set' : [
                        {
                            'min_of_people' : 4,
                            'max_of_people' : 8,
                            'price' : '200000.00'
                        }
                    ]
                }
            ]
        )

    def test_success_planet_list_view_with_price_filter(self):
        response = self.client.get('/api/planets?min-price=210000&max-price=2500000')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            [
                {
                    'id' : 1,
                    'name' : '이쁜행성',
                    'thumbnail' : 'https://test.server/thumbnail1.jpg',
                    'galaxy' : {
                        'name' : '우리은하'
                    },
                    'theme' : {
                        'name' : '얼음'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test1.jpg'
                        },
                        {
                            'image_url' : 'testurl/testurl/test2.jpg'
                        }
                    ],
                    'accomodation_set' : [
                        {
                            'max_of_people': 4,
                            'min_of_people': 2,
                            'price': '2500000.00'
                        }
                    ]
                }
            ]
        )

    def test_success_planet_list_view_with_searching_filter(self):
        response = self.client.get('/api/planets?searching=멋진행성')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    'id' : 2,
                    'name' : '멋진행성',
                    'thumbnail' : 'https://test.server/thumbnail2.jpg',
                    'galaxy' : {
                        'name' : '안드로메다'
                    },
                    'theme' : {
                        'name' : '불'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test3.jpg'
                        }
                    ],
                    'accomodation_set' : [
                        {
                            'min_of_people' : 4,
                            'max_of_people' : 8,
                            'price' : '200000.00'
                        }
                    ]
                }
            ]
        )

    def test_success_planet_list_view_with_sort(self):
        response = self.client.get('/api/planets?sort=asc')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                 {
                    'id' : 2,
                    'name' : '멋진행성',
                    'galaxy' : {
                        'name' : '안드로메다'
                    },
                    'theme' : {
                        'name' : '불'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test3.jpg'
                        }
                    ],
                    'thumbnail' : 'https://test.server/thumbnail2.jpg',
                    'accomodation_set' : [
                        {
                            'max_of_people': 8,
                            'min_of_people': 4,
                            'price': '200000.00'
                        }
                    ]
                },
                {
                    'id' : 1,
                    'name' : '이쁜행성',
                    'galaxy' : {
                        'name' : '우리은하'
                    },
                    'theme' : {
                        'name' : '얼음'
                    },
                    'planetimage_set' : [
                        {
                            'image_url' : 'testurl/testurl/test1.jpg'
                        },
                        {
                            'image_url' : 'testurl/testurl/test2.jpg'
                        }
                    ],
                    'thumbnail' : 'https://test.server/thumbnail1.jpg',
                    'accomodation_set' : [
                        {
                            'max_of_people': 4,
                            'min_of_people': 2,
                            'price': '2500000.00'
                        }
                    ]
                }
            ]
        )

    def test_fail_planetlistview_get_invalid_date(self):
        response = self.client.get('/api/planets?check-in=2022-03-19&check-out=2022-03-18')
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Invalid Date'
            }
        )

class PlanetDetailTest(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        password = bcrypt.hashpw('test1234!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cls.user = User.objects.create(
            id = 1,
            name = "testman",
            password = password,
            email = "test@test.com",
            kakao_id = 12345678911
        )

        cls.client = APIClient()

        PlanetTheme.objects.create(
            id   = 1,
            name = '불'
        )

        Galaxy.objects.create(
            id   = 1,
            name = '우리은하'
        )

        Planet.objects.create(
            id        = 1,
            name      = '이쁜행성',
            thumbnail = 'testurl/testurl/test',
            theme_id  = 1,
            galaxy_id = 1
        )

        PlanetImage.objects.create(
            id        = 1,
            image_url = 'https://testurl/testurl/test1.jpg',
            planet_id = 1
        )

        BookingStatus.objects.create(
            id     = 1,
            status = '예약중'
        )

        Accomodation.objects.create(
            id            = 1,
            name          = '이쁜숙소',
            price         = 2500000.00,
            min_of_people = 2,
            max_of_people = 4,
            num_of_bed    = 2,
            description   = '엄청 이쁜 숙소입니다.',
            planet_id     = 1
        )

        AccomodationImage.objects.create(
            id              = 1,
            image_url       = 'https://beautiful.img/test1.jpg',
            accomodation_id = 1
        )

        booking_number1 = uuid4()
        booking_number2 = uuid4()

        Booking.objects.bulk_create([
                Booking(
                    id                 = 1,
                    booking_number     = booking_number1,
                    start_date         = '2022-12-01',
                    end_date           = '2022-12-15',
                    price              = 222222,
                    number_of_adults   = 2,
                    number_of_children = 0,
                    user_request       = '깨끗하게 청소해주세요 :).',
                    user               = cls.user,
                    booking_status_id  = 1,
                    planet_id          = 1,
                    accomodation_id    = 1
                ),
                Booking(
                    id                 = 2,
                    booking_number     = booking_number2,
                    start_date         = '2023-02-01',
                    end_date           = '2023-02-10',
                    price              = 5555555,
                    number_of_adults   = 2,
                    number_of_children = 0,
                    user_request       = '',
                    user               = cls.user,
                    booking_status_id  = 1,
                    planet_id          = 1,
                    accomodation_id    = 1
                )
            ]
        )

    def test_success_accomodation_view_when_list_page_checked_date(self):
        response = self.client.get('/api/planets/1/accomodation/1?check-in=2023-03-01&check-out=2023-03-05')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),{
                'id' : 1,
                'name' : '이쁜숙소',
                'stays' : 4,
                'price' : 10000000.00,
                'accomodationimage_set' : [
                    {
                        'image_url' : 'https://beautiful.img/test1.jpg'
                    }
                ],
                'description' : '엄청 이쁜 숙소입니다.',
                'invalid_dates' : [
                    '2023-02-01',
                    '2023-02-02',
                    '2023-02-03',
                    '2023-02-04',
                    '2023-02-05',
                    '2023-02-06',
                    '2023-02-07',
                    '2023-02-08',
                    '2023-02-09'
                ],
                'max_of_people' : 4,
                'min_of_people' : 2,
                'num_of_bed' : 2,
            }
        )

    def test_success_accomodation_view_when_list_page_unchecked_date(self):
        response = self.client.get('/api/planets/1/accomodation/1?check-in=&check-out=')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'id' : 1,
                'name' : '이쁜숙소',
                'stays' : None,
                'price' : None,
                'accomodationimage_set' : [
                    {
                        'image_url' : 'https://beautiful.img/test1.jpg'
                    }
                ],
                'description' : '엄청 이쁜 숙소입니다.',
                'invalid_dates' : [
                    '2023-02-01',
                    '2023-02-02',
                    '2023-02-03',
                    '2023-02-04',
                    '2023-02-05',
                    '2023-02-06',
                    '2023-02-07',
                    '2023-02-08',
                    '2023-02-09'
                ],
                'max_of_people' : 4,
                'min_of_people' : 2,
                'num_of_bed' : 2,
            }
        )

    def test_fail_accomodation_booking_due_to_invalid_check_in_date(self):
        response = self.client.get('/api/planets/1/accomodation/1?check-in=2023-02-09&check-out=2023-02-15')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Invalid Date'
            }
        )
        
    def test_fail_accomodation_booking_due_to_invalid_check_out_date(self):
        response = self.client.get('/api/planets/1/accomodation/1?check-in=2023-01-28&check-out=2023-02-02')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Invalid Date'
            }
        )

    def test_fail_accomodation_booking_due_to_invalid_accomodation_id(self):
        response = self.client.get('/api/planets/1/accomodation/255?check-in=&check-out=')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Invalid Accomodation'
            }
        )
    
    def test_fail_accomodation_booking_due_to_invalid_planet_id(self):
        response = self.client.get('/api/planets/555/accomodation/1?check-in=&check-out=')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message' : 'Invalid Accomodation'
            }
        )