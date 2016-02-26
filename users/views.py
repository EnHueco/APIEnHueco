from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *
from users.models import User, FriendRequest, Friendship
from schedules.models import Gap
from django.core import exceptions
from django.db.models import Q


# -------------

class UsersViewSet(viewsets.ViewSet) :
	def show (self, request, pk, isSync=False) :

		user = User.objects.filter(login=pk).first()
		serializer = UserSerializerWithSchedule(user, allow_null=True)
		return Response(serializer.data)


	def updateImageURL (self, request, pk) :

		user = User.objects.filter(login=pk).first()
		serializer = UserImageSerializer(user, data=request.data, partial=True)
		if serializer.is_valid() :
			serializer.save()
			serializer = UserSerializer(user)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else :
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def update (self, request, pk) :

		user = User.objects.filter(login=pk).first()  # type: User
		serializer = UserSerializer(user, data=request.data, partial=True)
		if serializer.is_valid() :
			serializer.save()
			serializer = UserSerializer(user)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else :
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendsViewSet(viewsets.ViewSet) :
	def show (self, request, pk, fpk) :

		if (Friendship.areFriendsPK(pk, fpk)) :
			return UsersViewSet().show(request, fpk)
		else :
			return Response("ERROR: Users are not friends")


	def list (self, request, pk, is_sync=False) :

		friendsQuery = User.objects.filter(login=pk).first().friends

		serializer = UserIDSerializer(data=request.data)
		# Filter requested friends, if any.
		if serializer.is_valid() :
			my_filter_qs = Q()
			for login in serializer.validated_data :
				my_filter_qs = my_filter_qs | Q(login=login)
			friendsQuery = friendsQuery.filter(my_filter_qs)

		## Handling privacy data
		friends = friendsQuery.all()

		if is_sync :
			serializer = UserSyncSerializer(friends, many=True)
		else :
			serializer = UserSerializerWithSchedule(friends, many=True)

		return Response(serializer.data)


	def delete (self, request, pk, fpk) :

		if (Friendship.areFriendsPK(pk, fpk)) :

			me = User.objects.get(login=pk)
			friend = User.objects.get(login=fpk)

			friendship1 = Friendship.objects.filter(firstUser=me, secondUser=friend).first()
			# Friendship Exists
			friendship2 = Friendship.objects.filter(firstUser=friend, secondUser=me).first()

			# Delete friendships
			friendship1.delete()
			friendship2.delete()

			return Response("Correct")

		else :
			return Response("Users are not friends")


	def create (self, request, pk, fpk) :

		try :
			# Get Users
			me = User.objects.get(login=pk)
			newFriend = User.objects.get(login=fpk)

			# Check if users are already friends
			for actualFriend in me.friends.all() :
				if (actualFriend == newFriend) :
					# Users are already friends
					return Response('ERROR: Users are already friends')

			try :
				inverseRequestExists = FriendRequest.objects.get(fromUser=newFriend, toUser=me)

				# Friend has already sent request
				# Delete friend request and add friends
				inverseRequestExists.delete()
				f1 = Friendship(firstUser=me, secondUser=newFriend)
				f1.save()
				f2 = Friendship(firstUser=newFriend, secondUser=me)
				f2.save()

				serializer = FriendshipSerializer(f1)
				return Response(serializer.data)

			except exceptions.ObjectDoesNotExist :
				# No inverse relationship exists
				# We will search for an existing request from sender
				try :
					exists = FriendRequest.objects.get(fromUser=me, toUser=newFriend)
					# Already has sent request
					return Response('ERROR: Already sent request')

				except exceptions.ObjectDoesNotExist :
					# Haven't sent request
					request = FriendRequest(fromUser=me, toUser=newFriend)
					request.save()
					serializer = FriendRequestSerializer(request)
					return Response(serializer.data)

				except exceptions.MultipleObjectsReturned :
					# Many requests from me to same friend
					return Response('ERROR: # Many requests from me to same friend')

			except exceptions.MultipleObjectsReturned :
				# Many inverse relations have been sent
				return Response('ERROR: # Many inverse relations have been sent')

		except exceptions.ObjectDoesNotExist :
			# No users found
			return Response('ERROR: # No users found')

		except exceptions.MultipleObjectsReturned :
			# Multiple users found for same login
			return Response('ERROR: # Multiple users found for same login')


class SentFriendRequestViewSet(viewsets.ViewSet) :
	def list (self, request, pk) :
		# Find User and return sent requests
		me = User.objects.filter(login=pk).first()
		requests = me.requests_sent.all()
		serializer = UserSerializer(requests, many=True)
		return Response(serializer.data)


class ReceivedFriendRequestViewSet(viewsets.ViewSet) :
	def list (self, request, pk) :
		# Find User and return sent requests
		me = User.objects.filter(login=pk).first()
		requests = me.requests_received.all()
		serializer = UserSerializer(requests, many=True)
		return Response(serializer.data)
