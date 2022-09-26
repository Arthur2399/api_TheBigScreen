from django.urls import path
from survey.api import views
urlpatterns = [
    path('template/list', views.SurveyTemplateList.as_view(), name='Listar Plantillas'),
    path('template/update/<id>',views.SurveyTemplateUpdate.as_view(),name='actualizar Plantilla'),
    path('survey/usr',views.mobilSurvey.as_view(),name='Survey_usr'),
    path('survey/answer/<id>',views.postSurvey.as_view(),name='Survey_post'),
]

