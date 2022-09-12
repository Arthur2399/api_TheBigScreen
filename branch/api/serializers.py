from rest_framework import serializers
from branch.models import Branch

class BranchSerializers(serializers.ModelSerializer):
    stars=serializers.FloatField(read_only=True)
    class Meta:
        model = Branch
        fields="__all__"