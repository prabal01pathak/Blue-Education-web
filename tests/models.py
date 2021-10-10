from django.db import models
from django.contrib.auth.models import User

# Create your models here.


dificulties = (('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'))

types = (('single', 'single'), ('write', 'write'),
         ('multiselect', 'multiselect'))

answer_choice = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))
exam_choice = (('Jee','Jee'),('Neet','Neet'))


class Title(models.Model):
    Queistion_Paper_Title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=100,blank=True,choices=exam_choice,default='Jee')
    hidden = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.Queistion_Paper_Title+" "+self.exam_type


class Questions(models.Model):
    paper_title = models.ForeignKey(Title, on_delete=models.CASCADE)
    Q_No = models.IntegerField(default=0,help_text="increament every time for unique paper type")
    description = models.TextField()
    type = models.CharField(max_length=20, choices=types, default='single',help_text="Please enter your answerin option1 for write type questions")
    option1 = models.CharField(max_length=500, blank=True)
    option2 = models.CharField(max_length=500, blank=True)
    option3 = models.CharField(max_length=500, blank=True)
    option4 = models.CharField(max_length=500, blank=True)
    difficulty = models.CharField(
        max_length=100, choices=dificulties, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer = models.CharField(choices=answer_choice,default="A", max_length=100)
    explanation = models.TextField(default='None',blank=True)

    class Meta:
        abstract=True

    def __str__(self):
        return "Q.No: "+str(self.Q_No) +" "+  self.paper_title.Queistion_Paper_Title + " "  + self.description

class Math(Questions):
    pass

class Chemistry(Questions):
    pass

class Physics(Questions):
    pass

class StudentData(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    paper = models.ForeignKey(Title, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0, blank=True)
    marks = models.CharField(max_length=200, default=0, blank=True)
    math_score = models.IntegerField(blank=True,default=0)
    chemistry_score = models.IntegerField(blank=True,default=0)
    physics_score = models.IntegerField(blank=True,default=0)
    want_try_again=models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=0)  
    

    def __str__(self):
        return "User: "+self.user.username + ", Paper: "+self.paper.Queistion_Paper_Title +", Marks: "+self.marks
