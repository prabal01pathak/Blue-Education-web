from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(Person,through="Membership")

class Membership(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)