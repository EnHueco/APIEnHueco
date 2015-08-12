__author__ = 'Diego'
from rest_framework import serializers
import schedules.models as models


class GapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gap
        fields = ('day','start_hour','end_hour', 'updated_on', 'user')