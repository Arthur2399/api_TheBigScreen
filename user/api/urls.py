from django.urls import include, path
from user.api import views
from rest_framework.authtoken import views as token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    path('createu', views.usersNew.as_view(), name='Crear Usuario Mobil'),
    path('createe',views.EmployeeNew.as_view(), name='Crear Empleado'),
    path('liste',views.EmployeeList.as_view(), name='Listar Empleados'),   
    path('user',views.UserProfile.as_view(), name='Datos de Usuario'),
    path('employee',views.EmployeeProfile.as_view(), name='Datos de Empleado'),
    path('lastemployee',views.LastEmployee.as_view(), name='Ultimo Empleado'),
    path('example', views.ExampleView.as_view(), name='Prueba'),
    path('loginU', views.LoginMovil.as_view(), name='login Usuario Movil'),
    path('loginE', views.LoginWeb.as_view(), name='login Empleado Web'),
    #basic token
    path('api-token-auth', token.obtain_auth_token),
    path('changepassword', views.ChangePassword.as_view(), name='Cambiar Contraseña'),
    path('web/user',views.WebMovilUSer.as_view(), name='Datos de Usuario Web'),
    #rol
    path('rol/list',views.RolList.as_view(), name='Listar Roles'),
    #jwt token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]