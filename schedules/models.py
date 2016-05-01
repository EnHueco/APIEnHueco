from django.db import models
from django.conf import settings
from django.core import serializers
from django.utils import timezone
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
import json
import datetime


# Create your models here.

class Gap(models.Model):
    ### Constants
    FREE_TIME = 'FT'
    CLASS = 'CLASS'

    id = models.AutoField(primary_key=True)

    # Event type -> Used for further improvements on Gap class
    type = models.CharField(max_length=30)

    # Optional Values
    name = models.TextField(null=False, blank=True)
    location = models.TextField(null=False, blank=True)

    # Time values
    start_hour_weekday = models.CharField(max_length=2)
    end_hour_weekday = models.CharField(max_length=2)
    start_hour = models.CharField(max_length=5)
    end_hour = models.CharField(max_length=5)

    # Control Attributes
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # Foreign Key
    user = models.ForeignKey(settings.USER_MODEL)

    def save(self, *args, **kwargs):
        super(Gap, self).save(*args, **kwargs)

        # Set new user schedule updated on
        self.user.schedule_updated_on = self.updated_on
        self.user.updated_on = self.updated_on
        self.user.save(update_fields=["immediate_event_updated_on", "updated_on"])

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
                if (sharedGap is not None):
                    sharedGaps.append(sharedGap)
        return sharedGaps

    def __str__(self):
        return "{} : {}".format(self.name, self.location)

    # TODO: Update and fix to make it work with new 'end_hour_weekday' field.
    def cross(self, gap2):
        """
        :type gap2: Gap
        :param gap2:
        :return:
        """

        # Si son distintos dias

        if (self.start_hour_weekday != gap2.start_hour_weekday):
            return None

        # Si no se cruzan
        if (int(self.end_hour) <= int(gap2.start_hour) or int(self.start_hour) >= int(gap2.end_hour)):
            return None
        else:

            if (int(gap2.start_hour) <= int(self.start_hour) <= int(gap2.end_hour)):
                starthour = self.start_hour
            else:
                starthour = gap2.start_hour

            if (int(self.end_hour) <= int(gap2.end_hour)):
                endhour = self.end_hour
            else:
                endhour = gap2.end_hour

            return Gap(start_hour_weekday=self.start_hour_weekday, start_hour=starthour, end_hour=endhour)


class ImmediateEvent(models.Model):
    # Event type -> Either FREE_TIME or CLASS
    type = models.CharField(max_length=30, default=Gap.FREE_TIME)

    # Optional Values
    name = models.TextField(null=False, blank=True, default="")
    location = models.TextField(null=False, blank=True, default="")

    # End date of the immediate event
    valid_until = models.DateTimeField(default=datetime.datetime.now())

    # Control Attributes
    updated_on = models.DateTimeField(auto_now=True)

    # User Key
    user = models.OneToOneField(
        settings.USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='immediate_event'
    )

    def save(self, *args, **kwargs):
        super(ImmediateEvent, self).save(*args, **kwargs)

        # Set new user schedule updated on
        self.user.immediate_event_updated_on = self.updated_on
        self.user.updated_on = self.updated_on
        self.user.save(update_fields=["immediate_event_updated_on", "updated_on"])
