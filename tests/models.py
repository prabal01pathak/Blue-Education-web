from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


dificulties = (('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'))

types = (('single', 'single'), ('write', 'write'),
         ('multiselect', 'multiselect'))

answer_choice = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))
exam_choice = (('JEE Mains','JEE Mains'),('NEET','NEET'),('PAT','PAT'),('GATE','GATE'))
marking_choice = (('0','0'),('1','1'),('2','2'),('3','3'),('4','4'))
minus_marking_choice = (('0','0'),('1','1'),('2','2'),('3','3'),('4','4'))

class Paper_Title(models.Model):
    Question_Paper_Title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=100,blank=True,choices=exam_choice,default='Jee')
    marking_scheme = models.CharField(max_length=200,blank=True,choices=marking_choice,default='0',help_text="assigned marks for every questions") 
    minus_marking_scheme = models.CharField(max_length=200,blank=True,choices=minus_marking_choice,default='0')
    scheduled_time = models.DateTimeField(blank=True,null=True,default=timezone.now)  
    end_time = models.DateTimeField(blank=True,null=True,default=timezone.now)  
    hidden = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    remove_live_minutes = models.IntegerField(default=15,blank=True)
    description = models.TextField(blank=True,default='')
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.Question_Paper_Title

class Title(models.Model):
    Question_Paper_Title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=100,blank=True,choices=exam_choice,default='Jee')
    marking_scheme = models.CharField(max_length=200,blank=True,choices=marking_choice,default='0',help_text="assigned marks for every questions") 
    minus_marking_scheme = models.CharField(max_length=200,blank=True,choices=minus_marking_choice,default='0')
    scheduled_time = models.DateTimeField(blank=True,null=True,default=timezone.now)  
    end_time = models.DateTimeField(blank=True,null=True,default=timezone.now)  
    hidden = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    remove_live_minutes = models.IntegerField(default=15,blank=True)
    description = models.TextField(blank=True,default='')

    def __str__(self):
        return self.Question_Paper_Title


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
    marking = models.FloatField(default=0,blank=True,help_text="assigned marks for this questions if same as title leave it.") 
    minus_marking = models.FloatField(default=0,blank=True,help_text="assigned negative marks for every questions if same as title leave it.") 
    answer = models.CharField(choices=answer_choice,default="A", max_length=100)
    explanation = models.TextField(default='None',blank=True)

    class Meta:
        abstract=True

    def __str__(self):
        return "Q.No: "+str(self.Q_No) +" "+  self.paper_title.Question_Paper_Title + " "  + self.description
    def name(self):
        return type(self).__name__

class Math(Questions):
    pass

class Chemistry(Questions):
    pass

class Physics(Questions):
    pass

class Biology(Questions):
    pass
class Agriculture(Questions):
    pass
class StudentData(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    paper = models.ForeignKey(Title, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0, blank=True)
    marks = models.IntegerField(default=0,blank=True)
    rank = models.IntegerField(default=0,blank=True)
    exam_data = models.TextField(default='None',blank=True)
    want_try_again = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=0,blank=True)  
    

    def __str__(self):
        return "User: "+self.user.username + ", Paper: "+self.paper.Queistion_Paper_Title 
