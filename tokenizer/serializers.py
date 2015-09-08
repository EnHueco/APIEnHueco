__author__ = 'Diego'
from rest_framework import serializers
from tokenizer.models import Token
from users.serializers import UserSerializer

class TokenSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = Token
        fields = ('value', 'user', 'created_on')