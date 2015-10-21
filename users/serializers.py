__author__ = 'Diego'

# imports
from users.models import User, FriendRequest, Friendship
from schedules.serializers import GapSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login', 'firstNames', 'lastNames', 'imageURL', 'lastUpdated_on')


class FriendRequestSerializer(serializers.ModelSerializer):

    fromUser = UserSerializer()
    toUser = UserSerializer()
    class Meta:
        model = FriendRequest
        fields = ('fromUser','toUser', 'created_on')

class FriendshipSerializer(serializers.ModelSerializer):
    secondUser = UserSerializer()
    class Meta:
        model = Friendship
        fields = ('firstUser','secondUser', 'created_on')


# Mixed serializer
class UserSerializerWithSchedule(serializers.ModelSerializer):
    schedule = GapSerializer()
    class Meta:
        model = User
        fields = ('login', 'firstNames', 'lastNames', 'imageURL', 'lastUpdated_on')