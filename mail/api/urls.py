from django.urls import include, path
from mail.api import views

urlpatterns = [
    path('settings', views.settings.as_view(), name='settings'),
    path('Changepassword', views.returnPassword.as_view(), name='password'),
]