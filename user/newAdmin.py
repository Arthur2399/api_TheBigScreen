from user import models
from utils.random import get_random_string
from utils.crypt import encrypt
from utils.QrGenerator import Generator
from djcines.settings import DIR,EMAIL_HOST_USER
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
import getpass
from menu import models as menu_models
def SendNewAdmin(name,password,email):
    context={"name":name,"password":password}
    template = get_template('email.html')
    content=template.render(context)
    email=EmailMultiAlternatives(
        'Bienvenido a The Big Screen',
        'Bienvenida',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    return True

def newAdmin():
    first_name=None
    while (first_name==None or first_name==""):
        first_name=input("Ingrese el nombre del administrador: ")
    last_name=None
    while (last_name==None or last_name==""):
        last_name=input("Ingrese el apellido del administrador: ")
    email=None
    username=None
    while (email==None or email==""):
        email=input("Ingrese el correo del administrador: ")
        username=email
    ci=None
    while (ci==None or ci==""):
        ci=input("Ingrese la cedula del administrador: ")
    birth=None
    while (birth==None or birth==""):
        birth=input("Ingrese la fecha de nacimiento del administrador (yyyy-MM-dd): ")
    manual=input("Contraseña manual o aleatoria? (m/a): ")
    if manual=="m":
        password=None
        igual=False
        while not igual:
            print("Contraseña: ")
            password = getpass.getpass()
            print("")
            print("Confirmar contraseña: ")
            contraseña2 = getpass.getpass()
            if password == contraseña2:
                igual=True
            else:
                print("Contraseñas no coinciden")
    else:
        password=get_random_string(8)
    user=models.User()
    user.id=1
    user.first_name=first_name
    user.last_name=last_name
    user.email=email
    user.username=username
    user.set_password(password)
    user.save()
    cont_assignment=1
    for menus in menu_models.menu.objects.all():
        assignment=menu_models.assignment()
        assignment.id=cont_assignment
        assignment.user=user
        assignment.menu=menus
        assignment.save()
        cont_assignment+=1
    image=models.image()
    image.id=1
    image.user=user
    secret=encrypt(str(user.id))
    fil=str(user.id)+'.png'
    path="/qr/"
    Generator(secret,path,fil)
    image.rol_id=1
    image.image="users/admin.png"
    image.qrprofile=path+fil
    image.type="E"
    image.ci=ci
    image.birth=birth
    image.save()
    if manual!="m":
        message =SendNewAdmin(first_name+" "+last_name,password,email)
    return True