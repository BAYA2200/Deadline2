from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    date_birth = models.DateField(null=True, blank=True)
    place_residence = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
