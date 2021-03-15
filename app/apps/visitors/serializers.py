from rest_framework import serializers


class SimpleDateSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
