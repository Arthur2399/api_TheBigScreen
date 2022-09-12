from django.db import models

# Create your models here.
class Branch(models.Model):
    name_branch = models.CharField(max_length=100,verbose_name="Nombre de la sucursal")
    address_branch = models.CharField(max_length=100,verbose_name="Dirección de la sucursal")
    phone_branch = models.CharField(max_length=30,blank=True,null=True,verbose_name="Teléfono de la sucursal")
    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
    def __str__(self):
        return self.name_branch