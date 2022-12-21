from rest_framework import serializers

from planets.serializers import PlanetSerializer

from .models import WishList

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WishList
        fields = ('id', 'user', 'planet', 'created_at')
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        
        res.update({'planet': PlanetSerializer(instance.planet).data})
        
        return res

class WishListDetailSerializer(serializers.ModelSerializer):
    planet = PlanetSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = ('id', 'planet')