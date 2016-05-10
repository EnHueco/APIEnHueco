__author__ = 'Diego'
from rest_framework import serializers
import schedules.models as models


class GapSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = models.Gap

    # read_only_fields = ('created_on', 'updated_on')

    def to_representation(self, instance):
        repr = super(GapSerializer, self).to_representation(instance)

        if hasattr(instance, 'user'):
            if not instance.user.shares_event_names: repr['name'] = ''
            if not instance.user.shares_event_locations: repr['location'] = ''

        return repr

class GapSerializerNoUser(GapSerializer):

    class Meta:
        model = models.Gap
        exclude = ('user',)

class EventSerializerNoUser(GapSerializer):
    class Meta:
        model = models.Gap
        exclude = ('user',)


class GapSerializerID(serializers.ModelSerializer):
    class Meta:
        model = models.Gap
        fields = ('id',)
        extra_kwargs = {'id': {'read_only': False}}


class ImmediateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImmediateEvent
        read_only = ('updated_on',)


class ImmediateEventSerializerNoUser(serializers.ModelSerializer):
    class Meta:
        model = models.ImmediateEvent
        exclude = ('user',)
        read_only = ('updated_on',)


class ImmediateEventSerializerNoUserNoName(serializers.ModelSerializer):
    class Meta:
        model = models.ImmediateEvent
        exclude = ('user', 'name')
        read_only = ('updated_on',)


class ImmediateEventSerializerNoUserNoLocation(serializers.ModelSerializer):
    class Meta:
        model = models.ImmediateEvent
        exclude = ('user', 'location')
        read_only = ('updated_on',)


class ImmediateEventSerializerNoUserNoNameNoLocation(serializers.ModelSerializer):
    class Meta:
        model = models.ImmediateEvent
        exclude = ('user', 'name', 'location')
        read_only = ('updated_on',)
