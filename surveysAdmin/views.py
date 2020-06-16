from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Survey, Question, Choice
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/survey-admin/login')
def index(request):
    surveys = Survey.objects.filter(enable_flag='True').count()
    users = User.objects.filter(is_staff=False).count()
    admin_users = User.objects.filter(is_staff=True).count()
    context = {
        'surveys_count': surveys,
        'users_count': users,
        'admin_users_count': admin_users
    }
    return render(request, "admin/index.html", context)


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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "admin/login.html", {"message": "Invalid credential", "form": form})
    else:
        form = forms.LoginForm(None)
    return render(request, "admin/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/survey-admin/login')
def user_view(request):
    users = User.objects.filter(is_staff=True).order_by('id')
    context = {
        'users': users
    }
    return render(request, "admin/admin_users/index.html", context)


@login_required(login_url='/survey-admin/login')
def user(request):
    users = User.objects.filter(is_staff=False).order_by('id')
    context = {
        'users': users
    }
    return render(request, "admin/users/index.html", context)


@login_required(login_url='/survey-admin/login')
def add_users(request):
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
            return render(request, "admin/admin_users/edit.html", context)
        else:
            user = User()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.username = request.POST["username"]
            user.password = make_password(request.POST["password"])
            if request.POST["is_superuser"] == 'yes':
                s = True
            else:
                s = False
            user.is_superuser = s
            user.is_staff = True
            user.save()
            message = "New account created successfully!"

            context = {
                'message': message
            }
            return render(request, "admin/admin_users/edit.html", context)
    else:
        return render(request, "admin/admin_users/edit.html")


@login_required(login_url='/survey-admin/login')
def edit_users(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == "POST":
        error_message = {}
        if User.objects.filter(email=request.POST["email"]).exclude(pk=user_id).exists():
            error_message['email'] = "Email already exist, please use different one or re-login"
        if User.objects.filter(username=request.POST["username"]).exclude(pk=user_id).exists():
            error_message['username'] = "Username already exist, please use different one or re-login"
        if request.POST["password"] != request.POST["confirm_password"]:
            error_message['password'] = "Password and Confirm Password didn't match, Please enter password carefully!"
        if request.POST["password"] and len(request.POST["password"]) < 6:
            error_message['password'] = "Password is to short, Password should be min 6 character"
        if request.POST["confirm_password"] and len(request.POST["confirm_password"]) < 6:
            error_message[
                'confirm_password'] = "Confirm Password is to short, Confirm Password should be min 6 character"
        # return HttpResponse(request.POST)

        if error_message:
            context = {
                'error_message': error_message,
                'form_data': user
            }
            return render(request, "admin/admin_users/edit.html", context)
        else:
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.username = request.POST["username"]
            if request.POST["password"]:
                user.password = make_password(request.POST["password"])

            if request.POST["is_superuser"] == 'yes':
                s = True
            else:
                s = False
            user.is_superuser = s
            user.is_staff = True
            user.save()
            message = "Account detail updated successfully!"

            context = {
                'message': message
            }
            return render(request, "admin/admin_users/edit.html", context)
    else:
        context = {
            'form_data': user
        }
        return render(request, "admin/admin_users/edit.html", context)


@login_required(login_url='/survey-admin/login')
def survey_view(request):
    surveys = Survey.objects.all().order_by('id')
    context = {
        'surveys': surveys
    }
    return render(request, "admin/surveys/index.html", context)


@login_required(login_url='/survey-admin/login')
def add_survey(request):
    if request.method == "POST":
        error_message = {}
        if not request.POST["title"]:
            error_message['title'] = "Title is required"
        if not request.POST["description"]:
            error_message['description'] = "Description is required"
        # return HttpResponse(error_message)

        if error_message:
            context = {
                'error_message': error_message,
                'form_data': request.POST
            }
            return render(request, "admin/surveys/edit.html", context)
        else:
            if request.POST.get("enable_flag"):
                enable_flag = True
            else:
                enable_flag = False
            survey = Survey()
            survey.title = request.POST["title"]
            survey.description = request.POST["description"]
            survey.enable_flag = enable_flag
            survey.save()
            message = "Survey Created Successfully"
            context = {
                'message': message
            }
            return render(request, "admin/surveys/edit.html", context)
    else:
        return render(request, "admin/surveys/edit.html")


@login_required(login_url='/survey-admin/login')
def edit_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    if request.method == "POST":
        error_message = {}
        if not request.POST["title"]:
            error_message['title'] = "Title is required"
        if not request.POST["description"]:
            error_message['description'] = "Description is required"
        # return HttpResponse(error_message)

        if error_message:
            context = {
                'error_message': error_message,
                'form_data': request.POST
            }
            return render(request, "admin/surveys/edit.html", context)
        else:
            if request.POST.get("enable_flag"):
                enable_flag = True
            else:
                enable_flag = False

            survey.title = request.POST["title"]
            survey.description = request.POST["description"]
            survey.enable_flag = enable_flag
            survey.save()
            message = "Survey Updated Successfully"
            context = {
                'message': message
            }
            return render(request, "admin/surveys/edit.html", context)
    else:
        context = {
            'form_data': survey
        }
        return render(request, "admin/surveys/edit.html", context)


@login_required(login_url='/survey-admin/login')
def delete_survey(request):
    survey_id = request.POST["survey_id"]
    Survey.objects.filter(id=survey_id).delete()
    return redirect('surveys')


@login_required(login_url='/survey-admin/login')
def question(request, survey_id):
    questions = Question.objects.filter(survey_id=survey_id)
    context = {
        'survey_id': survey_id,
        'questions': questions
    }
    return render(request, "admin/surveys/question/index.html", context)


@login_required(login_url='/survey-admin/login')
def add_question(request, survey_id):
    if request.method == "POST":
        error_message = {}
        if not request.POST["question"]:
            error_message['title'] = "Question is required"
            if error_message:
                context = {
                    'error_message': error_message,
                    'form_data': request.POST,
                    'survey_id': survey_id
                }
            return render(request, "admin/surveys/question/edit.html", context)
        else:

            question = Question()
            question.question = request.POST["question"]
            question.survey_id = survey_id
            question.type = request.POST["type"]
            question.save()
            if request.POST.get("type") == 'checkbox' or request.POST.get("type") == 'radio':
                for c in request.POST.getlist("options[]"):
                    choice = Choice()
                    if c:
                        choice.choice = c
                        choice.question_id = question.id
                        choice.save()

            message = "Question Created Successfully"
            context = {
                'message': message,
                'survey_id': survey_id
            }
            return render(request, "admin/surveys/question/edit.html", context)
    context = {
        'survey_id': survey_id
    }
    return render(request, "admin/surveys/question/edit.html", context)


@login_required(login_url='/survey-admin/login')
def edit_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    choices = ''
    options = ''
    if question.type != 'text':
        choices = Choice.objects.filter(question_id=question.id)

    if request.method == "POST":
        error_message = {}
        if not request.POST["question"]:
            error_message['title'] = "Question is required"
            if error_message:
                context = {
                    'error_message': error_message,
                    'form_data': request.POST,
                    'choices': choices,
                    'survey_id': question.survey_id,
                    'options': range(1, (5 - choices.count()) + 1)
                }
            return render(request, "admin/surveys/question/edit.html", context)
        else:

            question.question = request.POST["question"]
            question.type = request.POST["type"]
            question.save()
            if request.POST.get("type") == 'checkbox' or request.POST.get("type") == 'radio':
                Choice.objects.filter(question_id=question_id).delete()
                for c in request.POST.getlist("options[]"):
                    choice = Choice()
                    if c:
                        choice.choice = c
                        choice.question_id = question.id
                        choice.save()

            message = "Question Updated Successfully"
            if question.type != 'text':
                choices = Choice.objects.filter(question_id=question.id)
            context = {
                'message': message,
                'survey_id': question.survey_id,
                'form_data': question,
                'choices': choices,
                'options': range(1, (5 - choices.count()) + 1)
            }
            return render(request, "admin/surveys/question/edit.html", context)

    context = {
        'survey_id': question.survey_id,
        'form_data': question,
        'choices': choices,
        'options': range(1, (5 - choices.count()) + 1)
    }
    return render(request, "admin/surveys/question/edit.html", context)


@login_required(login_url='/survey-admin/login')
def delete_question(request):
    question_id = request.POST["question_id"]
    survey_id = request.POST["survey_id"]
    Question.objects.filter(id=question_id).delete()

    return redirect('question', survey_id)


@login_required(login_url='/survey-admin/login')
def delete_user(request):
    user_id = request.POST["user_id"]
    User.objects.filter(id=user_id).delete()

    return redirect('users')


@login_required(login_url='/survey-admin/login')
def delete_user_n(request):
    user_id = request.POST["user_id"]
    User.objects.filter(id=user_id).delete()

    return redirect('user')
