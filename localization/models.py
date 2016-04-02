from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Location(models.Model):
    # User
    user = models.OneToOneField(User, primary_key=True)

    # BSSID
    bssid = models.CharField(max_length=30, default="")
    bssid_date = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return '{} : {}'.format(self.bssid, self.bssid_date)


@receiver(post_save, sender=User)
def create_location(sender, instance, created, **kwargs):
    if created:
        Location.objects.create(user=instance)
