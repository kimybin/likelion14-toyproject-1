from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string

def generate_invite_code():
    # A7K3D9 같은 6자리 랜덤 코드 생성
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    profile_image = models.ImageField(
        upload_to='profile_pics', # 임시 경로
        blank=True,
        null=True
    )
    medal_count = models.IntegerField(default=0)

class Team(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    invite_code = models.CharField(
        max_length=6,
        unique=True, # 코드 중복 불가
        default=generate_invite_code, # 팀 생성 시 자동 생성
    )
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('leader', '팀장'),
        ('member', '팀원')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

