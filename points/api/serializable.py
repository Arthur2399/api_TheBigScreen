from rest_framework import serializers
from points import models
from drf_extra_fields.fields import Base64ImageField
from djcines.settings import DIR,os
class TicketsSerializers(serializers.ModelSerializer):
    timetable_ticket_id=serializers.IntegerField()
    timetable_ticket=serializers.CharField(read_only=True)
    value=serializers.IntegerField(default=100)
    date_functions=serializers.DateField(required=False)
    branch_ticket=serializers.IntegerField(Required=False)
    class Meta:
        model = models.Ticket
        fields = '__all__'

class ReadTicketsSerializable(serializers.Serializer):
    qr=serializers.CharField(max_length=255)

class AwardsSerializable(serializers.ModelSerializer):
    photo_award=Base64ImageField(max_length=None,use_url=True)
    class Meta:
        model = models.Awards
        fields = '__all__'
    
class AwardsSerializableUpdate(serializers.ModelSerializer):
    photo_award=Base64ImageField(max_length=None,use_url=True)
    image_change=serializers.BooleanField(write_only=True)
    class Meta:
        model = models.Awards
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.name_award=validated_data.get("name_award",instance.name_award)
        instance.number_award=validated_data.get("number_award",instance.number_award)
        if validated_data.get('image_change'):
            if os.path.exists(DIR+instance.photo_award.url):
                os.remove(DIR+instance.photo_award.url)
            instance.photo_award=validated_data.get('image',instance.photo_award)
        instance.save()
        return instance

class TransactionsSerializable(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = '__all__'

class TransactionsDetailSerializable(serializers.ModelSerializer):
    class Meta:
        model = models.TransactionDetail
        fields = '__all__'

class TransactionPrincipalSerializable(serializers.Serializer):
    header=serializers.JSONField()
    detail=serializers.ListField(child=serializers.JSONField())
    def validate_header(self,data):
        #credits_translation
        if not type(data['credits_translation'])==int:
            raise serializers.ValidationError({"credits_translation":'Tiene que ser int'})
        if data['credits_translation'] == None or data['credits_translation']==0:
            raise serializers.ValidationError({"credits_translation":'No puede ser nulo'})
        else:
            client=models.Credits.objects.filter(id=data['credits_translation'])
            if not len(client)>0:
                raise serializers.ValidationError({"credits_translation":'No coincide con la cuenta del cliente'})
        #total_cost
        if not type(data['total_cost'])==int:
            raise serializers.ValidationError({"total_cost":'Tiene que ser int'}) 
        if data['total_cost']==None:
            raise serializers.ValidationError({"total_cost":'No puede ser nulo'})
        #total_credits   
        if not type(data['total_credits'])==int:
            raise serializers.ValidationError({"total_credits":'Tiene que ser int'}) 
        if data['total_credits']==None:
            raise serializers.ValidationError({"total_credits":'No puede ser nulo'})
        #balance    
        if not type(data['balance'])==int:
            raise serializers.ValidationError({"balance":'Tiene que ser int'})
        if data['balance']==None:
            raise serializers.ValidationError({"balance":'No puede ser nulo'})
        if data['total_cost']>data['total_credits'] or int(data['balance'])<0:
            raise serializers.ValidationError({"Error":'Creditos insuficientes'})
        return data
    def validate_detail(self,data):
        for x in data:
            if not type(x['awards_detail'])== int:
                raise serializers.ValidationError({"awards_detail":"Tiene que ser int"})
            if x['awards_detail']<=0 or x['awards_detail']==None:
                raise serializers.ValidationError({"awards_detail":"No puede ser nulo"})
            else:
                awards=models.Awards.objects.filter(id=x['awards_detail'])
                if not len(awards)>0:
                    raise serializers.ValidationError({"awards_detail":'No coincide con un premio'})
            if not type(x["price"])==int:
                raise serializers.ValidationError({"price":"Tiene que ser int"})
            if x["price"]<0:
                raise serializers.ValidationError({"price":"No puede ser negativo"})
            if not type(x["quantity"])==int:
                raise serializers.ValidationError({"quantity":"Tiene que ser int"})
            if x['quantity']<=0:
                raise serializers.ValidationError({"quantity":"No puede ser menor o igual a 0"})
            if not type(x['subtotal'])==int:
                raise serializers.ValidationError({"subtotal": "Tiene que ser int"})
            if x['subtotal']<0:
                raise serializers.ValidationError({"subtotal":"El subtotal no puede estar en negativo"})
        return data
