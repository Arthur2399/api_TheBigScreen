from django.urls import path
from menu.api import views
urlpatterns = [
    path('menu', views.assignmentList.as_view(), name='Lista Menu User'),
]