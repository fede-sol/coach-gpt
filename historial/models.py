from django.db import models
from django.contrib.auth.models import User

class CoachedUser(models.Model):
    phone_number = models.CharField(max_length=20)

class CoachedUserIntro(models.Model):
    user = models.ForeignKey(CoachedUser, on_delete=models.CASCADE)
    user_intro = models.TextField()

class UserConsciousness(models.Model):
    user = models.ForeignKey(CoachedUser, on_delete=models.CASCADE)
    consciousness = models.TextField()

class UserConsult(models.Model):
    user = models.ForeignKey(CoachedUser, on_delete=models.CASCADE)
    consult = models.TextField()

class ConsultAnswer(models.Model):
    consult = models.ForeignKey(UserConsult, on_delete=models.CASCADE)
    answer = models.TextField()