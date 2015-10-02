from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Details


class DetailSerializer(serializers.ModelSerializer):
    """
        Details Model Serializer
    """
    class Meta:
        model = Details
        fields = ('user', 'father_name', 'mother_name', 'city')


class UserSerializer(serializers.ModelSerializer):
    """
        User model Serializer
    """
    details = DetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'details')
