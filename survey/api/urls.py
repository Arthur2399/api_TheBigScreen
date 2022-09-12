from django.urls import path
from survey.api import views
urlpatterns = [
    path('template/list', views.SurveyTemplateList.as_view(), name='Listar Plantillas'),
    path('survey/usr',views.mobilSurvey.as_view(),name='Survey_usr'),
    path('survey/answer/<id>',views.postSurvey.as_view(),name='Survey_post'),
]