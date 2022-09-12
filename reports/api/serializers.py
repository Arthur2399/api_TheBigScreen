from rest_framework import serializers

class type(serializers.Serializer):
    type=serializers.ChoiceField(choices=[1,2,"month","day"],write_only=True)

class report_survey(serializers.Serializer):
    branch_id=serializers.IntegerField(write_only=True)