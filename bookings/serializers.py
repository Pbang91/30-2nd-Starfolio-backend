from typing import OrderedDict
from datetime import timedelta

from django.db.models import Q
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Booking, BookingStatus

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BookingStatus
        fields = "__all__"

class BookingSerializer(serializers.Serializer):
    id                 = serializers.IntegerField(read_only=True)
    booking_number     = serializers.CharField()
    start_date         = serializers.DateField()
    end_date           = serializers.DateField()
    number_of_adults   = serializers.IntegerField()
    number_of_children = serializers.IntegerField()
    user_request       = serializers.CharField()
    price              = serializers.DecimalField(max_digits=11, decimal_places=2)
    user_id            = serializers.IntegerField(write_only=True)
    booking_status_id  = serializers.IntegerField()
    planet_id          = serializers.IntegerField()
    accomodation_id    = serializers.IntegerField()

    def create(self, validated_data):
        '''
        아래 create코드는 저장 직전 새로운 예약이 DB에 저장되었을 때 발생시키는 에러를 위한 Test Code
        '''
        # Booking.objects.create(
        #     id                 = 4,
        #     booking_number     = 4959,
        #     start_date         = '2023-05-22',
        #     end_date           = '2023-05-25',
        #     number_of_adults   = 1,
        #     number_of_children = 1,
        #     user_request       = '숙소 뺏기.',
        #     price              = 30000,
        #     user_id            = 1,
        #     booking_status_id  = 1,
        #     planet_id          = 1,
        #     accomodation_id    = 1
        # )
        
        q = Q()
        
        plnaet_id       = validated_data.get('planet_id')
        accomodation_id = validated_data.get('accomodation_id')
        start_date      = validated_data.get('start_date')
        end_date        = validated_data.get('end_date')

        q &= Q(accomodation_id=accomodation_id) & Q(planet_id=plnaet_id)
        q &= Q(start_date__range=(start_date, end_date-timedelta(days=1)))\
                 | Q(end_date__range=(start_date+timedelta(days=1), end_date))

        if not Booking.objects.filter(q):
            booking = Booking.objects.create(**validated_data)
        
        else:
            raise ValidationError(message="Already Booked Accomodation")

        return booking
    
    def update(self, obj : Booking, validated_data : OrderedDict):
        obj.start_date         = validated_data.get('start_date', obj.start_date)
        obj.end_date           = validated_data.get('end_date', obj.end_date)
        obj.number_of_adults   = validated_data.get('number_of_adults', obj.number_of_adults)
        obj.number_of_children = validated_data.get('number_of_children', obj.number_of_children)
        obj.user_request       = validated_data.get('user_request', obj.user_request)

        return obj

class BookingPostSchemaSerializer(serializers.Serializer):
    '''
    Booking Post 스키마 시리얼라이저 [Only Use Swagger]
    '''
    number_of_adults   = serializers.IntegerField(required=False)
    number_of_children = serializers.IntegerField(required=False)
    total_price        = serializers.IntegerField(required=False)
    plnet_id           = serializers.IntegerField()
    accomodation_id    = serializers.IntegerField()

class BookingUpdateSchemaSerializer(serializers.Serializer):
    '''
    Booking Patch 스키마 시리얼라이저 [Only User Swagger]
    '''
    booking_status   = serializers.IntegerField(required=False)
    number_of_adults = serializers.IntegerField(required=False)
    number_of_children = serializers.IntegerField(required=False)