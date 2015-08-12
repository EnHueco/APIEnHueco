from django.db import models
from django.utils import timezone
from django.conf import settings
#---------

class User(models.Model):

    # User Data
    login = models.CharField(max_length=30, primary_key=True)
    firstNames = models.CharField(max_length=50)
    lastNames = models.CharField(max_length=50)
    imageURL = models.CharField(max_length=200)

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now())
    lastUpdated_on = models.DateTimeField(auto_now=True)

    # Relationships

    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends+', through='Friendship')
    requests_sent= models.ManyToManyField('self', through='FriendRequest',symmetrical=False, related_name='requests_received')


    def isFriendsWith(self, otherUser):
        return otherUser in self.friends.all()

    @classmethod
    def create(cls, login, firstNames, lastNames):
        me = cls(login=login, firstNames=firstNames, lastNames=lastNames)
        return me

    def __str__(self):
        return self.login


class FriendRequest(models.Model):

    fromUser = models.ForeignKey(settings.USER_MODEL, related_name='+')
    toUser = models.ForeignKey(settings.USER_MODEL, related_name='+')

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now())
    lastUpdated_on = models.DateTimeField(auto_now=True)

class Friendship(models.Model):

    firstUser = models.ForeignKey(settings.USER_MODEL, related_name='+')
    secondUser = models.ForeignKey(settings.USER_MODEL, related_name='+')

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now())
    lastUpdated_on = models.DateTimeField(auto_now=True)


    @classmethod
    def areFriends(cls, user1, user2):
        """
        :param user1: User
        :param user2: User
        :return:
        """
        return user2 in user1.friends.all()

    @classmethod
    def areFriendsPK(cls, user1, user2):
        """
        :param user1: String
        :param user2: String
        :return:
        """
        usr1 = User.objects.filter(login=user1).first()
        usr2 = User.objects.filter(login=user2).first()

        if(usr1 is not None and usr2 is not None):

            return cls.areFriends(usr1,usr2)

        else:
            return False