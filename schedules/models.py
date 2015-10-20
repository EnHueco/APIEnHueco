from django.db import models
from django.conf import settings
from django.core import serializers
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
import json

# Create your models here.

class Gap(models.Model):

    # Time values
    weekday = models.CharField(max_length=2)
    start_hour = models.CharField(max_length=5)
    end_hour = models.CharField(max_length=5)

    # Event type -> Used for further improvements on Gap class
    type = models.CharField(max_length=10)

    # Optional Values
    name = models.TextField()
    location = models.TextField()

    # Control Attributes
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    # Foreign Key
    user = models.ForeignKey(settings.USER_MODEL)

    @classmethod
    def create(cls, day, start_hour, end_hour, user):
        return cls(day=day, start_hour=start_hour, end_hour=end_hour, user=user)

    @classmethod
    def crossGaps(cls, gaps1, gaps2):
        """
        :type gaps1: list[Gap]
        :type gaps2: list[Gap]
        :return sharedGaps: Gap
        """

        for gap1 in gaps1:
            for gap2 in gaps2:
                sharedGaps = []
                sharedGap = gap1.cross(gap2)
                if(sharedGap is not None):
                    sharedGaps.append(sharedGap)
        return sharedGaps


    def __str__(self):
        return "{} : {} -> {}".format(self.user, self.start_hour, self.end_hour)

    def cross(self, gap2):
        """
        :type gap2: Gap
        :param gap2:
        :return:
        """

        # Si son distintos dias

        if(self.day != gap2.day):
            return None

        # Si no se cruzan
        if(int(self.end_hour) <= int(gap2.start_hour)
            or int(self.start_hour) >= int(gap2.end_hour)):
            return None
        else:

            if(int(gap2.start_hour) <= int(self.start_hour) <= int(gap2.end_hour)):
                starthour = self.start_hour
            else:
                starthour = gap2.start_hour

            if(int(self.end_hour) <= int(gap2.end_hour)):
                endhour = self.end_hour
            else:
                endhour = gap2.end_hour

            return Gap(day=self.day, start_hour=starthour, end_hour=endhour)

