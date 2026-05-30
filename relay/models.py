from django.db import models
from home.models import User, Team

class Relay(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal = models.CharField(max_length=200)
    days_per_runner = models.IntegerField(default=3)
    started_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    consecutive_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team.name} - {self.goal}"

class RelaySlot(models.Model):
    STATUS_CHOICES = [
        ('waiting', '바톤 대기 중'),
        ('running', '수행 중'),
        ('done', '바톤터치 완료'),
        ('sos', 'SOS 발동'),
    ]
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    runner = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_rescue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.relay} - {self.order}번째 주자 {self.runner.nickname}"

class Certification(models.Model):
    slot = models.ForeignKey(RelaySlot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='certifications/')
    certified_at = models.DateTimeField(auto_now_add=True)
    day_number = models.IntegerField()  

    def __str__(self):
        return f"{self.slot} - {self.day_number}일차 인증"