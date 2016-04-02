__author__ = 'Diego'
from rest_framework import serializers
from tokenizer.models import Token
from users.serializers import UserSerializerWithSchedule


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializerWithSchedule()

    class Meta:
        model = Token
        depth = 2
        fields = ('value', 'user', 'created_on')
