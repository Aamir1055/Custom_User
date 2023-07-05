# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from api_app.managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractUser):
    username = None
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    email = models.EmailField('email address', primary_key = True,unique= True,blank=False)
    phnum = models.CharField('phone number', max_length = 80)
    
    id =models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserDetails(models.Model):
    id = models.IntegerField(primary_key = True, editable=False)
    age = models.CharField(max_length = 200, blank = True)
    dob = models.CharField(max_length = 200, blank = True)
    profession = models.CharField(max_length = 200, blank = True)
    address = models.CharField(max_length = 200, blank = True)
    hobby = models.CharField(max_length = 200, blank = True)
    user_email = models.ForeignKey('CustomUser', on_delete = models.CASCADE, blank = True, null = True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.user_email}({self.id})'