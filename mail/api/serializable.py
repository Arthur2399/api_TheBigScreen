from rest_framework import serializers


class settingsSerializable(serializers.Serializer):
    EMAIL_HOST=serializers.CharField(max_length=255)
    EMAIL_HOST_USER=serializers.EmailField()
    EMAIL_HOST_PASSWORD= serializers.CharField(max_length=255)
    RECIPIENT_ADDRESS=serializers.EmailField()

class emailSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField()
    subject = serializers.CharField(required=False)