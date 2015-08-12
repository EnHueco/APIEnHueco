from django.db import models
from django.core import exceptions
from django.conf import settings
import string
import random
import hashlib
from django.utils import timezone
# Create your models here.


class Token(models.Model):

    value = models.CharField(max_length=256)
    owner = models.ForeignKey(settings.USER_MODEL, primary_key=True)
    created_on = models.DateTimeField(default=timezone.now())

    @classmethod
    def create(cls, user):
        new = cls()
        new.value = hashlib.sha256(''.join(random.choice(string.ascii_uppercase) for i in range(32))).hexdigest()
        new.owner = user
        return new


class Tokenizer(models.Model):

    @staticmethod
    def assignToken(user):

        token = Token.create(user)
        token.save()
        return token

    @staticmethod
    def authenticate(user_id, tokenValue):

        try:
            token = Token.objects.get(value=tokenValue)
            if token.owner.login == user_id:
                return True
        except exceptions.ObjectDoesNotExist:
            # TOKEN not found
            return False
        except exceptions.MultipleObjectsReturned:
            # Many Tokens found
            tokens = Token.objects.query(value=tokenValue)
            for token in tokens:
                if token.owner.login == user_id:
                    return True
                else:
                    return False