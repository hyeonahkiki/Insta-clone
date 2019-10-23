from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

#이미만들어진 모델에 좀만 더 기능을 추가하는 방향
class User(AbstractUser):
    # M대 N을 연결하기 위해서(USER랑 연결해야하는데 
    # 자기 자신과 연결할 수 없기 때문에 settings.AUTH_USER_MODEL로 연결 그런데 이건 기본 auth.user랑 연결되이있어서)
    # 설정을 바꿔야한다
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='follwings')