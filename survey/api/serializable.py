from rest_framework import serializers
from survey import models

class SurveyTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Survey_template
        fields='__all__'

class SurveySerializer(serializers.ModelSerializer):
    movies=serializers.CharField(read_only=True)
    class Meta:
        model=models.Survey
        fields='__all__'

class surveyAnswer(serializers.Serializer):
    answer1=serializers.CharField(max_length=100)
    answer2=serializers.CharField(max_length=100)
    answer3=serializers.CharField(max_length=100)
    answer4=serializers.CharField(max_length=100)
    answer5=serializers.CharField(max_length=100)