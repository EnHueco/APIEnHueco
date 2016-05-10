from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from enHuecoAPIMain import settings
from schedules.serializers import ImmediateEventSerializer, GapSerializerNoUser
from tokenizer.models import Tokenizer, Token
from schedules.models import Gap, ImmediateEvent
from users.serializers import *
from rest_framework.test import APITestCase
import datetime


# Create your tests here.

class EHAPITestCase(APITestCase):
    def setUp(self):
        self.my_login = 'test10'
        self.friend_login = 'friend10'

        self.me, self.my_token = User.objects.create_user_and_token(login=self.my_login, first_names='testNames',
                                                                    last_names='testLastNames')

        self.credentials_kwargs = {'HTTP_X_USER_ID': self.my_login, 'HTTP_X_USER_TOKEN': self.my_token.value}

        self.friend, self.friend_token = User.objects.create_user_and_token(login=self.friend_login,
                                                                            first_names='friendName',
                                                                            last_names='friendLast')
        self.friend_credentials_kwargs = {'HTTP_X_USER_ID': self.friend_login,
                                          'HTTP_X_USER_TOKEN': self.friend_token.value}

    def addGapData(self):
        self.gaps = []
        self.friend_gaps = []
        for i in range(1, 4):
            new_gap = Gap.objects.create(name="Event {}".format(i), location="Location {}".format(i), type="CLASS",
                                         start_hour_weekday=str(i), start_hour='100', end_hour='153', user=self.me)

            new_friend_gap = Gap.objects.create(name="Friend Event {}".format(i),
                                                location="Friend Location {}".format(i), type="CLASS",
                                                start_hour_weekday=str(i), start_hour='100', end_hour='153',
                                                user=self.friend)
            self.gaps.append(new_gap)
            self.friend_gaps.append(new_friend_gap)

    def addFriendshipData(self):
        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship1.save()
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)
        friendship2.save()


class FriendRequestTestCase(EHAPITestCase):
    def testSendFriendRequest(self):
        url = reverse('friend-detail', kwargs={'fpk': self.friend_login})  # '/requests/create/'+self.friendLogin +'/'
        data = self.credentials_kwargs

        response = self.client.post(url, format='json', **data)

        fr = FriendRequest(fromUser=self.me, toUser=self.friend)
        fr.save()

        self.assertTrue(self.friend in self.me.requests_sent.all())

    def testSendExistingFriendRequest(self):
        url = reverse('friend-detail', kwargs={'fpk': self.friend_login})  # '/requests/create/'+self.friendLogin +'/'
        data = self.credentials_kwargs

        response = self.client.post(url, format='json', **data)
        response = self.client.post(url, format='json', **data)

        self.assertEqual(response.data, 'ERROR: Already sent request')

    def testSendExistingReverseFriendRequest(self):
        friendRequest = FriendRequest.objects.create(fromUser=self.friend, toUser=self.me)

        url = reverse('friend-detail', kwargs={'fpk': self.friend_login})  # '/requests/create/'+self.friendLogin +'/'
        data = self.credentials_kwargs

        response = self.client.post(url, format='json', **data)

        newFriendShip = Friendship.objects.create(firstUser=self.me, secondUser=self.friend)

        self.assertTrue(self.friend in self.me.friends.all())
        self.assertTrue(self.me in self.friend.friends.all())

    def testShowReceivedFriendRequests(self):
        url = reverse('received-friend-requests-list')
        data = self.credentials_kwargs

        response = self.client.get(url, format='json', **data)

        friends = self.me.requests_received.all()
        serializer = FriendRequestSerializer(friends, many=True)

        self.assertEqual(response.data, serializer.data)

    def testShowSentFriendRequests(self):
        url = reverse('sent-friend-requests-list')
        data = self.credentials_kwargs

        response = self.client.get(url, format='json', **data)

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
        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        serializer = UserSyncSerializer(self.me.friends.all(), many=True)

        url = reverse('friend-list-sync')
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}
        encodedFriend = {'login': self.friend.login}

        response = self.client.get(url, format='json', **data)

        self.assertEqual(response.data, serializer.data)

        pass

    def testShowAllFriends(self):
        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        serializer = UserSerializerWithSchedule(self.me.friends.all(), many=True)

        url = reverse('friend-list')
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}
        encodedFriend = {'login': self.friend.login}

        response = self.client.get(url, format='json', **data)

        self.assertEqual(response.data, serializer.data)

        pass

    def testShowSomeFriends(self):
        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        serializer = UserSerializerWithSchedule(self.me.friends.all(), many=True)

        url = reverse('friend-list')
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}
        encodedFriend = [{'login': self.friend.login}]

        response = self.client.post(url, data=encodedFriend, format='json', **data)

        self.assertEqual(response.data, serializer.data)

    def testShowFriend(self):
        url = reverse('friend-detail', kwargs={'fpk': self.friendLogin})
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}

        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        response = self.client.get(url, format='json', **data)

        serializer = UserSerializerWithSchedule(self.friend)

        self.assertEqual(response.data, serializer.data)

    def testShowUnfriendedFriend(self):
        url = reverse('friend-detail', kwargs={'fpk': self.friendLogin})
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}

        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        response = self.client.get(url, format='json', **data)

        self.assertEqual(response.data, 'ERROR: Users are not friends')

    def testShowAllFriends(self):
        url = reverse('friend-list')
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}

        response = self.client.get(url, format='json', **data)

        friends = self.me.friends.all()
        serializer = FriendshipSerializer(friends, many=True)

        self.assertEqual(response.data, serializer.data)

    def testDeleteFriend(self):
        url = reverse('friend-detail', kwargs={'fpk': self.friend.login})
        data = {'HTTP_X_USER_ID': self.myLogin, 'HTTP_X_USER_TOKEN': self.myToken.value}
        args = {'fpk': self.me.login}

        friendship1 = Friendship(firstUser=self.me, secondUser=self.friend)
        friendship2 = Friendship(firstUser=self.friend, secondUser=self.me)

        friendship1.save()
        friendship2.save()

        response = self.client.delete(url, **data)

        self.assertFalse(self.me in self.friend.friends.all())


# ----- SCHEDULES -----
class SchedulesTestCase(EHAPITestCase):
    def setUp(self):
        super(SchedulesTestCase, self).setUp()
        super(SchedulesTestCase, self).addGapData()
        super(SchedulesTestCase, self).addFriendshipData()

    def testShowGaps(self):
        url = reverse('show-gaps')
        data = self.credentials_kwargs

        response = self.client.get(url, **data)
        serializer = GapSerializer(self.gaps, many=True)

        self.assertEqual(response.data, serializer.data)

    def testCreateGaps(self):
        url = reverse('show-gaps')
        data = self.credentials_kwargs

        events_to_add = []
        for i in range(3):
            new_event = Gap(name="New Event {}".format(i), location="New Location {}".format(i), type="FREE TIME",
                            start_hour_weekday=str(i), start_hour='200', end_hour_weekday=str(i), end_hour='210')
            events_to_add.append(new_event)

        serializer = GapSerializer(events_to_add, many=True)

        response = self.client.post(url, serializer.data, format='json', **data)

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        response.render()
        for i, newly_created_event in enumerate(response.data):

            for event_attribute in newly_created_event.keys():
                new_attributes = ('id', 'created_on', 'updated_on')
                if event_attribute not in new_attributes:
                    self.assertEqual(newly_created_event[event_attribute], getattr(events_to_add[i], event_attribute))

    def testUpdateGap(self):
        data = self.credentials_kwargs

        gaps = self.me.gap_set.all()
        for i, gap in enumerate(gaps):
            gap.name = ""
            gap.location = ""
            gap.start_hour = "99"
            gap.end_hour = "99"
            gap.start_hour_weekday = "88"
            gap.end_hour_weekday = "88"

            url = reverse('gap-detail', kwargs={'gid': gap.id})

            serializer = GapSerializerNoUser(gap)
            response = self.client.put(url, serializer.data, **data)

            response_event = response.data

            for key in response.data.keys():
                if key == 'user':
                    self.assertEqual(response_event[key], getattr(gap, key).login)
                elif '_on' in key :
                    self.assertEqual(response_event[key], getattr(gap, key).strftime(settings.DATETIME_FORMAT))
                else:
                    self.assertEqual(response_event[key], getattr(gap, key))


    def testDeleteGaps(self):
        url = reverse('show-gaps')
        data = self.credentials_kwargs

        serializer = GapSerializer(self.me.gap_set.all(), many=True)
        response = self.client.delete(url, serializer.data, format='json', **data)

        self.gaps = User.objects.get(login=self.my_login).gap_set.all()

        self.assertTrue(response.status_code == status.HTTP_200_OK)
        self.assertTrue(len(self.me.gap_set.all()) == 0)

    def testShowFriendSchedule(self):
        url = reverse('show-friend-gaps', kwargs={'fpk': 'friend10'})
        data = self.credentials_kwargs

        response = self.client.get(url, format='json', **data)
        serializer = GapSerializer(self.friend.gap_set.all(), many=True)

        self.assertEqual(response.data, serializer.data)

    def testUpdateImmediateEvent(self):
        url = reverse('show-immediate-events')
        data = self.credentials_kwargs

        immediate_event = ImmediateEvent(type=Gap.FREE_TIME, name='Immediate Event 1', location='Location 1',
                                         valid_until=datetime.datetime.now())
        serializer = ImmediateEventSerializerNoUser(instance=immediate_event)

        response = self.client.put(url, serializer.data, **data)
        response.data['updated_on'] = None

        for key, value in serializer.data.iteritems():
            self.assertEqual(serializer.data[key], response.data[key])


"""
	def testShowFriendGapsCross (self) :
		url = reverse('show-friend-gaps-cross', kwargs={'fpk' : 'friend10'})
		data = {'HTTP_X_USER_ID' : self.my_login, 'HTTP_X_USER_TOKEN' : self.my_token.value}

		finalSchedule = Gap.crossGaps(self.me.gap_set.all(), self.friend.gap_set.all())
		serializer = GapSerializer(finalSchedule, many=True)

		response = self.client.get(url, **data)

		self.assertEqual(serializer.data, response.data)



	def testUpdateGap (self) :
		newGap = Gap(type="G", start_hour_weekday='1', end_hour_weekday='1', start_hour='080', end_hour='170',
					 user=self.me, id=1)

		serializer = GapSerializer(newGap)
		gap = serializer.data

		url = reverse('gap-detail', kwargs={'gid' : '1'})
		data = self.credentials_kwargs

		response = self.client.put(url, data=gap, **data)

		# Returns the new Gap
		self.assertEqual(serializer.data['start_hour'], response.data['start_hour'])
		self.assertEqual(serializer.data['end_hour'], response.data['end_hour'])
		self.assertEqual(serializer.data['start_hour_weekday'], response.data['start_hour_weekday'])
		self.assertEqual(serializer.data['user'], response.data['user'])

	def testAddGap (self) :
		newGap = Gap(type='GAP', name='My Gap', location='Building A', start_hour_weekday='5', start_hour='100',
					 end_hour_weekday='5', end_hour='153', user=self.me)
		serializer = GapSerializer(newGap)

		gapCount = User.objects.get(login=self.me.login).gap_set.all().count()
		url = reverse('show-gaps')
		data = {'HTTP_X_USER_ID' : self.my_login, 'HTTP_X_USER_TOKEN' : self.my_token.value}
		gap = {'type' :             'GAP', 'name' : 'My Gap', 'location' : 'Building A', 'start_hour_weekday' : '5',
			   'end_hour_weekday' : '5', 'start_hour' : '100', 'end_hour' : '153', 'user' : self.me}

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
"""


class PrivacyTestCase(EHAPITestCase):
    def setUp(self):
        super(PrivacyTestCase, self).setUp()
        super(PrivacyTestCase, self).addGapData()
        super(PrivacyTestCase, self).addFriendshipData()

    def testUpdateLocationPrivacyAttributes(self):
        url = reverse('show-me')
        data = self.credentials_kwargs

        possible_values = [False, True]

        for actual_value in possible_values:
            user_json_data = UserSerializer(self.me).data
            user_json_data['shares_event_names'] = actual_value
            user_json_data['shares_event_locations'] = actual_value
            response = self.client.put(url, data=user_json_data, **data)

            self.me = User.objects.get(login=self.me.login)

            self.assertTrue(self.me.shares_event_names == actual_value,
                            "User attribute 'shares event_names' is not being updated to {}.".format(actual_value))
            self.assertTrue(self.me.shares_event_locations == actual_value,
                            "User attribute 'shares_event_locations' is not being updated to False.".format(
                                actual_value))

    def testHidesLocationPrivacyValues(self):
        url = reverse('show-me')
        friend_data = self.friend_credentials_kwargs

        possible_values = [False, True]

        for actual_boolean_value in possible_values:

            friend_json_data = UserSerializer(self.friend).data
            friend_json_data['shares_event_names'] = actual_boolean_value
            friend_json_data['shares_event_locations'] = actual_boolean_value

            url = reverse('show-me')
            response = self.client.put(url, data=friend_json_data, **friend_data)
            #			print response

            url = reverse('friend-list')
            data = self.credentials_kwargs

            response = self.client.get(url, format='json', **data)

            for user in response.data:
                for event in user['gap_set']:
                    #					print event
                    if actual_boolean_value == False:
                        self.assertEqual(event['location'], '')
                        self.assertEqual(event['name'], '')
                    else:
                        self.assertNotEqual(event['location'], '')
                        self.assertNotEqual(event['name'], '')

# def testUpdateMyScheduleDay(self):

#        weekday = 'tuesday'
#        url = reverse('update-schedule-day')
#        dayJSON = '{\\"AM91\\": true, \\"AM90\\": false, \\"AM111\\": true, \\"AM110\\": false, \\"PM61\\": true,
# \\"PM60\\": false, \\"PM21\\": true, \\"PM20\\": false, \\"PM41\\": false, \\"PM40\\": false, \\"AM80\\": false,
# \\"AM81\\": false, \\"AM100\\": false, \\"AM101\\": false, \\"AM71\\": false, \\"AM70\\": false, \\"PM10\\": false,
#  \\"PM11\\": false, \\"PM31\\": false, \\"PM50\\": false, \\"PM51\\": false, \\"PM30\\": false, \\"PM121\\": false,
#  \\"PM120\\": false}'
#        data = {'login':self.myLogin, 'token':self.myToken.value, 'day': dayJSON, 'weekday': weekday}

#        response = self.client.post(url, data, format='json')

#        self.me = User.objects.get(login=self.myLogin)
#        serializer = DaySerializer(getattr(self.me.schedule, weekday))

#        self.assertEqual(response.data, serializer.data)
