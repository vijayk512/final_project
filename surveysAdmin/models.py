from django.db import models

# Create your models here.


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    enable_flag = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    survey_id = models.CharField(max_length=20)
    question = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    question_id = models.CharField(max_length=20)
    choice = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    question_id = models.CharField(max_length=10)
    choice = models.CharField(max_length=200)
    user_id = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)