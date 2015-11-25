from django.test import TestCase
import datetime
from users.models import User, Friendship
from users.serializers import UserLocationSerializer



class LocationTestCase(TestCase):

    def testLocationCorrect(self):
        pass
        # ## Scenario setup
        # user1 = User.objects.create(login="user1", firstNames="fn1", lastNames="ln1")
        # user2 = User.objects.create(login="user2", firstNames="fn2", lastNames="ln2")
        # Friendship.objects.create(firstUser=user1, secondUser=user2)
        # Friendship.objects.create(firstUser=user2, secondUser=user1)
        #
        # ## Location setup
        # now = datetime.datetime.now()
        # user2.location.bssid= "bssid1"
        # user2.location.bssid_date=now
        # earlier = datetime.datetime.now() - datetime.timedelta(minutes=5)
        # friends = User.objects.get(login="user1").friends.filter(location__bssid_date__range=(earlier, now))
        # serializer = UserLocationSerializer(friends, many=True)
        # print(serializer.data)