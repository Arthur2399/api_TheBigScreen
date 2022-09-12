from django.urls import include, path
from movies.api import views

urlpatterns = [
    #movies
    path('movies/list', views.Movies.as_view(), name='list movies'),
    path('movies/create', views.Movies.as_view(), name='create movies'),
    path('movies/nextPremiere', views.NextPremiere.as_view(), name='update movies'),
    path('movies/best', views.bestMovie.as_view(), name='Best'),
    path('movies/best5', views.bestMovie5.as_view(), name='Best'),

    #actors
    path('actors/list', views.Actors.as_view(), name='list actors'),
    #categories
    path('categories/list', views.Categories.as_view(), name='list categories'),
    #schedules
    path('schedules/list', views.ScheduleList.as_view(), name='list schedules'),
    path('schedules/create', views.ScheduleCreate.as_view(), name='list schedules'),
    #timetables
    path('timetables/list', views.TimetableList.as_view(), name='list timetables'),
    path('timetables/create', views.TimetableCreate.as_view(), name='list timetables'),
    #billboard
    path('billboard', views.Billboard.as_view(), name='list billboard'),
]