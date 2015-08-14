from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.core import exceptions
from authentication.models import LDAPWrapper
from tokenizer.models import Tokenizer, Token
from users.models import User, Friendship
from tokenizer.serializers import TokenSerializer
from users.views import SentFriendRequestViewSet, ReceivedFriendRequestViewSet, UsersViewSet
from users.views import FriendsViewSet
from schedules.views import GapsViewSet

# Method that authenticates user if valid token and user_id is given
class APIView(APIView):

    def set_authentication_params(self, request):

        self.user_id =  request.META['HTTP_X_USER_ID']
        self.token = request.META['HTTP_X_USER_TOKEN']

    def authenticate(self):
        return Tokenizer.authenticate(self.user_id, self.token)



class Authenticate(APIView):


    def post(self, request):

        user_id = request.data['user_id']
        password = request.data['password']

        ldapWrapper = LDAPWrapper()
        access_granted = ldapWrapper.authenticate(user_id, password)

        if(access_granted):
            finalUser = None
            try:
                user = User.objects.get(login=user_id)
                finalUser = user
                # user already exists

            except exceptions.ObjectDoesNotExist:
                # user doesn't exist
                data = ldapWrapper.search(user_id)
                # FALTA Revisar data...

                deleteExtraChars = r'[\[\]\']'

                firstNames = data['givenName'][0].strip()
                lastNames = data['sn'][0].strip()

                # CREATE and save User
                newUser = User.create(login=user_id, firstNames=firstNames, lastNames=lastNames)
                newUser.save()

                finalUser = newUser

            except exceptions.MultipleObjectsReturned:
                return Response('ERROR')

            token = Tokenizer.assignToken(finalUser)

            serializer = TokenSerializer(token)

            return Response(serializer.data)

        else:
            # Invalid Credentials
            return Response('ERROR: Invalid Credentials')


# ------ USER ------


class UserDetail(APIView):

    def get(self, request):
        self.set_authentication_params(request)
        if self.authenticate():
            return UsersViewSet().show(request,self.user_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# ------ FRIEND REQUESTS ------

class ReceivedFriendRequestsList(APIView):

    def get(self, request):
        self.set_authentication_params(request)
        if self.authenticate():
            return ReceivedFriendRequestViewSet().list(request, self.user_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SentFriendRequestList(APIView):

    def get(self, request):
        self.set_authentication_params(request)
        if self.authenticate():
            return SentFriendRequestViewSet().list(request, pk=self.user_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#  ------  FRIENDSHIPS -------
class FriendDetail(APIView):

    def get(self, request, fpk):
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().show(request, self.user_id, fpk)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, fpk):

        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().create(request,pk=self.user_id,fpk=fpk)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, fpk):
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().delete(request, self.user_id, fpk)
        else:
            #
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

class FriendList(APIView):

    def get(self, request):
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().list(request, self.user_id)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

# ------- GAPS -------

class GapsList(APIView):

    def get(self, request):
        self.set_authentication_params(request)
        if self.authenticate():
            return GapsViewSet().list(request, self.user_id)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        self.set_authentication_params(request)
        if self.authenticate():
            return GapsViewSet().create(request)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

class GapsFriendList(APIView):

    def get(self, request, fpk):

        self.set_authentication_params(request)
        if self.authenticate():
            if Friendship.areFriendsPK(self.user_id, fpk):
                return GapsViewSet().list(request, fpk)
            else:
                return Response('Users are not friends',status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

class GapsCross(APIView):

    def get(self, request, fpk):
        self.set_authentication_params(request)
        if self.authenticate():
            if Friendship.areFriendsPK(self.user_id,fpk):
                return GapsViewSet().cross(request, pk1=self.user_id, pk2=fpk)
            else:
                return Response('Users are not friends',status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

"""
class UpdateMySchedule(APIView):

    def post(self, request):
        if(Tokenizer.authenticate(request.data['user_id'], request.data['token'])):
            user_id = request.data['user_id']
            schedule = request.data['schedule']
            view = SchedulesViews()
            return view.updateSchedule(request, ownerPK=user_id, scheduleUpdate=schedule)
        else:
            return Response('Token not found or does not match',status=status.HTTP_400_BAD_REQUEST)

"""