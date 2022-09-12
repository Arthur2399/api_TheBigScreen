from datetime import date
from django.db import models
from user.models import User
from movies.models import Schedule,Branch,Timetable
# Create your models here.
class Awards(models.Model):
    name_award = models.CharField(max_length=255,unique=True)
    number_award=models.IntegerField()
    photo_award=models.ImageField(max_length=255,upload_to='awards/')
    class Meta:
        verbose_name = 'Award'
        verbose_name_plural = 'Awards'
    def __str__(self):
        return self.name_award

class Credits(models.Model):
    number_credits=models.IntegerField()
    user=models.OneToOneField(User,on_delete=models.RESTRICT,related_name='user_credits',null=False,blank=False)
    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    date_transaction = models.DateTimeField(auto_now_add=True)
    credits_translation=models.ForeignKey(Credits,on_delete=models.RESTRICT)
    total_cost=models.IntegerField()
    total_credits=models.IntegerField()
    balance=models.IntegerField()
    time_transaction=models.TimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
    def __str__(self):
        return self.credits_translation.user.username + " %s"%self.date_transaction
class TransactionDetail(models.Model):
    transaction_detail=models.ForeignKey(Transaction,on_delete=models.RESTRICT)
    awards_detail=models.ForeignKey(Awards,on_delete=models.RESTRICT)
    price=models.IntegerField()
    quantity=models.IntegerField()
    subtotal=models.IntegerField()
    class Meta:
        verbose_name = 'TransactionDetail'
        verbose_name_plural = 'TransactionDetails'
    def __str__(self):
        return self.transaction_detail.credits_translation.user.username + " %s"%self.transaction_detail.date_transaction

class Ticket(models.Model):
    name_user = models.CharField(max_length=255,blank=True,null=True)
    credits_ticket=models.ForeignKey(Credits,on_delete=models.RESTRICT,null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    date_functions=models.DateField()
    value=models.IntegerField(default=100)  
    totalcredit=models.IntegerField(null=True,blank=True)
    balance=models.IntegerField(null=True,blank=True)
    qrImage=models.ImageField(max_length=255,upload_to='qrticket/',null=True,blank=True)
    timetable_ticket=models.ForeignKey(Timetable,on_delete=models.RESTRICT)
    branch_ticket=models.ForeignKey(Branch,on_delete=models.RESTRICT,null=False,blank=False)
    state=models.IntegerField(default=1)
