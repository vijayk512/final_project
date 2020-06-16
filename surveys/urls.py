from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index_user"),
    path("login", views.login_view, name="login_user"),
    path("logout", views.logout_view, name="logout_user"),
    path("register", views.register_view, name="register_user"),
    path("start/<int:survey_id>", views.survey_view, name="start"),
    path("next_question/<int:survey_id>/<int:question_id>", views.next_question, name="next_question"),
    path("thankyou", views.thank_you, name="thank_you"),

]