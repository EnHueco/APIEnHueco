from django.shortcuts import render
import datetime, sys
from rest_framework import viewsets, status
from rest_framework.response import Response
from localization.serializers import LocationSerializer
from users.serializers import UserLocationSerializer
from users.models import User

class LocationsViewSet(viewsets.ViewSet):

    def list(self, request, pk):
        try:
            now = datetime.datetime.now()
            earlier = datetime.datetime.now() - datetime.timedelta(minutes=5)
            friends = User.objects.get(login=pk).friends.exclude(location__bssid="").filter(location__bssid_date__range=(earlier, now))
            serializer = UserLocationSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(sys.exc_info()[0],status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            user = User.objects.get(login=pk)
            serializer = LocationSerializer(user.location, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Invalid Serializer", status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError) as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(sys.exc_info()[0],status=status.HTTP_500_INTERNAL_SERVER_ERROR)

