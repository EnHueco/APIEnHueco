from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.response import Response

from rest_framework import status

# IMPORT MODELS
from authentication.models import LDAPWrapper
from tokenizer.models import Tokenizer, Token
from users.models import User, FriendRequest, Friendship

# IMPORT SERIALIZERS
from users.serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer

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
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        response = self.client.post(url, data, format='json')

        fr = FriendRequest(fromUser=self.me, toUser=self.friend)
        fr.save()

        self.assertTrue(self.friend in self.me.requests_sent.all())


    def testSendExistingFriendRequest(self):

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})#'/requests/create/'+self.friendLogin +'/'
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.data, 'ERROR: Already sent request')


    def testSendExistingReverseFriendRequest(self):

        friendRequest = FriendRequest(fromUser=self.friend, toUser=self.me)
        friendRequest.save()

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})#'/requests/create/'+self.friendLogin +'/'
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        response = self.client.post(url, data, format='json')

        newFriendShip = Friendship.objects.create(firstUser=self.me, secondUser=self.friend)

        self.assertTrue(self.friend in self.me.friends.all())
        self.assertTrue(self.me in self.friend.friends.all())


    def testShowReceivedFriendRequests(self):
        url = reverse('received-friend-requests-list')
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        response = self.client.get(url,data=data,format='json')

        friends = self.me.requests_received.all()
        serializer = FriendRequestSerializer(friends, many=True)

        self.assertEqual(response.data, serializer.data)


    def testShowSentFriendRequests(self):

        url = reverse('sent-friend-requests-list')
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        response = self.client.get(url,data=data,format='json')

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


    def testShowFriend(self):

        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        friendship1.save()
        friendship2.save()

        response = self.client.get(url,data=data,format='json')

        serializer = UserSerializer(self.friend)

        self.assertEqual(response.data, serializer.data)

    def testShowUnfriendedFriend(self):


        url = reverse('friend-detail', kwargs={'fpk' : self.friendLogin})
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)

        response = self.client.get(url,data=data,format='json')


        self.assertEqual(response.data, 'ERROR: Users are not friends')



    def testShowAllFriends(self):

        url = reverse('friend-list')
        data = {'user_id':self.myLogin, 'token':self.myToken.value}

        response = self.client.get(url,data=data,format='json')

        friends = self.me.friends.all()
        serializer = FriendshipSerializer(friends, many=True)


        self.assertEqual(response.data, serializer.data)


    def testDeleteFriend(self):

        url = reverse('friend-detail',kwargs={'fpk': self.friend.login})
        data = {'user_id':self.myLogin, 'token':self.myToken.value}
        args={'fpk': self.me.login}

        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        response = self.client.delete(url,data=data)

        self.assertFalse(self.me in self.friend.friends.all())



# ----- SCHEDULES -----
# class SchedulesTestCase(APITestCase):
#
#
#     def setUp(self):
#         pass
#
#         self.myLogin = 'test10'
#         self.friendLogin = 'friend10'
#
#         self.me = User.create(login=self.myLogin, firstNames='testNames', lastNames='testLastNames')
#         self.me.save()
#
#         self.mySchedule = Schedule.create()
#         self.mySchedule.owner = self.me
#         self.mySchedule.save()
#
#         self.friendSchedule = Schedule.create()
#
#         self.myToken = Tokenizer.assignToken(self.me)
#
#         self.friend = User.create(login=self.friendLogin, firstNames='friendName', lastNames='friendLast')
#         self.friend.save()
#
#         self.friendSchedule.owner = self.friend
#         self.friendSchedule.save()
#
#
#     def testShowMySchedule(self):
#         pass
#
# #        url = reverse('show-schedule')
# #        data = {'login':self.myLogin, 'token':self.myToken.value}
# #
# #        response = self.client.post(url, data, format='json')
# #        serializer = ScheduleSerializer(self.me.schedule)
#
# #        self.assertEqual(response.data, serializer.data)
#
#     def testUpdateMySchedule(self):
#         pass
#
# #        url = reverse('update-schedule')
# #        scheduleJSON = '{"monday": "{\\"AM91\\": true, \\"AM90\\": false, \\"AM111\\": true, \\"AM110\\": false, \\"PM61\\": true, \\"PM60\\": false, \\"PM21\\": true, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}", "tuesday": "{\\"AM91\\": false, \\"AM90\\": false, \\"AM111\\": false, \\"AM110\\": false, \\"PM61\\": false, \\"PM60\\": false, \\"PM21\\": false, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}", "wednesday": "{\\"AM91\\": false, \\"AM90\\": false, \\"AM111\\": false, \\"AM110\\": false, \\"PM61\\": false, \\"PM60\\": false, \\"PM21\\": false, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}", "thursday": "{\\"AM91\\": false, \\"AM90\\": false, \\"AM111\\": false, \\"AM110\\": false, \\"PM61\\": false, \\"PM60\\": false, \\"PM21\\": false, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}", "friday": "{\\"AM91\\": false, \\"AM90\\": false, \\"AM111\\": false, \\"AM110\\": false, \\"PM61\\": false, \\"PM60\\": false, \\"PM21\\": false, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}", "created_on": "2015-01-29T23:02:07.672090", "lastUpdated_on": "2015-01-29T23:02:07.672090" }'
# #        data = {'login':self.myLogin, 'token':self.myToken.value, 'schedule': scheduleJSON}
#
# #        response = self.client.post(url, data, format='json')
#
# #        self.me = User.objects.get(login=self.myLogin)
# #        serializer = ScheduleSerializer(self.me.schedule)
#
# #        self.assertEqual(response.data, serializer.data)
#
#
#     def testShowFriendSchedule(self):
#         pass
# #        url = reverse('friend-detail-schedule', kwargs={'fpk':'friend10'})
# #        data = {'login':self.myLogin, 'token':self.myToken.value}
#
#
# #        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
# #        friendship1.save()
# #        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)
# #        friendship2.save()
#
# #        self.assertEqual(self.me.friends.all()[0], self.friend)
# #        friend = self.me.friends.all()[0]
#
# #        response = self.client.post(url, data, format='json')
# #        serializer = ScheduleSerializer(friend.schedule)
#
# #        self.assertEqual(response.data, serializer.data)
#
#     def testShowCrossSchedulesFriend(self):
#         pass
# #        url = reverse('show-cross-schedule-friend', kwargs={'fpk':'friend10'})
# #        data = {'login':self.myLogin, 'token':self.myToken.value}
#
# #        friendship1 = Friendship(firstUser=self.me,secondUser=self.friend)
# #        friendship1.save()
# #        friendship2 = Friendship(firstUser=self.friend,secondUser=self.me)
# #        friendship2.save()
#
# #        finalSchedule = Schedule.crossSchedules(self.me.schedule, self.friend.schedule)
# #        serializer = ScheduleSerializer(finalSchedule)
#
# #        response = self.client.post(url, data, format='json')
#
#
# #        for weekDay in Schedule.WEEKDAYS:
# #            self.assertEqual(serializer.data[weekDay], response.data[weekDay])
#
#
# #    def testUpdateMyScheduleDay(self):
#
# #        weekday = 'tuesday'
# #        url = reverse('update-schedule-day')
# #        dayJSON = '{\\"AM91\\": true, \\"AM90\\": false, \\"AM111\\": true, \\"AM110\\": false, \\"PM61\\": true, \\"PM60\\": false, \\"PM21\\": true, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false, \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false, \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false, \\"PM120\\": false}'
# #        data = {'login':self.myLogin, 'token':self.myToken.value, 'day': dayJSON, 'weekday': weekday}
#
# #        response = self.client.post(url, data, format='json')
#
# #        self.me = User.objects.get(login=self.myLogin)
# #        serializer = DaySerializer(getattr(self.me.schedule, weekday))
#
# #        self.assertEqual(response.data, serializer.data)
