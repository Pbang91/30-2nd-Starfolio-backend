import jwt
from datetime import datetime, timedelta

from rest_framework import serializers

from starfolio.settings import SECRET_KEY, ALGORITHM

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class KakaoLogInSerializer(serializers.Serializer):
    name          = serializers.CharField()
    email         = serializers.EmailField()
    access_token  = serializers.SerializerMethodField(method_name="get_access_token")
    refresh_token = serializers.CharField()

    def update(self, instance : User, validated_data):
        instance.refresh_token = validated_data.get('refresh_token')
        return instance
    
    def get_access_token(self, obj):
        obj.access_token  = jwt.encode({'id' : obj.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

        return obj.access_token

class RenewalingTokenSerializer(serializers.Serializer):
    access_token  = serializers.SerializerMethodField(method_name="get_access_token")
    refresh_token = serializers.CharField()
    
    def update(self, instance : User, validated_data): # 만약 ModelSerializer를 사용한다면 create와 update는 구현하지 않아도 된다.
        instance.refresh_token = validated_data.get('refresh_token')

        return instance
    
    def get_access_token(self, obj):
        obj.access_token  = jwt.encode({'id' : obj.id, 'exp' : datetime.utcnow() + timedelta(days=2)}, SECRET_KEY, ALGORITHM)

        return obj.access_token

class LogOutSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField(method_name="get_access_token")
    
    class Meta:
        model = User
        fields = ("refresh_token", "access_token")
    
    def get_access_token(self, obj):
        obj.access_token = None

        return obj.access_token