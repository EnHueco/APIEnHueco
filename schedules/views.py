from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from models import Gap, ImmediateEvent
from schedules.serializers import GapSerializer, ImmediateEventSerializer, ImmediateEventSerializerNoUser, \
    ImmediateEventSerializerNoUserNoLocation, ImmediateEventSerializerNoUserNoName, \
    ImmediateEventSerializerNoUserNoNameNoLocation, GapSerializerID, EventSerializerNoUser
from users.models import User


class GapsViewSet(viewsets.ViewSet):
    def list(self, request, pk):

        gaps = Gap.objects.filter(user_id=pk)
        ser = GapSerializer(gaps, many=True)
        return Response(ser.data)

    def create(self, request):

        serializer = GapSerializer(data=request.data)

        if not serializer.is_valid():
            serializer = GapSerializer(data=request.data, exclude=('name',))
            if not serializer.is_valid():
                serializer = GapSerializer(data=request.data, exclude=('location',))
        if not serializer.is_valid():
            serializer = GapSerializer(data=request.data, exclude=('name', 'location',))
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def create_many(self, request, pk):

        valid_serializers = [EventSerializerNoUser(data=request.data, many=True),
                             EventSerializerNoUser(data=request.data, exclude=('name',), many=True),
                             EventSerializerNoUser(data=request.data, exclude=('location',), many=True),
                             EventSerializerNoUser(data=request.data, exclude=('name', 'location',), many=True)
                             ]
        for serializer in valid_serializers:
            if serializer.is_valid():
                user = User.objects.get(login=pk)
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        last_serializer = valid_serializers[len(valid_serializers) - 1]
        return Response(last_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def cross(self, request, pk1, pk2):

        gaps_user1 = Gap.objects.filter(user_id=pk1)
        gaps_user2 = Gap.objects.filter(user_id=pk2)

        sharedGaps = Gap.crossGaps(gaps_user1, gaps_user2)

        ser = GapSerializer(sharedGaps, many=True)
        return Response(ser.data)

    def delete(self, request, pk, id):

        gap = Gap.objects.filter(user_id=pk, id=id).first()
        if (gap is not None):
            gap.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete_many(self, request, pk):

        gaps_query = Q()
        events_to_delete = GapSerializerID(many=True, data=request.data)
        if events_to_delete.is_valid():
            for event in events_to_delete.validated_data:
                gaps_query = gaps_query | Q(id=event['id'])
            Gap.objects.filter(gaps_query).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(events_to_delete.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, id):

        gap = Gap.objects.filter(user_id=pk, id=id).first()
        if (gap is not None):
            valid_serializers = [GapSerializer(gap, data=request.data),
                                 GapSerializer(gap, data=request.data, exclude=('name',)),
                                 GapSerializer(gap, data=request.data, exclude=('location',)),
                                 GapSerializer(gap, data=request.data, exclude=('name', 'location',))
                                 ]
            for serializer in valid_serializers:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            last_serializer = valid_serializers[len(valid_serializers) - 1]
            return Response(last_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ImmediateEventViewSet(viewsets.ViewSet):
    def update(self, request, pk):
        immediate_event = ImmediateEvent.objects.filter(user=pk).all()
        if len(immediate_event) == 1:
            allowed_serializers = [ImmediateEventSerializerNoUser, ImmediateEventSerializerNoUserNoName,
                                   ImmediateEventSerializerNoUserNoLocation,
                                   ImmediateEventSerializerNoUserNoNameNoLocation]
            for serializer_class in allowed_serializers:
                serializer = serializer_class(immediate_event[0], data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response('{error: "bad request"}', status=status.HTTP_400_BAD_REQUEST)
