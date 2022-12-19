from datetime import datetime, timedelta

from rest_framework import serializers

from bookings.models import Booking

from .models import Planet, Galaxy, PlanetTheme, PlanetImage, Accomodation, AccomodationImage

class AccomodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accomodation
        fields = ('min_of_people', 'max_of_people', 'price')

class PlanetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetImage
        fields = ('image_url',)

class PlanetThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetTheme
        fields = ('name',)

class GalaxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Galaxy
        fields = ('name',)

class PlanetSerializer(serializers.ModelSerializer):
    galaxy = GalaxySerializer(read_only=True)
    theme = PlanetThemeSerializer(read_only=True)
    planetimage_set = PlanetImageSerializer(read_only=True, many=True)
    accomodation_set = AccomodationSerializer(read_only=True, many=True)

    class Meta:
        model = Planet
        fields = ('id', 'name', 'thumbnail', 'galaxy', 'theme', 'planetimage_set', 'accomodation_set')

class AccomodationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccomodationImage
        fields = ('image_url', )

class PlanetDetailSerializer(serializers.ModelSerializer):
    invalid_dates = serializers.SerializerMethodField('get_invalid_dates')
    accomodationimage_set = AccomodationImageSerializer(read_only=True, many=True)

    class Meta:
        model = Accomodation
        fields = ('id', 'name', 'price', 'description', 'accomodationimage_set', 'min_of_people', 'max_of_people', 'num_of_bed', 'invalid_dates')

        extra_kwargs = {
            'name' : {'required' : False},
            'description': {'required' : False},
            'min_of_people' : {'required' : False},
            'max_of_people' : {'required' : False},
            'num_of_bed' : {'required' : False},
        }

    def get_invalid_dates(self, obj):
        unavailable_bookings = Booking.objects.filter(accomodation=obj,
                                                      start_date__lte=datetime.today()+timedelta(days=186),
                                                      end_date__gte=datetime.today()
                                )

        invalid_dates = []

        for unavailable_booking in unavailable_bookings:
            booked_out_stays = (unavailable_booking.end_date - unavailable_booking.start_date).days
            invalid_dates   += [datetime.strftime(unavailable_booking.start_date+timedelta(days=booked_out_stay), "%Y-%m-%d") for booked_out_stay in range(booked_out_stays)]
        
        obj.invalid_dates = invalid_dates

        return obj.invalid_dates