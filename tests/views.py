from django.shortcuts import render, HttpResponse,redirect
from .models import  Title,StudentData,Math,Chemistry,Physics 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #, UserChangeForm 
from django.contrib.auth import authenticate, login
from .forms import TestForm
from django.utils import timezone
import json




#get time of database
def get_time():
    import datetime
    now = datetime.datetime.now()
    html = "Time: %s" % now
    return html



counter = 0
def check_answers(choice,model):
    #check type of input question
    mark=0
    right = 0
    if model.type == "write":
        answer=model.option1
    else:
        answer = model.answer

    # manipulate the marks based on answer given by student
    if choice != None and choice.lower() == answer.lower():
        mark += 4
        right+=1
    elif choice == None or choice == "":
        mark += 0
    else:
        mark -= 1
    return mark,right


# exam page
@login_required(login_url="user_auth:login")
def index(request, title_id):
    time = get_time()
    #get paper titles from database
    title = Title.objects.filter(id=title_id, hidden=False)

    #select first if multiple titles
    title = title[0]

    #get data of every subject from database
    model_mh = Math.objects.filter(paper_title=title)
    model_ch = Chemistry.objects.filter(paper_title=title)
    model_ph = Physics.objects.filter(paper_title=title)

    #get wholde question paper from database
    form = TestForm()
    context = {
        'title': title,
        'model_mh': model_mh,
        'model_ch': model_ch,
        'model_ph': model_ph,
    }
    if request.method == "POST":
        try:
            #get database if exist and set marks and attempts
            student = StudentData.objects.get(user=request.user,paper=title) 
        except:
            #create database if not exist
            student = StudentData.objects.create(user=request.user, marks=marks,paper=title)  

        if student.attempts >=1 and title.is_live:
            return HttpResponse("you have already submitted")
        # looping through all the questions in the database
        student.answers = " "

        # choices for math in student database
        choices_mh = []
        marks = 0
        right =0
        for i in range(0, len(model_mh)):
            #get data from user form.
            choice_mh = request.POST.get(f"option_mh{i+1}")
            #append answer to the student's answer
            choices_mh.append(choice_mh)

            # get answer form database
            model = model_mh[i]
            mark,rights = check_answers(choice_mh,model)
            right +=rights
            marks += mark
        math_marks = marks
        math_right = right
        

        #same as math
        # choices for chemistry
        marks=0
        right =0
        choices_ch = []
        for i in range(0, len(model_ch)):
            choice_ch = request.POST.get(f"option_ch{i+1}")
            choices_ch.append(choice_ch)
            model = model_ch[i]
            mark,rights = check_answers(choice_ch,model)
            right +=rights
            marks += mark
        chemistry_marks = marks
        chemistry_right = right


        #same as math
        # choices for physics
        marks=0
        right =0
        choices_ph= []
        for i in range(0, len(model_ph)):
            choice_ph = request.POST.get(f"option_ph{i+1}")
            choices_ph.append(choice_ph)
            model = model_ph[i]
            mark,rights = check_answers(choice_ph,model)
            right +=rights
            marks += mark
        physics_marks = marks
        physics_right = right

        # add marks and attempts to database and show the result page .
        total_marks = math_marks+physics_marks+chemistry_marks
        total_right = math_right+physics_right+chemistry_right
        student.marks = str(total_marks)
        student.math_score = math_marks
        student.chemistry_score = chemistry_marks
        student.physics_score = physics_marks
        student.attempts += 1
        student.submitted_at = timezone.now()
        student.save()
        # change data to show in result page.
        context['marks']= total_marks
        context['student'] =  student
        context['math_marks']= math_marks
        context['math_right']=math_right
        context['physics_marks']= physics_marks
        context['chemistry_marks']= chemistry_marks
        context['choices_mh'] = choices_mh
        context['choices_ch'] = choices_ch
        context['choices_ph'] = choices_ph
        context['chemistry_right']=chemistry_right
        context['physics_right']=physics_right
        context['right'] = total_right
        return render(request, 'index.html', context)
    return render(request, 'index.html', context)

# home page

# home view for user
def home(requests):
    titles = Title.objects.filter(hidden=False)
    context = {
        'titles': titles,
    }
    return render(requests, 'home.html', context)
