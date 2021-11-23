from django.db import models
from tests.models import *
from tinymce import models as tiny_models


"""
exam_choice = (("JEE Mains","JEE Mains"),("JEE Advanced","JEE Advanced"))
# Create your models here.
class JeePaperTitle(Paper_Title):
    exam_type = models.CharField(max_length=100,blank=True,choices=exam_choice,default='Jee')
    pass
class Math(Questions):
    paper_title = models.ForeignKey(JeePaperTitle, on_delete=models.CASCADE)
    pass
class Physics(Questions):
    paper_title = models.ForeignKey(JeePaperTitle, on_delete=models.CASCADE)
    pass
class Chemistry(Questions):
    paper_title = models.ForeignKey(JeePaperTitle, on_delete=models.CASCADE)
    pass
"""
class Topic(models.Model):
    title = models.CharField(max_length=100)
    Ano = tiny_models.HTMLField()
    some = models.TextField(blank=True,default="")
    def __str__(self):
        return self.title
