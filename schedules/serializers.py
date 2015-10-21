__author__ = 'Diego'
from rest_framework import serializers
import schedules.models as models


class GapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gap
        fields = (
            'type',
            'name',
            'location',
            'start_hour_weekday',
            'end_hour_weekday',
            'start_hour',
            'end_hour',
            'updated_on',
            'user')

        extra_kwargs = {
            'name': {
                'read_only': True,
            },
            'location': {
                'read_only': True,
            },
        }