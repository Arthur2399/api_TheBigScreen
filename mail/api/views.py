from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from mail.api.serializable import emailSerializer, settingsSerializable
from djcines.settings import DIR,EMAIL_HOST_USER
from utils.random import get_random_string



def getInfo(name,password,email):
    context={"name":name,"password":password}
    template = get_template('email.html')
    content=template.render(context)
    email=EmailMultiAlternatives(
        'Cambio de contraseña The Big Screen',
        'Cambio Contraseña',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    return True


class returnPassword(APIView):
    def post(self,request):
        serializer=emailSerializer(data=request.data)
        if serializer.is_valid():
            user=User.objects.filter(email=serializer.data['email']).first()
            if user:
                print(user.username)
                password=get_random_string(8)
                print(password)
                user.set_password(password)
                user.save()
                message = getInfo(user.first_name+" "+user.last_name,password,user.email)
                return Response("Correo enviado",status=status.HTTP_201_CREATED)
            return Response("No existe el correo",status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)

class settings(APIView):
    def post(self,request):
        serializer=settingsSerializable(data=request.data)
        if serializer.is_valid():
            save_path=DIR+"djcines/.env"
            with open(save_path, 'w') as f:
                f.write("EMAIL_HOST="+request.data['EMAIL_HOST']+"\n")
                f.write("EMAIL_HOST_USER="+request.data['EMAIL_HOST_USER']+"\n")
                f.write("EMAIL_HOST_PASSWORD="+request.data['EMAIL_HOST_PASSWORD']+"\n")
                f.write("RECIPIENT_ADDRESS="+request.data['RECIPIENT_ADDRESS']+"\n")
            return Response("ok",status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
