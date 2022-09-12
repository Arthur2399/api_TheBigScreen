from django.db import models
from branch.models import Branch
# Create your models here.
class categories(models.Model):
    category_name = models.CharField(max_length=100,unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.category_name

class actors(models.Model):
    name_actor = models.CharField(max_length=255)
    photo_actor=models.ImageField(max_length=255,upload_to='actors/')
    
    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'
    def __str__(self):
        return self.name_actor

class movies(models.Model):
    name_movie=models.CharField(max_length=255,unique=True)
    description_movie=models.TextField(max_length=500)
    duration_movie=models.DurationField()
    premiere_date_movie=models.DateField()
    departure_date_movie=models.DateField()
    photo_movie=models.ImageField(max_length=255,upload_to='movies/')
    category_movie=models.ManyToManyField(categories,related_name='category_movie',blank=False)
    actor_movie=models.ManyToManyField(actors,related_name='actor_movie',blank=False)
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
    def __str__(self):
        return self.name_movie


class Schedule(models.Model):
    movies_schedule = models.ForeignKey(movies,on_delete=models.RESTRICT)
    branch_schedule = models.ForeignKey(Branch,on_delete=models.RESTRICT)
    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        unique_together = ('movies_schedule', 'branch_schedule')
    def __str__(self):
        return self.movies_schedule.name_movie + " " + self.branch_schedule.name_branch

class Timetable(models.Model):
    schedule_timetable = models.ForeignKey(Schedule,on_delete=models.RESTRICT)
    day_timetable = models.DateField()
    hour_timetable = models.TimeField()
    room=models.IntegerField()
    class Meta:
        verbose_name = 'Timetable'
        verbose_name_plural = 'Timetables'
        unique_together = ('day_timetable','hour_timetable','room')
    def __str__(self):
        return self.schedule_timetable.movies_schedule.name_movie