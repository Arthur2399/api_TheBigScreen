from django.db import models
from django.contrib.auth.models import User
from branch.models import Branch

class role(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    class meta:
        verbose_name="Role"
        verbose_name_plural="Roles"
    def __str__(self):
        return self.name


class image(models.Model):
    user=models.OneToOneField(User,on_delete=models.RESTRICT,unique=True,null=False,blank=False)
    image=models.ImageField(upload_to='users/')
    qrprofile=models.ImageField(upload_to='qr/',blank=True,null=True)
    type=models.CharField(max_length=1)
    branch_user=models.ForeignKey(Branch,on_delete=models.RESTRICT,null=True,blank=True)
    rol=models.ForeignKey(role,on_delete=models.RESTRICT,null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    ci=models.CharField(verbose_name="Cedula Identificacion",blank=True,null=True,max_length=10)
    birth=models.DateField(verbose_name="Fecha de Nacimiento",blank=True,null=True)
    class meta:
        verbose_name='Image'
        verbose_name_plural='Images'
    def __str__(self):
        return self.user.username