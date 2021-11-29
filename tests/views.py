from django.shortcuts import render, HttpResponse, redirect,reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import TestForm,FormFilter
from django.utils import timezone
import json
from django.apps import apps
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import tzlocal
from .forms import AddTitleForm,AddQuestionForm

subject_model_names = ['Math','Chemistry','Physics','Biology','Agriculture','Account','OperatingSystem','DBMS','DigitalElectronics','COA','ComputerNetworks','DataScience','CyberSecurity']# list of all subjects in the database 
# get time of database
def get_time():
    import datetime
    now = datetime.datetime.now()
    html = "Time: %s" % now
    return html



def terms(request):
    return render(request,'terms.html',{})

def check_answers(choice, model, marking, minus_marking):
    # check type of input question
    mark = 0
    right = 0
    total_attempted = 0
    if model.type == "write":
        answer = model.option1
    else:
        answer = model.answer

    # manipulate the marks based on answer given by student
    if choice != None and choice.lower() == answer.lower():
        total_attempted += 1
        if model.marking != 0:
            mark = model.marking
        else:
            mark += marking
        right += 1
    elif choice == None or choice == "":
        mark += 0
    else:
        total_attempted += 1
        if model.marking != 0:
            mark -= model.minus_marking
        else:
            mark -= minus_marking
    return mark, right,total_attempted


def get_object(title, subject):
    models = apps.get_models()
    try:
        for model in models:
            models_name = str(model.__name__)
            if models_name == subject:
                return model.objects.filter(paper_title=title),model

    except ObjectDoesNotExist:
        return []


def split_model_name(name):
    name = name.split('_')
    last_name = name[1]
    return last_name


def get_posted_datas(request, models_list, marking, minus_marking):
    marking = float(marking)
    minus_marking = float(minus_marking)
    choices = []
    rights = 0
    marks = 0
    datas = {}
    total_attempted_question=0
    for key in models_list.keys():
        model_data = models_list[key]['model_name']
        name = models_list[key]['name']
        i = 0
        for data in model_data:
            choice = request.POST.get(f"option_{name}{i+1}")
            choices.append(choice)
            model = data
            mark, right,total_attempted= check_answers(choice, model, marking, minus_marking)
            marks += mark
            rights += right
            total_attempted_question += total_attempted
            i += 1
        datas[name] = {
            'marks': marks,
            'rights': rights,
            'choices': choices,
            'total_attempted': total_attempted_question,
        }
        total_attempted_question = 0

        marks = 0
        rights = 0
        choices = []
        print('qeustion:' ,datas[name]['total_attempted'],name)
        print(datas)
    return datas


def get_marks_and_rights(data):
    marks = 0
    rights = 0
    for subjects, values in data.items():
        mark = values['marks']
        right = values['rights']
        marks += mark
        rights += right
    return marks, rights


def calculate_rank(title,user):
    students = StudentData.objects.filter(paper=title).order_by('-marks') # get all students of this title and order by marks 
    i =0
    for user_ in students:
        user_.rank = i+1
        user_.save()
        i += 1
    student = StudentData.objects.get(paper=title,user=user)
    return student.rank

#submit student feedback on student id
@login_required(login_url="user_auth:login")
def feedback_save(request):
    if request.method == "POST":
        print(request.POST.keys())
        title_id = request.POST['title_id']
        #get user
        user = User.objects.get(username=request.user)
        #get title
        title = Title.objects.get(id=int(title_id))
        print(title)
        #get student data
        student = StudentData.objects.get(user=request.user, paper=title)
        #save student data
        student.feedback = request.POST['feedback']
        student.save()
        print('done')
        #return response
        return redirect(reverse("user_auth:dashboard"))
    #return it if request is get
    return redirect(reverse("user_auth:dashboard"))


# exam page
@login_required(login_url="user_auth:login")
def index(request, title_id):
    time = timezone.now()
    print(request.COOKIES.keys())
    # get paper titles from database
    title = Title.objects.filter(id=title_id, hidden=False)

    # select first because title will return a list.
    title = title[0]

    # paper time details 
    endtime = title.end_time 
    server_end = title.end_time+timezone.timedelta(minutes=1)
    time_now = timezone.now()

    if time > server_end and title.is_live:
        context = {
            'title': 'Exam End',
            'data': '<h2>Exam Ended</h2>'
        }
        return render(request,'result.html',context)


    # get data of every subject from database
    models = {}
    models_list = {}


    #Append every new model subjects in subjects list.
    subjects =subject_model_names
    total_subject = 0
    total_marks = 0
    total_questions = 0
    subject_wise_total_questions = 0
    subjects_name = ""
    for subject in subjects:
        model,current_model_name = get_object(title, subject)
        if model != None and len(model) > 0:
            models_list[f"model_{subject}"] = {
                'model_name': model,
                'name': subject
            }
            total_marks_for_subject = 0
            subject_total_marks = {}
            for marks in model: 
                if marks.marking !=0:
                    total_marks_for_subject += marks.marking
                    total_marks +=marks.marking
                else:
                    total_marks_for_subject +=float(title.marking_scheme)
                    total_marks +=float(title.marking_scheme)
            subject_total_marks[model[0].name()] = total_marks_for_subject
            total_questions += len(model)
            total_subject +=1
            subject_wise_total_questions += len(model)
            subjects_name += f"{total_subject+2}. {model[0].name()} \t has Total of {subject_wise_total_questions} questions.<br>"
            subject_wise_total_questions =0

    #subject details 
    total_subject_marks = total_marks / total_subject
    #    "total_subject_marks": total_subject_marks,
    every_subject_questions = total_questions / total_subject
    subject_detail = {
        "total_marks": int(total_marks),
        "every_subject_questions":int(every_subject_questions),
        "total_subject_marks": int(total_subject_marks),
        'subjects_name': subjects_name,
        "subject_total_marks":subject_total_marks,
    }

    total_remaining_time = (endtime - title.scheduled_time).seconds
    remaining_minutes = int(total_remaining_time/60)
    context = {
        'title': title,
        'models_list': models_list,
        "end_time": endtime,
        "subject_detail":subject_detail,
        "nowTime": time,
        'remaining_time': remaining_minutes,
        'total_time':remaining_minutes,
    }


    if title.is_live:
        time_delay = ((time_now - title.scheduled_time).seconds)/60
        total_remaining_minutes = int(remaining_minutes - time_delay)
        context['remaining_time']=total_remaining_minutes
    #time of exam and submission

    if request.method == "POST":
        #get submitted time.
        time = timezone.now()
        if time >server_end and title.is_live:
            context = {
                'title': 'Exam End',
                'data': '<h2>Exam Ended</h2>'
            }
            return render(request,'result.html',context)
        try:
            # get database if exist and set marks and attempts
            student = StudentData.objects.get(user=request.user, paper=title)
        except StudentData.DoesNotExist:
            # create database if not exist
            student = StudentData.objects.create(
                user=request.user, paper=title,submitted_at=time) 

        if student.attempts >= 1 and title.is_live:
            title = 'resubmission'
            context = {
                'title':title,
                'data':"<h2>You have already submitted</h2>"
            }
            return render(request,'result.html',context)
        # get student total posted data
        exam_data = get_posted_datas(
            request, models_list, title.marking_scheme, title.minus_marking_scheme)

        total_marks, total_rights = get_marks_and_rights(exam_data)

        # caculate student rank

        student.exam_data = exam_data
        student.attempts += 1
        student.submitted_at = timezone.now()
        student.marks = total_marks
        student.save()
        rank = calculate_rank(title,request.user)
        # change data to show in result page.
        for choices in exam_data:
            context[choices] = exam_data[choices]
        context['student'] = student
        context['exam_data'] = exam_data
        context['total_marks'] = total_marks
        context['total_rights'] = total_rights
        context['rank'] = rank
        return render(request, 'index.html', context)
    return render(request, 'index.html', context)

# home page

# home view for user
#

"""
title = Title.objects.get(id=1)
for i in range(0,10):
    Physics.objects.create(paper_title=title,description="sldfjsldjfsldjfsdjfsdfjsldjfsdjfdsf",marking = 4,minus_marking=2)
    print(i)
    """

def home(requests):
    titles = Title.objects.filter(is_live=True,hidden=False).order_by('-scheduled_time')
    print(titles)
    now_time = timezone.now()
    for title in titles:
        end_time = title.end_time
        remove_live = title.remove_live_minutes
        remove_live_time = end_time + timezone.timedelta(minutes=remove_live)
        if now_time > remove_live_time:
            title.is_live = False
            title.save()
    total_title = Title.objects.filter(hidden=False,is_live=False).order_by('-scheduled_time')
    live_title = Title.objects.filter(hidden=False,is_live=True).order_by('-scheduled_time')
    is_live_titles=False
    if len(live_title) > 0:
        is_live_titles=True
    print(live_title)
    form = FormFilter()
    context = {
        'titles': total_title,
        'form': form,
        'live_titles':live_title,
        'is_live_titles':is_live_titles,
    }
    print(form)
    if requests.method=="POST":
        form = FormFilter(requests.POST)
        filter_type = requests.POST['exam_type']
        total_title = Title.objects.filter(exam_type=filter_type,hidden=False,is_live=False).order_by('-scheduled_time')
        live_title = Title.objects.filter(exam_type=filter_type,hidden=False,is_live=True).order_by('-scheduled_time')
        is_live_titles=False
        if len(live_title)>0:
            is_live_titles=True
        context['titles'] = total_title
        context['form'] = form
        context['live_titles']=live_title
        context['is_live_titles']=is_live_titles
        return render(requests,'home.html',context)
    return render(requests, 'home.html', context)

def filter_pages(request,filter_type):
    print(type(filter_type))
    if filter_type.lower()=="all":
        title = Title.objects.filter(hidden=False,is_live=False)
        live_title = Title.objects.filter(hidden=False,is_live=True)
    else:
        title = Title.objects.filter(hidden=False,is_live=False,exam_type=filter_type)
        live_title = Title.objects.filter(hidden=False,is_live=True,exam_type=filter_type)
    is_live_titles = False
    if len(live_title)>0:
        is_live_titles=True
    context = {
            'titles':title,
            'live_titles':live_title,
            'is_live_titles':is_live_titles,
            'head_title':f"{filter_type} Tests",
            }
    return  render(request,'tests/filter_type.html',context)

# list all available titles 
@login_required(login_url = "user_auth:login")
def show_title(request):
    # if user is not superuser redirect to home page 
    if  not request.user.is_superuser:
        return redirect(reverse('jeetests:home'))
    data = Title.objects.all()
    for subject in data:
        subjects = get_subjects_list(subject.subjects)
    
    context = {
            'data':data,
            }
    if request.method =="POST":
        action_to = request.POST.get("select_action")
        checkbox_title_list = []
        for i in range(0,len(data)):
            checkbox_title_id = request.POST.get(f"{data[i].id}") 
            if checkbox_title_id != None:
                checkbox_title_id = int(checkbox_title_id)
                checkbox_title_list.append(checkbox_title_id) 
        print(checkbox_title_list)
        print(action_to)
        if action_to.lower() == "delete":
            if len(checkbox_title_list) > 0:
                for j in checkbox_title_list:
                    current_title = Title.objects.get(id=j)
                    current_title.delete()
                    print('done')
            return render(request,'tests/show_title.html',context)
        return render(request,'tests/show_title.html',context)
    return render(request,'tests/show_title.html',context)


# add new title 
@login_required(login_url = "user_auth:login") 
def add_title(request):
    # if user is not superuser redirect to home page 
    if not request.user.is_superuser:
        return redirect(reverse('jeetests:home')) 
    form = AddTitleForm()
    context = {
        'form':form,
    }
    if request.method=="POST":
        form = AddTitleForm(request.POST)
        front_image = form.data.get('Front_image')
        print(front_image)
        if form.is_valid():
            front_image = form.cleaned_data['Front_image']
            print(front_image)
            form.save()
            title = Title.objects.all()
            title = title[len(title)-1]
            title.Front_image = front_image
            title.save()
            # redirect to show title page 
            return redirect(reverse('jeetests:show-title'))
    return render(request,'tests/add_title.html',context)

# edit title page 
@login_required(login_url = "user_auth:login") 
def edit_title(request,title_id):
    # if user is not superuser redirect to home page 
    if not request.user.is_superuser:
        return redirect(reverse('jeetests:home'))

    title_id= int(title_id)
    title = Title.objects.get(id=title_id)

    #convert stored string form subjects in list of subjects.
    title_subjects = get_subjects_list(title.subjects) 
    form = AddTitleForm(instance=title,initial={'Front_image':title.Front_image,'subjects':title_subjects}) 
    context = {
        'form':form,
        'title':title,
    }
    if request.method =="POST":
        form = AddTitleForm(request.POST)
        if form.is_valid():
            front_image= form.cleaned_data['Front_image']
            Question_Paper_Title = form.cleaned_data['Question_Paper_Title'] 
            exam_type = form.cleaned_data['exam_type'] 
            marking_scheme = form.cleaned_data['marking_scheme']
            minus_marking_scheme = form.cleaned_data['minus_marking_scheme']
            scheduled_time = form.cleaned_data['scheduled_time'] 
            end_time = form.cleaned_data['end_time']
            remove_live_minutes = form.cleaned_data['remove_live_minutes']
            hidden = form.cleaned_data['hidden']
            subjects = form.cleaned_data['subjects']
            is_live = form.cleaned_data['is_live']
            description = form.cleaned_data['description']
            title.front_image = front_image
            print(front_image)
            title.Question_Paper_Title = Question_Paper_Title 
            title.exam_type = exam_type
            title.marking_scheme = marking_scheme
            title.minus_marking_scheme = minus_marking_scheme
            title.scheduled_time = scheduled_time
            title.end_time = end_time
            title.remove_live_minutes = remove_live_minutes
            title.hidden = hidden
            title.subjects = subjects
            title.is_live = is_live
            title.description = description
            title.save()
            return redirect(reverse('jeetests:show-title'))
        return render(request,'tests/edit_title.html',context) 
    return render(request,'tests/edit_title.html',context)

def get_subjects_list(string_of_subjects):
    list_of_subjects = string_of_subjects.split('\'')
    subjects_list = []
    for i in range(0,len(list_of_subjects)):
        if ',' in list_of_subjects[i] or '[' in list_of_subjects[i] or ']' in list_of_subjects[i]: 
            continue
        else:
            subjects_list.append(list_of_subjects[i])
    return subjects_list

@login_required(login_url = "user_auth:login")
def get_subject(request,title_id):
    # if user is not superuser redirect to home page 
    if  not request.user.is_superuser:
        return redirect(reverse('jeetests:home'))
    title = Title.objects.get(id=title_id)
    subjects = title.subjects
    list_of_subjects = get_subjects_list(subjects)
    context = {
        'title':title,
        'subject_list':list_of_subjects,
    }
    return render(request,'tests/get_subject.html',context)

@login_required(login_url = "user_auth:login")
def add_questions(request,model,title_id):
    # if user is not superuser redirect to home page 
    if  not request.user.is_superuser:
        return redirect(reverse('jeetests:home'))
    title = Title.objects.get(id=title_id)
    get_questions ,current_model_name= get_object(title,model)
    get_questions = get_questions.order_by('Q_No')
    q_no = 1
    if len(get_questions) > 0:
        q_no = get_questions[len(get_questions)-1].Q_No+1
    form = AddQuestionForm({"Q_No":q_no,'marking':title.marking_scheme,'minus_marking':title.minus_marking_scheme})
    context = {
        'title':title,
        'questions': get_questions,
        'form':form,
        'model':model,
    }
    if request.method == "POST":
        form = AddQuestionForm(request.POST)

        # get questions for checkboxes to do validation and assign it to other model 
        if form.is_valid():
            question_no = form.cleaned_data['Q_No']
            description = form.cleaned_data['description']
            types = form.cleaned_data['type']
            option1 = form.cleaned_data['option1']
            option2 = form.cleaned_data['option2']
            option3 = form.cleaned_data['option3']
            option4 = form.cleaned_data['option4']
            answer = form.cleaned_data['answer']
            difficulty = form.cleaned_data['difficulty']
            explanation = form.cleaned_data['explanation']
            marking = form.cleaned_data['marking']
            minus_marking = form.cleaned_data['minus_marking']
            # create new questions on given subjects
            current_model_name.objects.create(
                                              paper_title= title,Q_No=question_no,
                                              description=description,
                                              type=types,
                                              option1=option1,
                                              option2=option2,
                                              option3=option3,
                                              option4=option4,
                                              answer=answer,
                                              difficulty=difficulty,
                                              explanation=explanation,
                                              marking=marking,
                                              minus_marking=minus_marking
                                              ) 
            return redirect(reverse('jeetests:show-question',kwargs={'model':model,'title_id':title_id})) 
        return render(request,'tests/add_questions.html',context)
    return render(request,'tests/add_questions.html',context)

@login_required(login_url = "user_auth:login")
def show_assign_or_delete(request,model,title_id):
    # if user is not superuser redirect to home page 
    if  not request.user.is_superuser:
        return redirect(reverse('jeetests:home'))
    title = Title.objects.get(id=title_id)
    total_titles = Title.objects.all()
    get_questions ,current_model_name= get_object(title,model)
    get_questions = get_questions.order_by('Q_No')
    q_no = 1
    if len(get_questions) > 0:
        q_no = get_questions[len(get_questions)-1].Q_No+1
    context = {
        'title':title,
        'questions': get_questions,
        'model':model,
        'available_subjects':subject_model_names,
        'titles':total_titles,
    }
    if request.method == "POST":
        checkbox_question_id = []
        for i in range(len(get_questions)):
            number_of_checkbox = request.POST.get(f"question{i+1}")
            if number_of_checkbox != None:
                checkbox_question_id.append(number_of_checkbox)
        
        selected_thing = {}
        for j in range(len(total_titles)):
            selected_title = request.POST.get(f"{total_titles[j].id}{j+1}")
            select_subject  = request.POST.get(f"subject{total_titles[j].id}")
            if selected_title != None and select_subject!=None:
                selected_thing[selected_title]=select_subject
        print(selected_thing.__len__())

        action = request.POST.get('do-action')
        if action.lower() == 'assign_to_other':
            if len(checkbox_question_id)>0:
                for question_id in checkbox_question_id:
                    print(selected_thing)
                    for title_id,subject_to in selected_thing.items():
                        title_id = int(title_id)
                        title_input = Title.objects.get(id=title_id)
                        model_data,new_model_name = get_object(title_id, subject_to)
                        available_queryset = new_model_name.objects.filter(paper_title=title_input).order_by("-Q_No")
                        #get question id
                        question_id = int(question_id)
                        question = current_model_name.objects.get(id=question_id)
                        question_no =  1
                        if len(available_queryset) > 0:
                            question_no = available_queryset[0].Q_No+1 
                        new_model_name.objects.create(
                                paper_title=title_input,
                                Q_No=question_no,
                                description=question.description,
                                type=question.type,
                                option1=question.option1,
                                option2=question.option2,
                                option3=question.option3,
                                option4=question.option4,
                                answer=question.answer,
                                difficulty=question.difficulty,
                                explanation=question.explanation, 
                                marking=title_input.marking_scheme,
                                minus_marking=title_input.minus_marking_scheme
                                ) 
            return redirect(reverse('jeetests:show-question',kwargs={'model':model,'title_id':title.id})) 
        if action.lower() =='delete':
            for i in checkbox_question_id:
                current_model_name.objects.get(id=int(i)).delete()
                print('done deleting')
            
            remaining_questions = current_model_name.objects.filter(paper_title=title).order_by("Q_No") 
            if len(remaining_questions) > 0:
                no = 1
                for q_no in range(len(remaining_questions)):
                    remaining_questions[q_no].Q_No = no
                    remaining_questions[q_no].save()
                    no +=1
            return redirect(reverse('jeetests:show-question',kwargs={'model':model,'title_id':title_id}))
        return redirect(reverse('jeetests:show-question',kwargs={'model':model,'title_id':title_id})) 
    return render(request,'tests/show_assign_or_delete.html',context)

    
    

# Edit question
@login_required(login_url = "user_auth:login")
def edit_question(request,question_id,model,title_id):
    # if user is not superuser redirect to home page 
    if  not request.user.is_superuser:
        return redirect(reverse('jeetests:home'))
    title = Title.objects.get(id=title_id)
    # it will return queryset and model_name of current_model_name
    get_model,current_model_name = get_object(title,model)
    model_name = get_model[0].name()
    #get that question to edit 
    question = current_model_name.objects.get(id=question_id)

    #form to edit question with it's data .
    form = AddQuestionForm({"Q_No":question.Q_No,
                            'marking':question.marking,
                            'minus_marking':question.minus_marking,
                            'description':question.description,
                            'option1':question.option1,
                            'option2':question.option2,
                            'option3':question.option3,
                            'option4':question.option4,
                            'answer':question.answer,
                            'difficulty':question.difficulty,
                            'type':question.type,
                            'explanation':question.explanation,
                            })
    context = {
        'title':title,
        'form':form,
        'question':question,
        'model_name':model_name,
    }
    if request.method=="POST":
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question_no = form.cleaned_data['Q_No']
            description = form.cleaned_data['description']
            types = form.cleaned_data['type']
            option1 = form.cleaned_data['option1']
            option2 = form.cleaned_data['option2']
            option3 = form.cleaned_data['option3']
            option4 = form.cleaned_data['option4']
            answer = form.cleaned_data['answer']
            difficulty = form.cleaned_data['difficulty']
            explanation = form.cleaned_data['explanation']
            marking = form.cleaned_data['marking']
            minus_marking = form.cleaned_data['minus_marking']
            question.Q_No = question_no
            question.description = description
            question.type = types
            question.option1 = option1
            question.option2 = option2
            question.option3 = option3
            question.option4 = option4
            question.answer = answer
            question.difficulty = difficulty
            question.explanation = explanation
            question.marking = marking
            question.minus_marking = minus_marking
            question.save()
            print('done')
            return redirect(reverse('jeetests:show-question',kwargs={'model':model,'title_id':title_id})) 
        return render(request,'tests/edit_question.html',context)
    return render(request,'tests/edit_question.html',context)



# contact page 
def contact_us(request):
    return render(request,'tests/contact_us.html',{})

# contact page message to admin
def message_send(request):
    if request.method=="POST":
        email  = request.POST['email']
        message = request.POST['message']
        return render(request,'tests/contact_us.html',{'post':True})
    return HttpResponse("Don't do that ")

# careers page 
def careers(request):
    return render(request,'tests/contact_us.html',{'careers':True})
# recomendation page
def recomend(request):
    return render(request,'tests/contact_us.html',{'recomend':True})
