import imagekit
from django.db import models
from django.utils import timezone
from django.conf import settings
from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import strategies
#---------

def generate_filename(self, filename):
    url = "photos/original/%s.%s" % (self.login, filename.split(".")[-1].lower())
    return url

class ThumbnailSpec(ImageSpec):
    processors=[ResizeToFill(100,100)]
    format='JPEG'
    options={'quality': 80}
    cachefile_strategy = strategies.Optimistic

    # put thumbnails into the "photos/thumbs" folder and
    # name them the same as the source file
    @property
    def cachefile_name(self):
        source_filename = getattr(self.source, 'name', None) # type: str
        s = "photos/thumbs/" + source_filename.split('photos/original/')[1]
        return s

register.generator('enhueco:thumbnail', ThumbnailSpec)

class User(models.Model):

    ### User Data
    login = models.CharField(max_length=30, primary_key=True, default=None)
    firstNames = models.CharField(max_length=50, null=False, blank=False, default=None)
    lastNames = models.CharField(max_length=50, null=False, default=None)
    phoneNumber = models.CharField(max_length=30, default="", blank=True)
    imageURL = models.ImageField(upload_to= generate_filename)
    image_thumbnail = ImageSpecField(source='imageURL',
                                     id='enhueco:thumbnail'
                                     )
    # imageURL = models.CharField(max_length=200)

    ### Privacy Handling
    shares_user_nearby = models.BooleanField(default=True)
    shares_event_names = models.BooleanField(default=True)
    shares_event_locations = models.BooleanField(default=True)

    ### Relationship handlers
    schedule_updated_on = models.DateTimeField(default=timezone.now)

    ### Control Attributes
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    ### Relationship
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends+', through='Friendship')
    requests_sent= models.ManyToManyField('self', through='FriendRequest',symmetrical=False, related_name='requests_received')

    def get_image_thumbnail(self):
        return self.image_thumbnail.url

    def isFriendsWith(self, otherUser):
        return otherUser in self.friends.all()

    @classmethod
    def create(cls, login, firstNames, lastNames):
        me = cls(login=login, firstNames=firstNames, lastNames=lastNames)
        return me

    def __str__(self):
        return '{} : {} {}'.format(self.login, self.firstNames, self.lastNames)

class FriendRequest(models.Model):

    fromUser = models.ForeignKey(settings.USER_MODEL, related_name='+')
    toUser = models.ForeignKey(settings.USER_MODEL, related_name='+')

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now)
    # lastUpdated_on = models.DateTimeField(auto_now=True)

class Friendship(models.Model):

    firstUser = models.ForeignKey(settings.USER_MODEL, related_name='+')
    secondUser = models.ForeignKey(settings.USER_MODEL, related_name='+')

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now)
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