from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.response import Response

from rest_framework import status

# IMPORT MODELS
from tokenizer.models import Tokenizer, Token
from users.models import User, FriendRequest, Friendship
from schedules.models import Gap
# IMPORT SERIALIZERS
from schedules.serializers import GapSerializer
from users.serializers import *
from rest_framework.test import  APITestCase

# Create your tests here.

class FriendRequestTestCase(APITestCase):

    def setUp(self):

        self.myLogin = 'test10'
        self.friendLogin = 'friend10'

        self.me = User.create(login=self.myLogin, firstNames='testNames', lastNames='testLastNames')
        self.me.save()
        self.myToken = Tokenizer.assignToken(self.me)

        self.friend = User.create(login=self.friendLogin, firstNames='friendName', lastNames='friendLast')
        self.friend.save()


    def testSendFriendRequest(self):

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})#'/requests/create/'+self.friendLogin +'/'
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.post(url,format='json', **data)

        fr = FriendRequest(fromUser=self.me, toUser=self.friend)
        fr.save()

        self.assertTrue(self.friend in self.me.requests_sent.all())


    def testSendExistingFriendRequest(self):

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})#'/requests/create/'+self.friendLogin +'/'
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.post(url, format='json', **data)
        response = self.client.post(url, format='json', **data)

        self.assertEqual(response.data, 'ERROR: Already sent request')


    def testSendExistingReverseFriendRequest(self):

        friendRequest = FriendRequest(fromUser=self.friend, toUser=self.me)
        friendRequest.save()

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})#'/requests/create/'+self.friendLogin +'/'
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.post(url, format='json', **data)

        newFriendShip = Friendship.objects.create(firstUser=self.me, secondUser=self.friend)

        self.assertTrue(self.friend in self.me.friends.all())
        self.assertTrue(self.me in self.friend.friends.all())


    def testShowReceivedFriendRequests(self):
        url = reverse('received-friend-requests-list')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.get(url,format='json', **data)

        friends = self.me.requests_received.all()
        serializer = FriendRequestSerializer(friends, many=True)

        self.assertEqual(response.data, serializer.data)


    def testShowSentFriendRequests(self):

        url = reverse('sent-friend-requests-list')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.get(url,format='json', **data)

        friends = self.me.requests_sent.all()
        serializer = FriendRequestSerializer(friends, many=True)

        self.assertEqual(response.data, serializer.data)



class FriendshipTestCase(APITestCase):


    def setUp(self):

        self.myLogin = 'test10'
        self.friendLogin = 'friend10'

        self.me = User.create(login=self.myLogin, firstNames='testNames', lastNames='testLastNames')
        self.me.save()
        self.myToken = Tokenizer.assignToken(self.me)

        self.friend = User.create(login=self.friendLogin, firstNames='friendName', lastNames='friendLast')
        self.friend.save()


    def testShowAllSyncFriends(self):

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        friendship1.save()
        friendship2.save()

        serializer = UserSyncSerializer(self.me.friends.all(), many=True)

        url = reverse('friend-list-sync')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}
        encodedFriend = {'login': self.friend.login}

        response = self.client.get(url, format='json', **data)

        self.assertEqual(response.data, serializer.data)

        pass


    def testShowAllFriends(self):

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        friendship1.save()
        friendship2.save()

        serializer = UserSerializerWithSchedule(self.me.friends.all(), many=True)

        url = reverse('friend-list')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}
        encodedFriend = {'login': self.friend.login}

        response = self.client.get(url, format='json', **data)

        self.assertEqual(response.data, serializer.data)

        pass

    def testShowSomeFriends(self):

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        friendship1.save()
        friendship2.save()

        serializer = UserSerializerWithSchedule(self.me.friends.all(), many=True)

        url = reverse('friend-list')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}
        encodedFriend = {'login': self.friend.login}

        response = self.client.post(url, data=encodedFriend, **data)

        self.assertEqual(response.data, serializer.data)

        pass




    def testShowFriend(self):

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        friendship1.save()
        friendship2.save()

        response = self.client.get(url,format='json', **data)

        serializer = UserSerializerWithSchedule(self.friend)

        self.assertEqual(response.data, serializer.data)


    def testShowUnfriendedFriend(self):

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        response = self.client.get(url,format='json', **data)


        self.assertEqual(response.data, 'ERROR: Users are not friends')



    def testShowAllFriends(self):

        url = reverse('friend-list')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.get(url,format='json', **data)

        friends = self.me.friends.all()
        serializer = FriendshipSerializer(friends, many=True)


        self.assertEqual(response.data, serializer.data)


    def testDeleteFriend(self):

        url = reverse('friend-detail',kwargs={'fpk': self.friend.login})
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}
        args={'fpk': self.me.login}

        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        response = self.client.delete(url,**data)

        self.assertFalse(self.me in self.friend.friends.all())



#----- SCHEDULES -----
class SchedulesTestCase(APITestCase):

    def setUp(self):
        pass

        self.myLogin = 'test10'
        self.friendLogin = 'friend10'

        self.me = User.create(login=self.myLogin, firstNames='testNames', lastNames='testLastNames')
        self.me.save()

        self.gap1 = Gap.objects.create(name="", location ="", type="", start_hour_weekday="1",start_hour='100',end_hour='153',user=self.me)
        self.gap2 = Gap.objects.create(name="", location ="", type="", start_hour_weekday="2",start_hour='100',end_hour='153',user=self.me)
        self.gap3 = Gap.objects.create(name="", location ="", type="", start_hour_weekday="3",start_hour='100',end_hour='153',user=self.me)


        self.myToken = Tokenizer.assignToken(self.me)

        self.friend = User.create(login=self.friendLogin, firstNames='friendName', lastNames='friendLast')
        self.friend.save()

        self.fgap1 = Gap.objects.create(name="", location ="", type="", start_hour_weekday="1",start_hour='100',end_hour='153',user=self.friend)
        self.fgap2 = Gap.objects.create(name="", location ="", type="", start_hour_weekday="2",start_hour='100',end_hour='153',user=self.friend)
        self.fgap3 = Gap.objects.create(name="", location ="", type="", start_hour_weekday="3",start_hour='100',end_hour='153',user=self.friend)



    def testShowGaps(self):

        url = reverse('show-gaps')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.get(url, **data)
        serializer = GapSerializer([self.gap1,self.gap2,self.gap3], many=True)

        self.assertEqual(response.data, serializer.data)

    def testAddGap(self):

        newGap = Gap(type='GAP', name='My Gap', location='Building A',
                     start_hour_weekday='5',start_hour='100',
                     end_hour_weekday='5', end_hour='153',
                     user=self.me)
        serializer = GapSerializer(newGap)

        gapCount = User.objects.get(login=self.me.login).gap_set.all().count()
        url = reverse('show-gaps')
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}
        gap = { 'type' : 'GAP',
                'name' : 'My Gap',
                'location' : 'Building A',
                'start_hour_weekday':'5',
                'end_hour_weekday':'5',
                'start_hour':'100',
                'end_hour':'153',
                'user':self.me}

        response = self.client.post(url, data=gap, **data)

        gapCount2 = User.objects.get(login=self.me.login).gap_set.all().count()

        # Amount of gaps +1
        self.assertTrue(gapCount + 1 == gapCount2)

        # Returns the new Gap
        self.assertEqual(serializer.data['name'], response.data['name'])
        self.assertEqual(serializer.data['start_hour'], response.data['start_hour'])
        self.assertEqual(serializer.data['end_hour'], response.data['end_hour'])
        self.assertEqual(serializer.data['start_hour_weekday'], response.data['start_hour_weekday'])
        self.assertEqual(serializer.data['user'], response.data['user'])



    def testShowFriendSchedule(self):

        url = reverse('show-friend-gaps', kwargs={'fpk':'friend10'})
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}


        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship1.save()
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)
        friendship2.save()

        self.friend = self.me.friends.all()[0]

        response = self.client.get(url,format='json', **data)
        serializer = GapSerializer(self.friend.gap_set.all(), many=True)

        self.assertEqual(response.data, serializer.data)

    def testShowFriendGapsCross(self):

        url = reverse('show-friend-gaps-cross', kwargs={'fpk':'friend10'})
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship1.save()
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)
        friendship2.save()

        finalSchedule = Gap.crossGaps(self.me.gap_set.all(), self.friend.gap_set.all() )
        serializer = GapSerializer(finalSchedule, many=True)

        response = self.client.get(url, **data)

        self.assertEqual(serializer.data, response.data)

    def testUpdateGap(self):


        newGap = Gap(type="G",
                     start_hour_weekday='1',
                     end_hour_weekday='1',
                     start_hour='080',
                     end_hour='170',
                     user=self.me,
                     id=1)

        serializer = GapSerializer(newGap)
        gap = serializer.data

        url = reverse('gap-detail', kwargs={'gid': '1'})
        data = {'HTTP_X_USER_ID':self.myLogin, 'HTTP_X_USER_TOKEN':self.myToken.value}

        response = self.client.put(url, data=gap, **data)


        # Returns the new Gap
        self.assertEqual(serializer.data['start_hour'], response.data['start_hour'])
        self.assertEqual(serializer.data['end_hour'], response.data['end_hour'])
        self.assertEqual(serializer.data['start_hour_weekday'], response.data['start_hour_weekday'])
        self.assertEqual(serializer.data['user'], response.data['user'])



#    def testUpdateMyScheduleDay(self):

#        weekday = 'tuesday'
#        url = reverse('update-schedule-day')
#        dayJSON = '{\\"AM91\\": true, \\"AM90\\": false, \\"AM111\\": true, \\"AM110\\": false, \\"PM61\\": true, \\"PM60\\": false, \\"PM21\\": true, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}'
#        data = {'login':self.myLogin, 'token':self.myToken.value, 'day': dayJSON, 'weekday': weekday}

#        response = self.client.post(url, data, format='json')

#        self.me = User.objects.get(login=self.myLogin)
#        serializer = DaySerializer(getattr(self.me.schedule, weekday))

#        self.assertEqual(response.data, serializer.data)
