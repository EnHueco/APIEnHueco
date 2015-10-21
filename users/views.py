from rest_framework import viewsets
from rest_framework.response import Response
from users.serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer, UserSerializerWithSchedule
from users.models import User, FriendRequest, Friendship
from django.core import exceptions

#-------------



class UsersViewSet(viewsets.ViewSet):

    def show(self, request, pk):

        user = User.objects.filter(login=pk).first()
        serializer = UserSerializer(user, allow_null=True)
        return Response(serializer.data)


class FriendsViewSet(viewsets.ViewSet):

    def show(self, request, pk, fpk):

        if(Friendship.areFriendsPK(pk, fpk)):
            return UsersViewSet().show(request, fpk)
        else:
            return Response("ERROR: Users are not friends")

    def list(self, request, pk):
        friends = User.objects.filter(login=pk).first().friends.all()
        serializer = UserSerializerWithSchedule(friends, many=True)
        return Response(serializer.data)


    def delete(self, request, pk, fpk):

        if(Friendship.areFriendsPK(pk, fpk)):

            me = User.objects.get(login=pk)
            friend = User.objects.get(login=fpk)

            friendship1 = Friendship.objects.filter(firstUser=me, secondUser=friend).first()
            # Friendship Exists
            friendship2 = Friendship.objects.filter(firstUser=friend, secondUser=me).first()

            # Delete friendships
            friendship1.delete()
            friendship2.delete()

            return Response("Correct")

        else:
            return Response("Users are not friends")



    def create(self, request, pk, fpk):

        try:
            # Get Users
            me = User.objects.get(login=pk)
            newFriend = User.objects.get(login=fpk)

            # Check if users are already friends
            for actualFriend in me.friends.all():
                if(actualFriend == newFriend):
                    # Users are already friends
                    return Response('ERROR: Users are already friends')

            try:
                inverseRequestExists = FriendRequest.objects.get(fromUser=newFriend, toUser=me)

                # Friend has already sent request
                # Delete friend request and add friends
                inverseRequestExists.delete()
                f1 = Friendship(firstUser=me,secondUser=newFriend)
                f1.save()
                f2 = Friendship(firstUser=newFriend,secondUser=me)
                f2.save()

                serializer = FriendshipSerializer(f1)
                return Response(serializer.data)

            except exceptions.ObjectDoesNotExist:
                # No inverse relationship exists
                # We will search for an existing request from sender
                try:
                    exists = FriendRequest.objects.get(fromUser=me, toUser=newFriend)
                    # Already has sent request
                    return Response('ERROR: Already sent request')

                except exceptions.ObjectDoesNotExist:
                    # Haven't sent request
                    request = FriendRequest(fromUser=me, toUser=newFriend)
                    request.save()
                    serializer = FriendRequestSerializer(request)
                    return Response(serializer.data)

                except exceptions.MultipleObjectsReturned:
                    # Many requests from me to same friend
                    return Response('ERROR: # Many requests from me to same friend')

            except exceptions.MultipleObjectsReturned:
                # Many inverse relations have been sent
                return Response('ERROR: # Many inverse relations have been sent')

        except exceptions.ObjectDoesNotExist:
            # No users found
            return Response('ERROR: # No users found')

        except exceptions.MultipleObjectsReturned:
            # Multiple users found for same login
            return Response('ERROR: # Multiple users found for same login')

class SentFriendRequestViewSet(viewsets.ViewSet):

    def list(self, request, pk):

        # Find User and return sent requests
        me = User.objects.filter(login=pk).first()
        requests = me.requests_sent.all()
        serializer = UserSerializer(requests, many=True)
        return Response(serializer.data)

class ReceivedFriendRequestViewSet(viewsets.ViewSet):

    def list(self, request, pk):
        # Find User and return sent requests
        me = User.objects.filter(login=pk).first()
        requests = me.requests_received.all()
        serializer = UserSerializer(requests, many=True)
        return Response(serializer.data)