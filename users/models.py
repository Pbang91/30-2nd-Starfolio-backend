from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
    name          = models.CharField(max_length=45)
    password      = models.CharField(max_length=200, blank=True)
    email         = models.EmailField(max_length=100, unique=True)
    kakao_id      = models.BigIntegerField()
    refresh_token = models.CharField(max_length=2000, null=True, unique=True)
    
    class Meta:
        db_table = 'users'
