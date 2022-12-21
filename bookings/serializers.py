from typing import OrderedDict

from rest_framework import serializers

from .models import Booking, BookingStatus

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatus
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
        booking = Booking.objects.create(**validated_data)

        return booking
    
    def update(self, obj : Booking, validated_data : OrderedDict):
        obj.start_date = validated_data.get('start_date', obj.start_date)
        obj.end_date = validated_data.get('end_date', obj.end_date)
        obj.number_of_adults = validated_data.get('number_of_adults', obj.number_of_adults)
        obj.number_of_children = validated_data.get('number_of_children', obj.number_of_children)
        obj.user_request = validated_data.get('user_request', obj.user_request)

        return obj