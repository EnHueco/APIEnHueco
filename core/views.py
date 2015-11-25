import datetime
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from django.core import exceptions
from django.db.models import Q

from authentication.models import *

from tokenizer.models import *
from schedules.models import *
from localization.models import *
from users.serializers import *
from tokenizer.serializers import *
from localization.views import *
from schedules.views import GapsViewSet
from users.views import *

import string

# Method that authenticates user if valid token and user_id is given
class APIView(APIView):

    def set_authentication_params(self, request):

        self.user_id =  request.META.get('HTTP_X_USER_ID','');
        self.token = request.META.get('HTTP_X_USER_TOKEN','');

    def authenticate(self):
        return Tokenizer.authenticate(self.user_id, self.token)

    def unauthorized_response(self):
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class Authenticate(APIView):
    """
    Authentication Resource

    """
    def post(self, request):
        """
        Authenticates a User
        ---
        response_serializer: TokenSerializer
        parameters:
            - name: user_id
              type: string
              required: true
            - name: password
              type: string
              required: true
        """
        user_id = request.data['user_id']
        password = request.data['password']

        ldapWrapper = LDAPWrapper()
        if(ldapWrapper.authenticate(user_id, password)):
            finalUser = None
            try:
                finalUser = User.objects.get(login=user_id)
                # user already exists
            except exceptions.ObjectDoesNotExist:
                data = ldapWrapper.search(user_id)
                firstNames = string.capwords(data['givenName'][0].strip())
                lastNames = string.capwords(data['sn'][0].strip())

                finalUser = User.objects.create(login=user_id, firstNames=firstNames, lastNames=lastNames)

            except exceptions.MultipleObjectsReturned as e:
                return Response(e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            token = Tokenizer.assignToken(finalUser)
            serializer = TokenSerializer(token)
            return Response(serializer.data)

        else:
            # Invalid Credentials
            return Response(status=status.HTTP_400_BAD_REQUEST)


# ------ USER ------

class UserDetail(APIView):
    """
    User Detail
    """
    # parser_classes = (FormParser, MultiPartParser, )
    parser_classes = (FileUploadParser,)


    def get(self, request):
        """
        Shows user information
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """

        self.set_authentication_params(request)
        if self.authenticate():
            return UsersViewSet().show(request,self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put (self, request):
        """
        Uploads user information
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if request.data.get('file') != None:
            request.data['imageURL'] = request.data['file']

        if self.authenticate():
            return UsersViewSet().updateImageURL(request, self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# ------ FRIEND REQUESTS ------

class ReceivedFriendRequestsList(APIView):
    """
    Received friend-requests
     """
    def get(self, request):
        """
        Shows received friend-requests list
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: FriendRequestSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return ReceivedFriendRequestViewSet().list(request, self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SentFriendRequestList(APIView):
    """
    Sent friend-requests
    """
    def get(self, request):
        """
        Shows sent friend-requests list
        ---
        serializer: FriendRequestSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return SentFriendRequestViewSet().list(request, pk=self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

#  ------  FRIENDSHIPS -------
class FriendDetail(APIView):

    """
    Friends detail
    """
    def get(self, request, fpk):
        """
        Show friend detail
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().show(request, self.user_id, fpk)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, fpk):
        """
        Adds friend with fpk
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().create(request,pk=self.user_id,fpk=fpk)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, fpk):
        """
        Removes friendship with user fpk
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().delete(request, self.user_id, fpk)
        else:
            #
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class FriendList(APIView):
    """
    Lists of friends
    """
    def get(self, request):
        """
        Shows friends list
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().list(request, self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        """
        Shows friends list, those which info were received.
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().list(request, self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class FriendListSync(APIView):
    """
    Lists of friends with synchronization information
    """
    def get(self, request):
        """
        Shows friends list synchronization information.
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSyncSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return FriendsViewSet().list(request, self.user_id, isSync=True)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class FriendListGapNow(APIView):
    """
    Lists of friends with gap now
    """

    def get(self, request):
        """
        Shows friends list with gap now
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():

            actualDay = str(datetime.date.today()+1)

            gaps = Gap.objects.filter(user__friends__contains=self.user_id, day=actualDay, )


            return FriendsViewSet().list(request, self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# ------- USERS -------

class UserList(APIView):
    """
    User detail
    """
    def get(self, request, searchID):
        """
        Shows users with gap now
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        response_serializer: UserSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            users = User.objects.filter(Q(login__contains=searchID) | Q(firstNames__contains=searchID) | Q(lastNames__contains=searchID)).exclude(login=self.user_id)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



# ------- GAPS -------

class GapsDetail(APIView):
    """
    Gap detail
    """
    def put(self, request, gid):
        """
        Updates a Gap with ID gid
        ---
        response_serializer: GapSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return GapsViewSet().update(request, self.user_id, gid)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, gid):
        """
        Deletes a Gap with ID gid
        ---

        """
        self.set_authentication_params(request)
        if self.authenticate():
            return GapsViewSet().delete(request, self.user_id, gid)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)



class GapsList(APIView):
    """
    List of gaps
    """
    def get(self, request):
        """
        Shows list of gaps
        ---
        response_serializer: GapSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return GapsViewSet().list(request, self.user_id)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        """
        Inserts a new gap
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        serializer: GapSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            return GapsViewSet().create(request)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class GapsFriendList(APIView):
    """
    Friends gap list
    """

    def get(self, request, fpk):
        """
        Shows friend gap list
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        serializer: GapSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            if Friendship.areFriendsPK(self.user_id, fpk):
                return GapsViewSet().list(request, fpk)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class GapsCross(APIView):
    """
    Gap cross resource
    """
    def get(self, request, fpk):
        """
        Show mutual gaps with friend
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
              description: User ID
            - name: X-USER-TOKEN
              paramType: header
              description: User Token
        serializer: GapSerializer
        """
        self.set_authentication_params(request)
        if self.authenticate():
            if Friendship.areFriendsPK(self.user_id,fpk):
                return GapsViewSet().cross(request, pk1=self.user_id, pk2=fpk)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class LocationList(APIView):
    """
    Friends location list
    """
    def get(self, request):
        """
        Shows location list of user friends
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        serializer: UserLocationSerializer
        """
        #self.set_authentication_params(request)
        #if self.authenticate():
        return LocationsViewSet().list(request,pk="user1")
#        else:
 #           return Response(status=status.HTTP_401_UNAUTHORIZED)

class LocationDetail(APIView):
    """
    Location detail
    """
    def put(self, request):
        """
        Updates user location
        ---
        parameters:
            - name: X-USER-ID
              paramType: header
            - name: X-USER-TOKEN
              paramType: header
        serializer: UserLocationSerializer
        """
        #self.set_authentication_params(request)
        #if self.authenticate():
        return LocationsViewSet().update(request,pk="d")
        #else:
        #    return self.unauthorized_response()


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