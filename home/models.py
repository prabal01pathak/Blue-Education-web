from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Normal(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    some = models.TextField(blank=True,default='')
