from django.urls import path
from reports.api import views
urlpatterns = [
    path("sale",views.report_sale.as_view()),
    path("survey",views.report_survey.as_view()),
    path("bar",views.reportGlobal.as_view()),
    path("bar/<id>",views.reportBranch.as_view()),
]