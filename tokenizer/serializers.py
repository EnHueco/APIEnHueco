__author__ = 'Diego'
from rest_framework import serializers
from tokenizer.models import Token

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('value', 'owner', 'created_on')