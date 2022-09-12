from django.urls import include, path
from points.api import views

urlpatterns = [
    #Ticket
    path('ticket/create', views.CreateTicket.as_view(), name='create ticket'),
    path('ticket/read', views.ReadTicket.as_view(), name='read ticket'),
    path('ticket/survey',views.template.as_view(),name='survey'),
    #Awards
    path('awards/list', views.AwardsList.as_view(), name='awards list'),
    path('awards/create', views.AwardsCreate.as_view(), name='awards create'),
    #Transaction
    path('transaction/create', views.TransactionCreate.as_view(), name='transaction create'),
    path('transaction/prueba',views.prueba.as_view(),name="Prueba")
]