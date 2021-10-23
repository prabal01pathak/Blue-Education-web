from django.db import models
from django.contrib.auth.models import User

# Create your models here.

gender = (('Male',"Male"),("Female","Female"),("Other","Other"))
class UserExtraData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=14)
    gender = models.CharField(max_length=10,choices=gender,default=gender[0][0])
    accept_terms = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
