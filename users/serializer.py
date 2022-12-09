import jwt
from datetime import datetime, timedelta

from rest_framework import serializers

from starfolio.settings import SECRET_KEY, ALGORITHM

from .models import User

class KakaoLogInSerializer(serializers.Serializer):
    name          = serializers.CharField()
    email         = serializers.EmailField()
    access_token  = serializers.CharField(max_length=255)
    refresh_token = serializers.CharField()

class RenewalingTokenSerializer(serializers.ModelSerializer):
    access_token  = serializers.SerializerMethodField(method_name="get_access_token")
    
    class Meta:
        model = User
        fields = ("name", "email", "refresh_token", "access_token")
    
    def update(self, instance : User, validated_data):
        instance.refresh_token = validated_data.get('refresh_token', instance.refresh_token)

        instance.save()
        instance.refresh_from_db()

        return instance
    
    def get_access_token(self, obj):
        obj.access_token  = jwt.encode({'id' : obj.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

        return obj.access_token

class LogOutSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField(method_name="get_access_token")
    
    class Meta:
        model = User
        fields = ("refresh_token", "access_token")

    def update(self, instance : User, validated_data):
        instance.refresh_token = validated_data.get('refresh_token', None)
        
        instance.save()
        instance.refresh_from_db()

        return instance
    
    def get_access_token(self, obj):
        obj.access_token = None

        return obj.access_token