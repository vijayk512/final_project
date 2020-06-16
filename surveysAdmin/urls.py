from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("users", views.user_view, name="users"),
    path("users/add", views.add_users, name="add_users"),
    path("users/edit/<int:user_id>", views.edit_users, name="edit_users"),
    path("surveys", views.survey_view, name="surveys"),
    path("surveys/add", views.add_survey, name="add_survey"),
    path("surveys/edit/<int:survey_id>", views.edit_survey, name="edit_survey"),
    path("surveys/delete", views.delete_survey, name="delete_survey"),
    path("surveys/<int:survey_id>/question", views.question, name="question"),
    path("surveys/<int:survey_id>/question/add", views.add_question, name="add_question"),
    path("surveys/question/edit/<int:question_id>", views.edit_question, name="edit_question"),
    path("surveys/question/delete", views.delete_question, name="delete_question"),
    path("users/delete", views.delete_user, name="delete_user"),
    path("users/delete", views.delete_user_n, name="delete_user_n"),
    path("user", views.user, name="user"),
]
