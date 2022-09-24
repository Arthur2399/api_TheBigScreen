from tabnanny import verbose
from django.db import models
from movies.models import movies
from django.contrib.auth.models import User
# Create your models here.
class Survey_template(models.Model):
    name=models.CharField(max_length=100)
    date_start=models.DateField(auto_now_add=True)
    date_final=models.DateField(null=True, blank=True)
    state=models.IntegerField(default=1)
    question1=models.CharField(max_length=255)
    question2=models.CharField(max_length=255)
    question3=models.CharField(max_length=255)
    question4=models.CharField(max_length=255)
    question5=models.CharField(max_length=255)
    def __str__(self):
        return self.name
        

class Survey(models.Model):
    suervey_template=models.ForeignKey(Survey_template, on_delete=models.RESTRICT)
    question1=models.CharField(max_length=255)
    question2=models.CharField(max_length=255)
    question3=models.CharField(max_length=255)
    question4=models.CharField(max_length=255)
    question5=models.CharField(max_length=255)
    movies=models.ForeignKey(movies, on_delete=models.RESTRICT)
    user_id=models.ForeignKey(User, on_delete=models.RESTRICT)
    date=models.DateField(auto_now_add=True)
    answer1=models.IntegerField(default=0)
    answer2=models.IntegerField(default=0)
    answer3=models.IntegerField(default=0)
    answer4=models.IntegerField(default=0)
    answer5=models.CharField(max_length=100,default="")
    branch=models.ForeignKey('branch.Branch', on_delete=models.RESTRICT)
    status=models.IntegerField(default=1)
    class Meta:
        verbose_name='Survey'
        verbose_name_plural='Surveys'
    def __str__(self):
        return self.user_id.username + ' ' + self.movies.name_movie

class Options(models.Model):
    value=models.CharField(max_length=255)
    class Meta:
        verbose_name='Option'
        verbose_name_plural='Options'
