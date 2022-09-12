from django.urls import include, path
from branch.api import views
urlpatterns = [
    path('list', views.ListBranch.as_view(), name='Lista de Sucursales'),
    path('create',views.CreateBranch.as_view(), name='Crear Sucursal'),
]