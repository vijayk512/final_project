from django.http import HttpResponse
from django.shortcuts import render, redirect
from surveysAdmin.models import Survey, Question, Choice, Answer
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.


@login_required(login_url='/survey/login')
def index(request):
    surveys = Survey.objects.filter(enable_flag=True)
    context = {
        'surveys': surveys
    }
    return render(request, "feedback/index.html", context)


def login_view(request):
    if request.method == "POST":
        #  created a form in form.py file for login
        form = forms.LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        #  it's match the username and password.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index_user")
        else:
            return render(request, "feedback/login.html", {"message": "Invalid credential", "form": form})
    else:
        form = forms.LoginForm(None)
    return render(request, "feedback/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        error_message = {}
        if User.objects.filter(email=request.POST["email"]).exists():
            error_message['email'] = "Email already exist, please use different one or re-login"
        if User.objects.filter(username=request.POST["username"]).exists():
            error_message['username'] = "Username already exist, please use different one or re-login"
        if request.POST["password"] != request.POST["confirm_password"]:
            error_message['password'] = "Password and Confirm Password didn't match, Please enter password carefully!"
        if len(request.POST["password"]) < 6:
            error_message['password'] = "Password is to short, Password should be min 6 character"
        if len(request.POST["confirm_password"]) < 6:
            error_message[
                'confirm_password'] = "Confirm Password is to short, Confirm Password should be min 6 character"
        # return HttpResponse(request.POST)

        if error_message:
            context = {
                'error_message': error_message,
                'form_data': request.POST
            }
            return render(request, "feedback/register.html", context)
        else:
            user = User()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.username = request.POST["username"]
            user.password = make_password(request.POST["password"])
            user.is_superuser = False
            user.is_staff = False
            user.save()
            message = "New account created successfully! Please proceed for login"

            context = {
                'message': message
            }
            return render(request, "feedback/register.html", context)
    else:
        return render(request, "feedback/register.html")


@login_required(login_url='/survey/login')
def logout_view(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='/survey/login')
def survey_view(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    question = Question.objects.filter(survey_id=survey_id).order_by('id')[0:1]
    choices = ''
    question_id = Question.objects.filter(survey_id=survey_id).exclude(id=question[0].id).order_by('id')[0:1]
    if question[0].type != 'text':
        choices = Choice.objects.filter(question_id=question[0].id)
    if not question_id:
        q_id = 0
    else:
        q_id = question_id[0].id

    context = {
        'survey': survey,
        'questions': question,
        'question_id': q_id,
        'choices': choices,
        'c_q_id': question[0].id
    }
    return render(request, "feedback/survey.html", context)


@login_required(login_url='/survey/login')
def next_question(request, survey_id, question_id):
    survey = Survey.objects.get(pk=survey_id)
    choices = ''
    q_id = Question.objects.filter(id__gt=question_id).order_by("id")[0:1]
    if not q_id:
        q_id = 0
    else:
        q_id = q_id[0].id
    question = Question.objects.filter(id=question_id)
    if question[0].type != 'text':
        choices = Choice.objects.filter(question_id=question[0].id)

    if request.method == "POST":
        answer = Answer()
        answer.question_id = question_id
        answer.user_id = request.user.id
        answer.choice = request.POST.get("choice")
        answer.save()
        if not q_id:
            return redirect('thank_you')
        else:
            message = "Thank you for submitting your opinion, please process to next question."
            context = {
                'survey': survey,
                'questions': question,
                'question_id': q_id,
                'choices': choices,
                'message': message,
                'c_q_id': question[0].id
            }
            return render(request, "feedback/survey.html", context)
    context = {
        'survey': survey,
        'questions': question,
        'question_id': q_id,
        'choices': choices,
        'c_q_id': question[0].id
    }
    return render(request, "feedback/survey.html", context)


@login_required(login_url='/survey/login')
def thank_you(request):
    return render(request, "feedback/thankyou.html")
