from operator import length_hint
from rest_framework import serializers
from user.models import image,User,role
from drf_extra_fields.fields import Base64ImageField
from utils.random import get_random_string
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import get_template
from djcines.settings import DIR,EMAIL_HOST_USER
from utils.QrGenerator import Generator
from utils.crypt import encrypt,decrypt
from menu import models as menu_models


class UserSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField(min_length=8,write_only=True)
    image=Base64ImageField(default="/users/user.png",use_url=True,max_length=None)
    
    def create(self,validate_data):
        instance=User()
        instance.first_name=validate_data.get('first_name')
        instance.last_name=validate_data.get('last_name')
        instance.username=validate_data.get('username')
        instance.email=validate_data.get('email')
        instance.set_password(validate_data.get('password'))
        instance.save()
        instanceimage=image()
        instanceimage.user=instance
        instanceimage.type='U'
        instanceimage.image=validate_data.get('image')
        instanceimage.save()
        return instance
    def validate_username(self,data):
        users= User.objects.filter(username=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error user":"Este nombre de usuario ya esta en uso"})
        else:
            return data
    def validate_email(self,data):
        users= User.objects.filter(email=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error email":"Este email ya esta en uso"})
        else:
            return data
    def validate_image(self,data):
        if data==None:
            data="/users/user.png"
        return data

def SendNew(name,password,email):
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
def qr(id):
        secret=encrypt(str(id))
        fil=str(id)+'.png'
        path="/qr/"
        Generator(secret,path,fil)
        imageupdate=image.objects.filter(user=id).update(qrprofile=path+fil)

def set_menu(user_id,rol_id):
    assign=menu_models.assignment.objects.filter(user_id=user_id)
    print(len(assign))
    if len(assign)>0:
        assign.delete()
    if rol_id==1 or rol_id==2:
        for menu in menu_models.menu.objects.all():
            assign=menu_models.assignment()
            assign.user_id=user_id
            assign.menu_id=menu.id
            assign.save()
    elif rol_id==3:
        assign=menu_models.assignment()
        assign.user_id=user_id
        assign.menu_id=6
        assign.save()
        assign2=menu_models.assignment()
        assign2.user_id=user_id
        assign2.menu_id=7
        assign2.save()
    elif rol_id==4:
        assign=menu_models.assignment()
        assign.user_id=user_id
        assign.menu_id=3
        assign.save()
    elif rol_id==5:
        assign=menu_models.assignment()
        assign.user_id=user_id
        assign.menu_id=4
        assign.save()
    return True

class EmployeeSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    image=Base64ImageField(required=True,max_length=None,use_url=True)
    rol_id=serializers.IntegerField()
    rol=serializers.CharField(read_only=True)
    ci=serializers.CharField(max_length=10)
    birth=serializers.DateField(format="%Y-%m-%d")
    branch_user=serializers.CharField(read_only=True)
    branch_user_id=serializers.IntegerField(write_only=True)
    password=serializers.CharField(default=get_random_string(8))
    def create(self,validate_data):
        instance=User()
        instance.first_name=validate_data.get('first_name')
        instance.last_name=validate_data.get('last_name')
        instance.username=validate_data.get('username')
        instance.email=validate_data.get('email')
        instance.set_password(validate_data.get('password'))
        instance.save()
        instanceimage=image()
        instanceimage.user=instance
        instanceimage.type='E'
        instanceimage.branch_user_id=validate_data.get('branch_user_id')
        instanceimage.image=validate_data.get('image')
        instanceimage.ci=validate_data.get('ci')
        instanceimage.rol_id=validate_data.get('rol_id')
        instanceimage.birth=validate_data.get('birth')
        instanceimage.save()
        set_menu(instance.id,validate_data.get('rol_id'))
        qr(instance.id)
        return instance
    def update(self,instance,validate_data):
        instance.first_name=validate_data.get('first_name',instance.first_name)
        instance.last_name=validate_data.get('last_name',instance.last_name)
        instance.username=validate_data.get('username',instance.username)
        instance.email=validate_data.get('email',instance.email)
        instance.save()
        instanceimage=image.objects.get(instance.id)
        instanceimage.type='E'
        instanceimage.branch_user_id=validate_data.get('branch_user_id',instanceimage.branch_user_id)
        instanceimage.image=validate_data.get('image',instanceimage.image)
        instanceimage.ci=validate_data.get('ci',instanceimage.ci)
        instanceimage.rol_id=validate_data.get('rol_id',instanceimage.rol_id)
        instanceimage.birth=validate_data.get('birth',instanceimage.rol_id)
        instanceimage.save()
        set_menu(instance.id,instanceimage.rol_id)
        return instance
    def validate_username(self,data):
        users= User.objects.filter(username=data)
        if len(users)!=0:
            raise serializers.ValidationError("Este nombre de usuario ya esta en uso")
        else:
            return data
    def validate_email(self,data):
        users= User.objects.filter(email=data)
        if len(users)!=0:
            raise serializers.ValidationError("Este email ya esta en uso")
        else:
            return data
    def validate_rol_id(self,data):
        rol=role.objects.filter(id=data)
        if len(rol)==0:
            raise serializers.ValidationError({"Error rol_id":"No existe este rol"})
        return data

class EmployeeSerializerUpdate(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    image=Base64ImageField(required=True,max_length=None,use_url=True)
    rol_id=serializers.IntegerField()
    ci=serializers.CharField(max_length=10)
    birth=serializers.DateField(format="%Y-%m-%d")
    branch_user=serializers.CharField(read_only=True)
    branch_user_id=serializers.IntegerField()
    def update(self,instance,validate_data):
        instance.first_name=validate_data.get('first_name',instance.first_name)
        instance.last_name=validate_data.get('last_name',instance.last_name)
        instance.username=validate_data.get('username',instance.username)
        instance.email=validate_data.get('email',instance.email)
        instance.save()
        instanceimage=image.objects.get(user=instance.id)
        instanceimage.type='E'
        instanceimage.branch_user_id=validate_data.get('branch_user_id',instanceimage.branch_user_id)
        instanceimage.image=validate_data.get('image',instanceimage.image)
        instanceimage.ci=validate_data.get('ci',instanceimage.ci)
        instanceimage.rol_id=validate_data.get('rol_id',instanceimage.rol_id)
        instanceimage.birth=validate_data.get('birth',instanceimage.rol_id)
        instanceimage.save()
        set_menu(instance.id,validate_data.get('rol_id'))
        return instance


class UserGetSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    image=serializers.CharField()

class PasswordSerializer(serializers.Serializer):
    password=serializers.CharField()
    new_password=serializers.CharField()
    confirm_password=serializers.CharField()
    def validate_new_password(self,data):
        if data==self.initial_data.get('password'):
            raise serializers.ValidationError({"Error password":"La contraseña nueva no puede ser igual a la anterior"})
        else:
            return data
    def validate_confirm_password(self,data):
        if data!=self.initial_data.get('new_password'):
            raise serializers.ValidationError({"Error password":"Las contraseñas no coinciden"})
        else:
            return data

class QRSerializer(serializers.Serializer):
    qr=serializers.CharField()
    
class rolSerializer(serializers.ModelSerializer):
    class Meta:
        model=role
        fields='__all__'