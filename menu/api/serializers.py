from rest_framework import serializers
from menu import models

class assignmentSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    menu_id=serializers.IntegerField(read_only=True)
    menu=serializers.CharField(read_only=True)
    path=serializers.CharField(read_only=True)