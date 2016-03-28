from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from models import Gap, ImmediateEvent
from schedules.serializers import GapSerializer, ImmediateEventSerializer, ImmediateEventSerializerNoUser


class GapsViewSet(viewsets.ViewSet) :
	def list (self, request, pk) :

		gaps = Gap.objects.filter(user_id=pk)
		ser = GapSerializer(gaps, many=True)
		return Response(ser.data)


	def create (self, request) :

		serializer = GapSerializer(data=request.data)

		if not serializer.is_valid() :
			serializer = GapSerializer(data=request.data, exclude=('name',))
			if not serializer.is_valid() :
				serializer = GapSerializer(data=request.data, exclude=('location',))
                if not serializer.is_valid() :
                    serializer = GapSerializer(data=request.data, exclude=('name','location',))
                    if not serializer.is_valid() :
					    return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data)


	def cross (self, request, pk1, pk2) :

		gaps_user1 = Gap.objects.filter(user_id=pk1)
		gaps_user2 = Gap.objects.filter(user_id=pk2)

		sharedGaps = Gap.crossGaps(gaps_user1, gaps_user2)

		ser = GapSerializer(sharedGaps, many=True)
		return Response(ser.data)


	def delete (self, request, pk, id) :

		gap = Gap.objects.filter(user_id=pk, id=id).first()
		if (gap is not None) :
			gap.delete()
			return Response(status=status.HTTP_200_OK)
		else :
			return Response(status=status.HTTP_400_BAD_REQUEST)


	def update (self, request, pk, id) :

		gap = Gap.objects.filter(user_id=pk, id=id).first()
		if (gap is not None) :
			serializer = GapSerializer(gap, partial=True, data=request.data)
			if (serializer.is_valid()) :
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.error_messages, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else :
			return Response(status=status.HTTP_400_BAD_REQUEST)


class ImmediateEventViewSet(viewsets.ViewSet) :
	def update (self, request, pk) :
		immediate_event = ImmediateEvent.objects.filter(user=pk).all()
		if len(immediate_event) == 1 :
			serializer = ImmediateEventSerializerNoUser(immediate_event[0], partial=True, data=request.data)
			if serializer.is_valid() :
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.error_messages, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else :
			return Response('{error: "bad request"}',status=status.HTTP_400_BAD_REQUEST)
