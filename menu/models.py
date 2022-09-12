from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class menu(models.Model):
    name=models.CharField(max_length=100)
    path=models.CharField(max_length=100)
    class Meta:
        verbose_name='Menu'
        verbose_name_plural='Menus'
    def __str__(self):
        return self.name
class assignment(models.Model):
    menu=models.ForeignKey(menu,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        verbose_name='assignment'
        verbose_name_plural='assignments'
    def __str__(self):
        return self.menu.name+'-'+self.user.username